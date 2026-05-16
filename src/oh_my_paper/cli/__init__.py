"""Minimal CLI placeholder for Milestone 1 skeleton validation."""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="oh-my-paper")
    parser.add_argument("command", nargs="?", default="status", choices=["status"])
    parser.parse_args(argv)
    print("oh my paper skeleton is installed; workflow automation starts in Milestone 2.")
    return 0
