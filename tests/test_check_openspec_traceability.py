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
        """## Requirements Traceability

| 要件ID | 対応する設計節 | 責務・境界 | 実装タスク | 試験ケース | 検証方法 |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | Workflow | 結果生成 | 2.1 | TC-001 | unit test |

## Test Design

| TC ID | 要件ID | Scenario ID | テスト層 | 前提・操作 | 期待値 | pytest 実装 | 自動化 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-001 | REQ-001 | REQ-001-S01 | unit | 実行する | 結果 | `tests/test_example.py::test_example` | はい |
""",
        encoding="utf-8",
    )
    (change / "tasks.md").write_text(
        "- [ ] 2.1 結果生成を実装する。対応: REQ-001。\n"
        "- [ ] 3.1 `tests/test_example.py` に TC-001 の pytest テストを追加する。"
        " 対応: REQ-001 / REQ-001-S01。\n",
        encoding="utf-8",
    )


def run_check(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    """Run the script from a temporary repository root."""
    return subprocess.run(  # noqa: S603 -- test controls the fixed interpreter and script path.
        [sys.executable, str(SCRIPT_PATH.resolve()), *arguments],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )


def test_check_passes_when_all_traceability_links_exist(tmp_path: Path) -> None:
    write_change(tmp_path)

    result = run_check(tmp_path, "--change", "example")

    assert result.returncode == 0
    assert "passed" in result.stdout


def test_check_all_passes_when_changes_directory_does_not_exist(tmp_path: Path) -> None:
    result = run_check(tmp_path, "--all")

    assert result.returncode == 0
    assert "passed" in result.stdout


def test_check_reports_requirement_without_scenario(tmp_path: Path) -> None:
    write_change(tmp_path, include_scenario=False)

    result = run_check(tmp_path, "--change", "example")

    assert result.returncode == 1
    assert "REQ-001 に Scenario がありません" in result.stderr


def test_check_reports_missing_test_task(tmp_path: Path) -> None:
    write_change(tmp_path)
    tasks_file = tmp_path / "openspec" / "changes" / "example" / "tasks.md"
    tasks_file.write_text(
        "- [ ] 2.1 結果生成を実装する。対応: REQ-001。\n",
        encoding="utf-8",
    )

    result = run_check(tmp_path, "--change", "example")

    assert result.returncode == 1
    assert (
        "TC-001 に対応する pytest テスト作成・実行タスクがありません" in result.stderr
    )


def test_check_reports_missing_task_referenced_by_design(tmp_path: Path) -> None:
    write_change(tmp_path)
    design_file = tmp_path / "openspec" / "changes" / "example" / "design.md"
    design_file.write_text(
        design_file.read_text(encoding="utf-8").replace(
            "| REQ-001 | Workflow | 結果生成 | 2.1 |",
            "| REQ-001 | Workflow | 結果生成 | 9.9 |",
        ),
        encoding="utf-8",
    )

    result = run_check(tmp_path, "--change", "example")

    assert result.returncode == 1
    assert (
        "REQ-001 が参照する実装タスク 9.9 は tasks.md に存在しません" in result.stderr
    )


def test_check_reports_task_for_different_requirement(tmp_path: Path) -> None:
    write_change(tmp_path)
    tasks_file = tmp_path / "openspec" / "changes" / "example" / "tasks.md"
    tasks_file.write_text(
        tasks_file.read_text(encoding="utf-8").replace(
            "2.1 結果生成を実装する。対応: REQ-001。",
            "2.1 位置合わせを実装する。対応: REQ-002。",
        ),
        encoding="utf-8",
    )

    result = run_check(tmp_path, "--change", "example")

    assert result.returncode == 1
    assert (
        "REQ-001 が参照する実装タスク 2.1 はその要件を扱っていません" in result.stderr
    )
