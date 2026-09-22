# プロジェクト構成

## 共通ディレクトリ

```text
project/
├── src/<package_name>/  # 実行時コード
├── tests/               # 自動テスト
├── scripts/             # 開発・運用の補助スクリプト
├── openspec/            # OpenSpecの共通基盤、仕様、change
│   ├── changes/         # 進行中の変更
│   ├── specs/           # 正式仕様
│   └── schemas/         # ワークフローと成果物雛形
├── pyproject.toml       # Pythonとツールの設定
├── AGENTS.md            # AI 開発エージェントの共通指示
├── CLAUDE.md            # Claude Code 用の共通指示入口
└── README.md            # 利用方法
```

## 配置原則

- 実行時コードは `src/<package_name>/`、テストは `tests/`、開発・運用用スクリプトは `scripts/` に置く。
- 公開CLIやライブラリの入口はプロジェクト設定で定義し、業務処理は責務ごとに分ける。
- OpenSpecの仕様は「何を満たすか」、設計は「どのように満たすか」、タスクは「どの順で実装・検証するか」を扱う。
- 進行中の変更は `openspec/changes/<change-id>/`、正式仕様は `openspec/specs/<capability-path>/spec.md` に置く。

## 命名規則

| 対象 | 規則 | 例 |
| --- | --- | --- |
| Pythonパッケージ・モジュール | 小文字の `snake_case` | `app_core`, `settings.py` |
| Python関数・変数 | `snake_case` | `load_settings` |
| Pythonクラス・型 | `PascalCase` | `AppSettings` |
| pytestファイル・関数 | `test_` 接頭辞 + `snake_case` | `test_feature_returns_result` |
| OpenSpec change / capability | `kebab-case` | `add-export`, `identity/user-auth` |
