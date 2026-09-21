from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = Path("scripts/check_openspec_traceability.py")


def write_change(root: Path, *, include_scenario: bool = True) -> None:
    """Create a minimal change that follows the project traceability format."""
    change = root / "openspec" / "changes" / "example"
    spec_dir = change / "specs" / "example"
    spec_dir.mkdir(parents=True)
    scenario = (
        """
#### Scenario: REQ-001-S01 正常系

- **WHEN** 実行する
- **THEN** 結果を返す
"""
        if include_scenario
        else ""
    )
    (spec_dir / "spec.md").write_text(
        f"""## ADDED Requirements

### Requirement: REQ-001 例

システムは、結果を返さなければならない。
{scenario}
""",
        encoding="utf-8",
    )
    (change / "design.md").write_text(
        """## Test Design

| TC ID | 要件ID | Scenario ID | テスト層 | 前提・操作 | 期待値 | pytest 実装 | 自動化 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-001 | REQ-001 | REQ-001-S01 | unit | 実行する | 結果 | `tests/test_example.py::test_example` | はい |
""",
        encoding="utf-8",
    )
    (change / "tasks.md").write_text(
        "- [ ] 3.1 `tests/test_example.py` に TC-001 の pytest テストを追加する。\n",
        encoding="utf-8",
    )


def run_check(root: Path) -> subprocess.CompletedProcess[str]:
    """Run the script from a temporary repository root."""
    return subprocess.run(  # noqa: S603 -- test controls the fixed interpreter and script path.
        [sys.executable, str(SCRIPT_PATH.resolve()), "--change", "example"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )


def test_check_passes_when_all_traceability_links_exist(tmp_path: Path) -> None:
    write_change(tmp_path)

    result = run_check(tmp_path)

    assert result.returncode == 0
    assert "passed" in result.stdout


def test_check_reports_requirement_without_scenario(tmp_path: Path) -> None:
    write_change(tmp_path, include_scenario=False)

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "REQ-001 に Scenario がありません" in result.stderr


def test_check_reports_missing_test_task(tmp_path: Path) -> None:
    write_change(tmp_path)
    tasks_file = tmp_path / "openspec" / "changes" / "example" / "tasks.md"
    tasks_file.write_text("- [ ] 2.1 TC-001 を実装する。\n", encoding="utf-8")

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert (
        "TC-001 に対応する pytest テスト作成・実行タスクがありません" in result.stderr
    )
