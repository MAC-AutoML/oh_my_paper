"""Artifact parsers and validators for oh-my-paper workspaces."""

from __future__ import annotations

__all__ = ["ArtifactStore", "Issue", "ValidationReport"]


def __getattr__(name: str) -> object:
    if name == "ArtifactStore":
        from oh_my_paper.artifacts.store import ArtifactStore

        return ArtifactStore
    if name in {"Issue", "ValidationReport"}:
        from oh_my_paper.artifacts.types import Issue, ValidationReport

        return {"Issue": Issue, "ValidationReport": ValidationReport}[name]
    raise AttributeError(name)
