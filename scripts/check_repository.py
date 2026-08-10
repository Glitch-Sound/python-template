"""Run repository checks without making network requests."""

from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path
from shutil import which

import yaml

MAX_FILE_SIZE_BYTES = 1_000_000
PRIVATE_KEY_MARKER = "-----BEGIN "
CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
IGNORED_PATH_PARTS = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
}


def repository_files() -> list[Path]:
    """Return tracked and untracked repository files, excluding ignored files."""
    git_path = which("git")
    if git_path is None:
        raise RuntimeError("git must be available to run repository checks")
    result = subprocess.run(  # noqa: S603 -- executable is resolved from the local PATH.
        [git_path, "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        check=True,
        capture_output=True,
    )
    return [Path(name) for name in result.stdout.decode().split("\0") if name]


def check_file(path: Path) -> list[str]:
    """Return validation errors for one repository file."""
    if not path.is_file() or IGNORED_PATH_PARTS.intersection(path.parts):
        return []

    errors: list[str] = []
    if path.stat().st_size > MAX_FILE_SIZE_BYTES:
        errors.append(f"{path}: exceeds {MAX_FILE_SIZE_BYTES // 1_000_000} MB")

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return errors

    if path.suffix not in {".lock"}:
        for line_number, line in enumerate(content.splitlines(), start=1):
            if line.startswith(CONFLICT_MARKERS):
                errors.append(f"{path}:{line_number}: merge conflict marker")
            if line.rstrip(" \t") != line:
                errors.append(f"{path}:{line_number}: trailing whitespace")
        if content and not content.endswith("\n"):
            errors.append(f"{path}: missing final newline")

    if (
        path.name != Path(__file__).name
        and PRIVATE_KEY_MARKER in content
        and "PRIVATE KEY-----" in content
    ):
        errors.append(f"{path}: possible private key")

    try:
        if path.suffix == ".toml":
            tomllib.loads(content)
        elif path.suffix in {".yaml", ".yml"}:
            yaml.safe_load(content)
    except (tomllib.TOMLDecodeError, yaml.YAMLError) as error:
        errors.append(f"{path}: invalid configuration: {error}")
    return errors


def main() -> int:
    errors = [error for path in repository_files() for error in check_file(path)]
    if errors:
        print("Repository checks failed:", *errors, sep="\n", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
