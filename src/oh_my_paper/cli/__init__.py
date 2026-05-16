"""Command line helpers for local oh-my-paper validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from oh_my_paper.artifacts.store import ArtifactStore
from oh_my_paper.evals.capture import capture_fixture
from oh_my_paper.evals.changelog import append_changelog
from oh_my_paper.evals.fixtures import run_fixture_file
from oh_my_paper.evals.report import run_eval_report, write_eval_report
from oh_my_paper.gates.evidence import run_evidence_gate
from oh_my_paper.materials.intake import intake_pdf
from oh_my_paper.packaging.skills import packaging_status
from oh_my_paper.runtime.mock_runs import run_mock_app_server_probe
from oh_my_paper.workflows.demo import initialize_demo_workspace, run_demo_workflow
from oh_my_paper.workflows.full_paper import generate_full_paper_from_pdf, review_full_paper


def _print_json(data: object) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _status(_args: argparse.Namespace) -> int:
    print("oh my paper is installed; Milestone 6 official skill-installer packaging metadata is available.")
    return 0


def _validate_artifacts(args: argparse.Namespace) -> int:
    report = ArtifactStore.from_path(args.workspace).validate()
    _print_json(report.to_dict())
    return 0 if report.ok else 1


def _evidence_gate(args: argparse.Namespace) -> int:
    store = ArtifactStore.from_path(args.workspace)
    result = run_evidence_gate(store.claims_path, store.evidence_path)
    _print_json(result.to_dict())
    return 0 if result.ok else 1


def _run_eval(args: argparse.Namespace) -> int:
    results = run_fixture_file(Path(args.fixture_file))
    _print_json([result.to_dict() for result in results])
    return 0 if all(result.ok for result in results) else 1


def _intake_material(args: argparse.Namespace) -> int:
    result = intake_pdf(args.pdf, args.material_id, args.materials_root)
    _print_json(result.to_dict())
    return 0


def _packaging_status(_args: argparse.Namespace) -> int:
    _print_json(packaging_status())
    return 0


def _capture_fixture(args: argparse.Namespace) -> int:
    result = capture_fixture(
        args.workspace,
        args.output,
        fixture_id=args.fixture_id,
        purpose=args.purpose,
        privacy=args.privacy,
    )
    _print_json(result.to_dict())
    return 0


def _eval_report(args: argparse.Namespace) -> int:
    report = run_eval_report(args.fixture_files)
    if args.output:
        write_eval_report(report, args.output)
    if args.changelog:
        append_changelog(args.changelog, report, args.note)
    _print_json(report.to_dict())
    return 0 if report.ok else 1


def _mock_app_server(args: argparse.Namespace) -> int:
    summary = run_mock_app_server_probe(args.workspace, args.fixture_file)
    _print_json(summary)
    return 0 if all(result["status"] == "pass" for result in summary["eval_results"]) else 1


def _init_workspace(args: argparse.Namespace) -> int:
    root = initialize_demo_workspace(args.workspace, overwrite=args.overwrite)
    _print_json({"workspace": str(root), "created": True, "synthetic": True})
    return 0


def _run_demo(args: argparse.Namespace) -> int:
    result = run_demo_workflow(args.workspace)
    _print_json(result.to_dict())
    return 0 if result.ok else 1


def _generate_paper(args: argparse.Namespace) -> int:
    related = Path(args.related_context).read_text(encoding="utf-8") if args.related_context else ""
    result = generate_full_paper_from_pdf(
        args.pdf,
        args.workspace,
        env_file=args.env_file,
        related_context=related,
        reviewer=not args.no_review,
    )
    _print_json(result.to_dict())
    return 0 if result.ok else 1


def _review_paper(args: argparse.Namespace) -> int:
    related = Path(args.related_context).read_text(encoding="utf-8") if args.related_context else ""
    review = review_full_paper(args.paper, env_file=args.env_file, related_context=related)
    if args.output:
        Path(args.output).write_text(json.dumps(review, indent=2, ensure_ascii=False), encoding="utf-8")
    _print_json(review)
    return 0 if review.get("verdict") == "PASS" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="oh-my-paper")
    subparsers = parser.add_subparsers(dest="command")

    init = subparsers.add_parser("init", help="create a synthetic local paper workspace")
    init.add_argument("workspace", nargs="?", default=".")
    init.add_argument("--overwrite", action="store_true", help="overwrite existing demo artifacts")
    init.set_defaults(func=_init_workspace)

    status = subparsers.add_parser("status", help="show installation status")
    status.set_defaults(func=_status)

    validate = subparsers.add_parser("validate-artifacts", help="validate required workspace artifacts")
    validate.add_argument("workspace", nargs="?", default=".")
    validate.set_defaults(func=_validate_artifacts)

    gate = subparsers.add_parser("evidence-gate", help="run unsupported-claim evidence gate")
    gate.add_argument("workspace", nargs="?", default=".")
    gate.set_defaults(func=_evidence_gate)

    eval_parser = subparsers.add_parser("run-eval", help="run synthetic JSONL eval fixtures")
    eval_parser.add_argument("fixture_file")
    eval_parser.set_defaults(func=_run_eval)

    demo = subparsers.add_parser("run-demo", help="run deterministic local MVP workflow")
    demo.add_argument("workspace")
    demo.set_defaults(func=_run_demo)

    full = subparsers.add_parser("generate-paper", help="generate a full paper draft from a local PDF and optionally run strict Gemini review")
    full.add_argument("pdf")
    full.add_argument("workspace")
    full.add_argument("--env-file", default=".env")
    full.add_argument("--related-context")
    full.add_argument("--no-review", action="store_true")
    full.set_defaults(func=_generate_paper)

    review = subparsers.add_parser("review-paper", help="run strict Gemini-compatible review on a generated paper")
    review.add_argument("paper")
    review.add_argument("--env-file", default=".env")
    review.add_argument("--related-context")
    review.add_argument("--output")
    review.set_defaults(func=_review_paper)

    mock_app = subparsers.add_parser("mock-app-server", help="run mocked App Server adapter probe")
    mock_app.add_argument("workspace")
    mock_app.add_argument("fixture_file")
    mock_app.set_defaults(func=_mock_app_server)

    intake = subparsers.add_parser(
        "intake-material",
        help="extract and classify a local PDF into ignored materials cache",
    )
    intake.add_argument("pdf")
    intake.add_argument("--material-id", required=True)
    intake.add_argument("--materials-root", default="materials/paper-ai")
    intake.set_defaults(func=_intake_material)

    packaging = subparsers.add_parser("packaging-status", help="show official skill-installer compatible paths")
    packaging.set_defaults(func=_packaging_status)

    capture = subparsers.add_parser("capture-fixture", help="capture a workspace run as a regression fixture")
    capture.add_argument("workspace")
    capture.add_argument("output")
    capture.add_argument("--fixture-id", required=True)
    capture.add_argument("--purpose", required=True)
    capture.add_argument("--privacy", choices=["synthetic", "redacted", "private"], default="redacted")
    capture.set_defaults(func=_capture_fixture)

    report = subparsers.add_parser("eval-report", help="run fixture files and optionally write report/changelog")
    report.add_argument("fixture_files", nargs="+")
    report.add_argument("--output")
    report.add_argument("--changelog")
    report.add_argument("--note", default="eval report")
    report.set_defaults(func=_eval_report)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        args = parser.parse_args(["status"] if argv is None else [*argv, "status"])
    return int(args.func(args))
