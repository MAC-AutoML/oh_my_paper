"""Shared artifact validation types."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Issue:
    """A validator or gate finding."""

    severity: str
    message: str
    path: str | None = None
    subject: str | None = None


@dataclass
class ValidationReport:
    """Structured result for artifact checks."""

    name: str
    inspected: list[str] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not any(issue.severity in {"error", "blocking"} for issue in self.issues)

    def add(self, severity: str, message: str, path: str | None = None, subject: str | None = None) -> None:
        self.issues.append(Issue(severity=severity, message=message, path=path, subject=subject))

    def extend(self, other: "ValidationReport") -> None:
        self.inspected.extend(other.inspected)
        self.issues.extend(other.issues)

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "ok": self.ok,
            "inspected": self.inspected,
            "issues": [issue.__dict__ for issue in self.issues],
        }
