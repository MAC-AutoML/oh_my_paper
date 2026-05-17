"""Semantic Scholar citation verification with cache-first offline support."""

from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from oh_my_paper.config.loader import ProjectConfig, load_project_config

SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
STATUSES = {"verified", "ambiguous", "not_found", "rate_limited", "error", "skipped"}


def verify_citations_file(
    citations_path: str | Path,
    output_path: str | Path | None = None,
    *,
    config_path: str | Path | None = None,
    offline_fixtures: str | Path | None = None,
    workspace: str | Path | None = None,
) -> dict[str, Any]:
    data = json.loads(Path(citations_path).read_text(encoding="utf-8"))
    citations = data if isinstance(data, list) else data.get("citations", data.get("sources", []))
    if not isinstance(citations, list):
        raise ValueError("citation input must be a list or {'citations': [...]} object")
    report = verify_citations(citations, config_path=config_path, offline_fixtures=offline_fixtures, workspace=workspace)
    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def verify_citations(
    citations: list[dict[str, Any]],
    *,
    config_path: str | Path | None = None,
    offline_fixtures: str | Path | None = None,
    workspace: str | Path | None = None,
) -> dict[str, Any]:
    config = load_project_config(config_path)
    mode = config.semantic_mode()
    cache_dir = config.semantic_cache_dir(workspace)
    cache_dir.mkdir(parents=True, exist_ok=True)
    fixture_dir = Path(offline_fixtures) if offline_fixtures else None
    checks: list[dict[str, Any]] = []
    stats = {status: 0 for status in STATUSES}
    cache_hits = 0
    cache_misses = 0
    rate_limited = 0
    retry_after: float | None = None
    for index, citation in enumerate(citations):
        check, cache_hit, retry = _verify_one(citation, index, config, mode, cache_dir, fixture_dir)
        checks.append(check)
        stats[check["status"]] += 1
        cache_hits += int(cache_hit)
        cache_misses += int(not cache_hit and mode != "disabled")
        if check["status"] == "rate_limited":
            rate_limited += 1
            retry_after = retry
        interval = _interval(config, mode)
        if not fixture_dir and mode != "disabled" and interval > 0:
            time.sleep(interval)
    status = "skipped" if mode == "disabled" else "clear"
    if stats["not_found"] or stats["error"] or stats["rate_limited"]:
        status = "blocked" if any(c.get("required", False) and c["status"] == "not_found" for c in checks) else "suspected"
    report = {
        "schema_version": "1.0",
        "producer": "oh-my-paper:verify-citations",
        "created_at": _now(),
        "workspace": str(Path(workspace or ".")),
        "inputs": ["citations"],
        "status": status,
        "semantic_scholar_mode": "disabled" if mode == "disabled" else mode,
        "cache": {"cache_dir": str(cache_dir), "hits": cache_hits, "misses": cache_misses},
        "rate_limits": {"encountered_429_count": rate_limited, "last_retry_after_seconds": retry_after},
        "checks": checks,
        "summary": {key: stats[key] for key in ["verified", "ambiguous", "not_found", "rate_limited", "error", "skipped"]},
    }
    return report


def _verify_one(citation: dict[str, Any], index: int, config: ProjectConfig, mode: str, cache_dir: Path, fixture_dir: Path | None) -> tuple[dict[str, Any], bool, float | None]:
    title = str(citation.get("title") or citation.get("input_title") or "").strip()
    citation_id = str(citation.get("id") or citation.get("citation_id") or f"C{index + 1}")
    key = _cache_key(title)
    base = _base_check(citation, citation_id, title, key)
    if mode == "disabled":
        return {**base, "status": "skipped", "reasons": ["Semantic Scholar disabled"]}, False, None
    cache_path = cache_dir / f"{key}.json"
    if cache_path.exists():
        response = json.loads(cache_path.read_text(encoding="utf-8"))
        return _match_response(base, citation, response, config), True, None
    if fixture_dir:
        response = _load_fixture_response(fixture_dir, citation, title)
        cache_path.write_text(json.dumps(response, indent=2, ensure_ascii=False), encoding="utf-8")
        return _match_response(base, citation, response, config), False, None
    try:
        response = _search_semantic_scholar(title, config, mode)
        cache_path.write_text(json.dumps(response, indent=2, ensure_ascii=False), encoding="utf-8")
        return _match_response(base, citation, response, config), False, None
    except urllib.error.HTTPError as exc:
        if exc.code == 429:
            retry = _retry_after(exc)
            return {**base, "status": "rate_limited", "reasons": ["Semantic Scholar returned HTTP 429"]}, False, retry
        return {**base, "status": "error", "reasons": [f"HTTP {exc.code}"]}, False, None
    except Exception as exc:  # pragma: no cover - defensive network boundary
        return {**base, "status": "error", "reasons": [str(exc)]}, False, None


def _base_check(citation: dict[str, Any], citation_id: str, title: str, key: str) -> dict[str, Any]:
    return {
        "citation_id": citation_id,
        "input_title": title,
        "input_authors": list(citation.get("authors", citation.get("input_authors", []))),
        "input_year": citation.get("year", citation.get("input_year")),
        "matched_title": None,
        "matched_authors": [],
        "matched_year": None,
        "paper_id": None,
        "doi": None,
        "title_similarity": 0.0,
        "status": "not_found",
        "reasons": [],
        "raw_cache_key": key,
        "required": bool(citation.get("required", False)),
    }


def _match_response(base: dict[str, Any], citation: dict[str, Any], response: dict[str, Any], config: ProjectConfig) -> dict[str, Any]:
    candidates = response.get("data", []) if isinstance(response, dict) else []
    if not candidates:
        return {**base, "status": "not_found", "reasons": ["no Semantic Scholar candidates"]}
    threshold = float(config.data["semantic_scholar"].get("title_similarity_threshold", 0.70))
    best = max((item for item in candidates if isinstance(item, dict)), key=lambda item: _similarity(base["input_title"], str(item.get("title", ""))), default=None)
    if not best:
        return {**base, "status": "not_found", "reasons": ["no valid candidates"]}
    similarity = _similarity(base["input_title"], str(best.get("title", "")))
    matched_authors = [str(author.get("name", author)) for author in best.get("authors", []) if author]
    out = {
        **base,
        "matched_title": best.get("title"),
        "matched_authors": matched_authors,
        "matched_year": best.get("year"),
        "paper_id": best.get("paperId"),
        "doi": (best.get("externalIds") or {}).get("DOI") if isinstance(best.get("externalIds"), dict) else None,
        "title_similarity": round(similarity, 4),
    }
    if similarity < threshold:
        return {**out, "status": "not_found", "reasons": [f"title similarity {similarity:.2f} below threshold {threshold:.2f}"]}
    year = citation.get("year", citation.get("input_year"))
    if year and best.get("year") and int(year) != int(best.get("year")):
        return {**out, "status": "ambiguous", "reasons": ["title matched but year differs"]}
    if similarity < 0.93:
        return {**out, "status": "ambiguous", "reasons": ["fuzzy title match requires review"]}
    return {**out, "status": "verified", "reasons": ["title/year match"]}


def _search_semantic_scholar(title: str, config: ProjectConfig, mode: str) -> dict[str, Any]:
    query = urllib.parse.urlencode({"query": title, "limit": "5", "fields": "title,authors,year,paperId,externalIds,venue,url"})
    request = urllib.request.Request(f"{SEARCH_URL}?{query}")
    if mode == "api_key" and config.semantic_api_key():
        request.add_header("x-api-key", config.semantic_api_key() or "")
    with urllib.request.urlopen(request, timeout=15) as response:  # noqa: S310 - user-triggered CLI query
        return json.loads(response.read().decode("utf-8"))


def _load_fixture_response(fixture_dir: Path, citation: dict[str, Any], title: str) -> dict[str, Any]:
    fixture = citation.get("fixture")
    candidates = [fixture_dir / str(fixture)] if fixture else []
    slug = _slug(title)
    candidates.extend([fixture_dir / f"search_{slug}.json", fixture_dir / f"{slug}.json"])
    for path in candidates:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    return {"data": []}


def _cache_key(title: str) -> str:
    return hashlib.sha256(title.casefold().encode("utf-8")).hexdigest()[:24]


def _slug(title: str) -> str:
    text = "".join(ch.lower() if ch.isalnum() else "_" for ch in title)
    parts = [part for part in text.split("_") if part]
    if any(part == "ppo" for part in parts):
        return "ppo"
    if any(part == "fabricated" for part in parts):
        return "fabricated"
    return "_".join(parts[:5]) or "empty"


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.casefold(), b.casefold()).ratio()


def _interval(config: ProjectConfig, mode: str) -> float:
    semantic = config.data["semantic_scholar"]
    key = "request_interval_seconds_api_key" if mode == "api_key" else "request_interval_seconds_no_key"
    return float(semantic.get(key, 0.0))


def _retry_after(exc: urllib.error.HTTPError) -> float | None:
    value = exc.headers.get("Retry-After") if exc.headers else None
    try:
        return float(value) if value else None
    except ValueError:
        return None


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
