"""Small GitHub-flavored Markdown table parser for local artifacts."""

from __future__ import annotations


def _split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(set(cell.replace(":", "").strip()) <= {"-"} and "-" in cell for cell in cells)


def parse_first_table(text: str) -> list[dict[str, str]]:
    """Parse the first markdown table in text into row dictionaries.

    The project artifacts intentionally use simple pipe tables. This parser is
    deliberately small and deterministic; complex markdown is out of scope.
    """

    lines = [line.rstrip() for line in text.splitlines()]
    for index, line in enumerate(lines):
        if "|" not in line:
            continue
        headers = _split_row(line)
        if index + 1 >= len(lines):
            continue
        separator = _split_row(lines[index + 1])
        if not _is_separator(separator):
            continue
        rows: list[dict[str, str]] = []
        for row_line in lines[index + 2 :]:
            if "|" not in row_line or not row_line.strip().startswith("|"):
                break
            cells = _split_row(row_line)
            if len(cells) < len(headers):
                cells.extend([""] * (len(headers) - len(cells)))
            rows.append(dict(zip(headers, cells, strict=False)))
        return rows
    return []
