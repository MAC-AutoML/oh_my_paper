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
from oh_my_paper.packaging.skills import install_skills, list_installed_skills, uninstall_skills
from oh_my_paper.runtime.mock_runs import run_mock_app_server_probe
from oh_my_paper.workflows.demo import initialize_demo_workspace, run_demo_workflow


def _print_json(data: object) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _status(_args: argparse.Namespace) -> int:
    print("oh my paper is installed; Milestone 6 packaging helpers are available.")
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


def _install_skills(args: argparse.Namespace) -> int:
    result = install_skills(args.target_dir, overwrite=args.overwrite)
    _print_json(result.to_dict())
    return 0


def _uninstall_skills(args: argparse.Namespace) -> int:
    result = uninstall_skills(args.target_dir)
    _print_json(result.to_dict())
    return 0


def _list_skills(args: argparse.Namespace) -> int:
    _print_json({"target_dir": args.target_dir, "skills": list_installed_skills(args.target_dir)})
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

    mock_app = subparsers.add_parser("mock-app-server", help="run mocked App Server adapter probe")
    mock_app.add_argument("workspace")
    mock_app.add_argument("fixture_file")
    mock_app.set_defaults(func=_mock_app_server)

    install = subparsers.add_parser("install-skills", help="copy paper-ai skills into a Codex skills directory")
    install.add_argument("target_dir", nargs="?")
    install.add_argument("--overwrite", action="store_true")
    install.set_defaults(func=_install_skills)

    uninstall = subparsers.add_parser("uninstall-skills", help="remove paper-ai skills from a Codex skills directory")
    uninstall.add_argument("target_dir", nargs="?")
    uninstall.set_defaults(func=_uninstall_skills)

    list_parser = subparsers.add_parser("list-skills", help="list installed paper-ai skills in a target directory")
    list_parser.add_argument("target_dir", nargs="?")
    list_parser.set_defaults(func=_list_skills)

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
