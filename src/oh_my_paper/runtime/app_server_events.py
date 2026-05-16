"""Minimal JSON-RPC-like App Server event models for mocked tests."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from uuid import uuid4


def _id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


@dataclass(frozen=True)
class AppServerMessage:
    method: str
    params: dict[str, object]
    jsonrpc: str = "2.0"
    id: str | None = None

    def to_dict(self) -> dict[str, object]:
        data: dict[str, object] = {"jsonrpc": self.jsonrpc, "method": self.method, "params": self.params}
        if self.id is not None:
            data["id"] = self.id
        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, separators=(",", ":"))


@dataclass
class MockThread:
    thread_id: str = field(default_factory=lambda: _id("thread"))
    turns: list[str] = field(default_factory=list)
    items: list[dict[str, object]] = field(default_factory=list)

    def new_turn(self, phase: str, intent: str) -> str:
        turn_id = _id("turn")
        self.turns.append(turn_id)
        self.items.append({"type": "turn_started", "turn_id": turn_id, "phase": phase, "intent": intent})
        return turn_id
