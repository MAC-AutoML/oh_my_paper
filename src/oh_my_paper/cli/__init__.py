"""Command line helpers for local oh-my-paper validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from oh_my_paper.artifacts.store import ArtifactStore
from oh_my_paper.evals.fixtures import run_fixture_file
from oh_my_paper.gates.evidence import run_evidence_gate
from oh_my_paper.workflows.demo import initialize_demo_workspace, run_demo_workflow


def _print_json(data: object) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _status(_args: argparse.Namespace) -> int:
    print("oh my paper is installed; Milestone 3 local demo workflow is available.")
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
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        args = parser.parse_args(["status"] if argv is None else [*argv, "status"])
    return int(args.func(args))
