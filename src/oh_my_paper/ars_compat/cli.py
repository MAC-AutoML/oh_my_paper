"""CLI handlers for ARS compatibility validation."""

from __future__ import annotations

import json
from argparse import ArgumentParser, Namespace
from pathlib import Path

from oh_my_paper.ars_compat.pipeline import pipeline_plan
from oh_my_paper.ars_compat.config import config_status_report, resolve_config
from oh_my_paper.ars_compat.semantic_scholar import SemanticScholarVerifier, load_citations, verifier_from_offline_fixtures
from oh_my_paper.ars_compat.registry import mode_registry, route_for_trigger, validate_agents, validate_modes
from oh_my_paper.ars_compat.validators import (
    load_json,
    validate_citation_anchors,
    validate_claim_support,
    validate_integrity_report,
    validate_material_passport,
    validate_sprint_contract,
)
from oh_my_paper.workflows.ars_pipeline import ars_stage_status, run_ars_pipeline


def print_json(data: object) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_mode_registry(_args: Namespace) -> int:
    validation = validate_modes()
    print_json({"count": len(mode_registry()), **validation.to_dict()})
    return 0 if validation.ok else 1


def cmd_agent_registry(_args: Namespace) -> int:
    validation = validate_agents()
    print_json(validation.to_dict())
    return 0 if validation.ok else 1


def cmd_route(args: Namespace) -> int:
    route = route_for_trigger(args.trigger)
    print_json({"found": route is not None, "route": route})
    return 0 if route else 1


def cmd_validate_passport(args: Namespace) -> int:
    result = validate_material_passport(args.path)
    print_json(result.to_dict())
    return 0 if result.ok else 1


def cmd_check_sprint_contract(args: Namespace) -> int:
    result = validate_sprint_contract(args.path)
    print_json(result.to_dict())
    return 0 if result.ok else 1


def cmd_check_citation_anchors(args: Namespace) -> int:
    result = validate_citation_anchors(args.path)
    print_json(result.to_dict())
    return 0 if result.ok else 1


def cmd_check_integrity_report(args: Namespace) -> int:
    result = validate_integrity_report(args.path)
    print_json(result.to_dict())
    return 0 if result.ok else 1


def cmd_check_data_access(_args: Namespace) -> int:
    levels = sorted({row["data_access_level"] for row in mode_registry()})
    print_json({"ok": levels == ["raw", "redacted", "verified_only"], "levels": levels})
    return 0 if levels == ["raw", "redacted", "verified_only"] else 1


def cmd_check_claims(args: Namespace) -> int:
    data = load_json(args.path)
    claims = data.get("claims", data if isinstance(data, list) else [])
    result = validate_claim_support(claims if isinstance(claims, list) else [])
    print_json(result.to_dict())
    return 0 if result.ok else 1


def cmd_pipeline_plan(args: Namespace) -> int:
    plan = pipeline_plan(args.stage)
    print_json(plan.to_dict())
    return 0


def cmd_run_ars_pipeline(args: Namespace) -> int:
    result = run_ars_pipeline(
        args.material,
        args.workspace,
        config=args.config,
        offline_fixtures=args.offline_fixtures,
        max_review_rounds=args.max_review_rounds,
        live=not bool(args.offline_fixtures),
    )
    print_json(result)
    return 0 if result.get("ok") else 1


def cmd_ars_stage_status(args: Namespace) -> int:
    print_json(ars_stage_status(args.workspace))
    return 0


def cmd_config_status(args: Namespace) -> int:
    report = config_status_report(args.config)
    print_json(report)
    return 0 if report.get("status") != "error" else 1


def cmd_verify_citations(args: Namespace) -> int:
    citations = load_citations(args.citations)
    if args.offline_fixtures:
        verifier = verifier_from_offline_fixtures(args.offline_fixtures)
    else:
        report = resolve_config(args.config)
        scholar = report.semantic_scholar
        verifier = SemanticScholarVerifier(
            mode=str(scholar["effective_mode"]),
            api_key=None,
            cache_dir=str(scholar["cache_dir"]),
            request_interval_seconds=float(scholar["request_interval_seconds"]),
            title_similarity_threshold=float(scholar["title_similarity_threshold"]),
        )
    report = verifier.verify(citations)
    print_json(report)
    return 0 if not any(check["status"] == "error" for check in report["checks"]) else 1


def add_ars_subcommands(subparsers) -> None:
    config = subparsers.add_parser("config-status", help="show redacted config resolution status")
    config.add_argument("--config")
    config.set_defaults(func=cmd_config_status)

    verify = subparsers.add_parser("verify-citations", help="verify citation metadata with Semantic Scholar")
    verify.add_argument("citations")
    verify.add_argument("--config")
    verify.add_argument("--offline-fixtures")
    verify.set_defaults(func=cmd_verify_citations)

    mode = subparsers.add_parser("ars-mode-registry", help="validate ARS-to-Codex mode registry")
    mode.set_defaults(func=cmd_mode_registry)

    agents = subparsers.add_parser("ars-agent-registry", help="validate ARS-to-Codex agent registry")
    agents.set_defaults(func=cmd_agent_registry)

    route = subparsers.add_parser("ars-route", help="route an old ARS-style intent to a Codex skill")
    route.add_argument("trigger")
    route.set_defaults(func=cmd_route)


    data_access = subparsers.add_parser("ars-check-data-access", help="validate ARS compatibility data access levels")
    data_access.set_defaults(func=cmd_check_data_access)

    claims = subparsers.add_parser("ars-check-claims", help="validate JSON claim support records")
    claims.add_argument("path", type=Path)
    claims.set_defaults(func=cmd_check_claims)

    pipeline = subparsers.add_parser("ars-pipeline-plan", help="show Codex-native ARS pipeline stage plan")
    pipeline.add_argument("--stage", default="research")
    pipeline.set_defaults(func=cmd_pipeline_plan)

    run_pipeline = subparsers.add_parser("run-ars-pipeline", help="run offline-capable four-skill ARS pipeline")
    run_pipeline.add_argument("material")
    run_pipeline.add_argument("workspace")
    run_pipeline.add_argument("--config")
    run_pipeline.add_argument("--offline-fixtures")
    run_pipeline.add_argument("--max-review-rounds", type=int, default=1)
    run_pipeline.set_defaults(func=cmd_run_ars_pipeline)

    stage_status = subparsers.add_parser("ars-stage-status", help="show ARS pipeline state and next stage")
    stage_status.add_argument("workspace")
    stage_status.set_defaults(func=cmd_ars_stage_status)

    passport = subparsers.add_parser("ars-validate-passport", help="validate Material Passport JSON")
    passport.add_argument("path", type=Path)
    passport.set_defaults(func=cmd_validate_passport)

    sprint = subparsers.add_parser("ars-check-sprint-contract", help="validate reviewer sprint contract JSON")
    sprint.add_argument("path", type=Path)
    sprint.set_defaults(func=cmd_check_sprint_contract)

    anchors = subparsers.add_parser("ars-check-citation-anchors", help="validate citation anchor audit JSON")
    anchors.add_argument("path", type=Path)
    anchors.set_defaults(func=cmd_check_citation_anchors)

    integrity = subparsers.add_parser("ars-check-integrity-report", help="validate integrity report JSON")
    integrity.add_argument("path", type=Path)
    integrity.set_defaults(func=cmd_check_integrity_report)
