"""Hash skill evaluation inputs without treating release metadata as instructions."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path


FRONTMATTER_DELIMITER = b"---"
METADATA_KEY = b"metadata:"
VERSION_KEY_PREFIX = b"  version:"
VERSION_LINE_RE = re.compile(
    rb'^  version: "(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)'
    rb'(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?'
    rb'(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"$'
)


def line_content(line: bytes) -> bytes:
    return line.rstrip(b"\r\n")


def normalized_skill_instruction_bytes(path: Path) -> bytes:
    """Return skill bytes with only the direct metadata.version line removed."""
    lines = path.read_bytes().splitlines(keepends=True)
    if not lines or line_content(lines[0]) != FRONTMATTER_DELIMITER:
        raise ValueError(f"{path}: SKILL.md must start with YAML frontmatter")

    closing_delimiters = [
        index
        for index, line in enumerate(lines[1:], start=1)
        if line_content(line) == FRONTMATTER_DELIMITER
    ]
    if not closing_delimiters:
        raise ValueError(f"{path}: SKILL.md frontmatter is not closed")
    frontmatter_end = closing_delimiters[0]

    metadata_lines = [
        index
        for index, line in enumerate(lines[1:frontmatter_end], start=1)
        if line_content(line) == METADATA_KEY
    ]
    if len(metadata_lines) != 1:
        raise ValueError(f"{path}: SKILL.md frontmatter must contain one top-level metadata mapping")

    metadata_start = metadata_lines[0]
    metadata_end = frontmatter_end
    for index in range(metadata_start + 1, frontmatter_end):
        content = line_content(lines[index])
        if content and not content.startswith((b" ", b"\t")):
            metadata_end = index
            break

    version_lines = [
        index
        for index in range(metadata_start + 1, metadata_end)
        if VERSION_LINE_RE.fullmatch(line_content(lines[index])) is not None
    ]
    malformed_version_lines = [
        index
        for index in range(metadata_start + 1, metadata_end)
        if (
            line_content(lines[index]).startswith(VERSION_KEY_PREFIX)
            and VERSION_LINE_RE.fullmatch(line_content(lines[index])) is None
        )
    ]
    if malformed_version_lines:
        raise ValueError(f"{path}: metadata.version must use a quoted semantic version")
    if len(version_lines) != 1:
        raise ValueError(f"{path}: metadata must contain one direct version field")

    version_line = version_lines[0]
    return b"".join(line for index, line in enumerate(lines) if index != version_line)


def skill_instruction_sha256(path: Path) -> str:
    return hashlib.sha256(normalized_skill_instruction_bytes(path)).hexdigest()
