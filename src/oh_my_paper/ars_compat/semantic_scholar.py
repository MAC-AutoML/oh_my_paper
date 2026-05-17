"""Offline-testable Semantic Scholar citation verification."""

from __future__ import annotations

import hashlib
import json
import time
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Callable

HttpGet = Callable[[str, dict[str, str], float], dict[str, object]]


class SemanticScholarVerifier:
    def __init__(self, *, mode: str = "no_key", api_key: str | None = None, cache_dir: str | Path | None = None, request_interval_seconds: float = 0.0, title_similarity_threshold: float = 0.7, http_get: HttpGet | None = None) -> None:
        self.mode = mode
        self.api_key = api_key
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.request_interval_seconds = request_interval_seconds
        self.title_similarity_threshold = title_similarity_threshold
        self.http_get = http_get or _urllib_get

    def verify(self, citations: list[dict[str, Any]]) -> dict[str, object]:
        checks = []
        hits = misses = rate_count = 0
        for citation in citations:
            key = _cache_key(citation)
            cached = self._read_cache(key)
            if cached is None:
                misses += 1
                response = self._fetch(citation)
                self._write_cache(key, response)
                if self.request_interval_seconds:
                    time.sleep(self.request_interval_seconds)
            else:
                hits += 1
                response = cached
            check = self._check(citation, response, key)
            if check["status"] == "rate_limited":
                rate_count += 1
            checks.append(check)
        summary = {status: sum(1 for c in checks if c["status"] == status) for status in ["verified", "ambiguous", "not_found", "rate_limited", "error", "skipped"]}
        return {
            "schema_version": "1.0",
            "producer": "oh-my-paper:verify-citations",
            "status": "clear" if not any(c["status"] in {"error", "rate_limited"} for c in checks) else "suspected",
            "semantic_scholar_mode": self.mode,
            "cache": {"cache_dir": str(self.cache_dir or ""), "hits": hits, "misses": misses},
            "rate_limits": {"encountered_429_count": rate_count, "last_retry_after_seconds": None},
            "checks": checks,
            "summary": summary,
        }

    def _fetch(self, citation: dict[str, Any]) -> dict[str, object]:
        headers = {"User-Agent": "oh-my-paper/0.1"}
        if self.mode == "api_key" and self.api_key:
            headers["x-api-key"] = self.api_key
        query = urllib.parse.urlencode({"query": str(citation.get("title", "")), "limit": "5"})
        try:
            return self.http_get(f"https://api.semanticscholar.org/graph/v1/paper/search?{query}", headers, 20.0)
        except Exception as exc:  # network must never become verified
            return {"error": str(exc)}

    def _check(self, citation: dict[str, Any], response: dict[str, object], cache_key: str) -> dict[str, object]:
        if response.get("status_code") == 429:
            return _empty_check(citation, "rate_limited", ["Semantic Scholar returned HTTP 429"], cache_key)
        if response.get("error"):
            return _empty_check(citation, "error", [str(response["error"])], cache_key)
        candidates = response.get("data") if isinstance(response.get("data"), list) else []
        if not candidates:
            return _empty_check(citation, "not_found", ["No Semantic Scholar match"], cache_key)
        best = max((c for c in candidates if isinstance(c, dict)), key=lambda c: _similarity(str(citation.get("title", "")), str(c.get("title", ""))), default={})
        score = _similarity(str(citation.get("title", "")), str(best.get("title", "")))
        year_match = not citation.get("year") or citation.get("year") == best.get("year")
        status = "verified" if score >= self.title_similarity_threshold and year_match else "ambiguous" if score >= self.title_similarity_threshold else "not_found"
        authors = [a.get("name", "") for a in best.get("authors", [])] if isinstance(best.get("authors"), list) else []
        external = best.get("externalIds") if isinstance(best.get("externalIds"), dict) else {}
        return {
            "citation_id": str(citation.get("citation_id") or citation.get("id") or citation.get("title", "")),
            "input_title": str(citation.get("title", "")),
            "input_authors": citation.get("authors", []),
            "input_year": citation.get("year"),
            "matched_title": best.get("title"),
            "matched_authors": authors,
            "matched_year": best.get("year"),
            "paper_id": best.get("paperId"),
            "doi": external.get("DOI"),
            "title_similarity": round(score, 3),
            "status": status,
            "reasons": [],
            "raw_cache_key": cache_key,
        }

    def _read_cache(self, key: str) -> dict[str, object] | None:
        if not self.cache_dir:
            return None
        path = self.cache_dir / f"{key}.json"
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None

    def _write_cache(self, key: str, response: dict[str, object]) -> None:
        if not self.cache_dir:
            return
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        (self.cache_dir / f"{key}.json").write_text(json.dumps(response, ensure_ascii=False), encoding="utf-8")


def verifier_from_offline_fixtures(fixtures: str | Path) -> SemanticScholarVerifier:
    base = Path(fixtures)

    def http_get(url: str, _headers: dict[str, str], _timeout: float) -> dict[str, object]:
        query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get("query", [""])[0].lower()
        for path in sorted(base.glob("*.json")):
            stem_tokens = set(path.stem.lower().split("_"))
            query_tokens = {part for part in query.split() if len(part) > 2}
            if stem_tokens & query_tokens:
                return json.loads(path.read_text(encoding="utf-8"))
        not_found = base / "search_fabricated.json"
        return json.loads(not_found.read_text(encoding="utf-8")) if not_found.exists() else {"data": []}

    return SemanticScholarVerifier(mode="disabled", http_get=http_get)


def load_citations(path: str | Path) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("citations", data.get("sources", []))
    if not isinstance(data, list):
        raise ValueError("citation input must be a list or object with citations/sources")
    return [item for item in data if isinstance(item, dict)]


def _urllib_get(url: str, headers: dict[str, str], timeout: float) -> dict[str, object]:
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 - user-invoked verifier
        return json.loads(response.read().decode("utf-8"))


def _cache_key(citation: dict[str, Any]) -> str:
    payload = json.dumps({"title": citation.get("title"), "year": citation.get("year")}, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, left.lower(), right.lower()).ratio()


def _empty_check(citation: dict[str, Any], status: str, reasons: list[str], cache_key: str) -> dict[str, object]:
    return {
        "citation_id": str(citation.get("citation_id") or citation.get("id") or citation.get("title", "")),
        "input_title": str(citation.get("title", "")),
        "input_authors": citation.get("authors", []),
        "input_year": citation.get("year"),
        "matched_title": None,
        "matched_authors": [],
        "matched_year": None,
        "paper_id": None,
        "doi": None,
        "title_similarity": 0.0,
        "status": status,
        "reasons": reasons,
        "raw_cache_key": cache_key,
    }
