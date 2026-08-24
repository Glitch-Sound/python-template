# プロジェクト構成

## ディレクトリ構造

```text
python-template/
├── src/
│   └── python_template/          # アプリケーションの本体（src レイアウト）
│       └── __init__.py           # 公開エントリーポイント `main` の現行配置
├── tests/                        # `src/` の振る舞いを検証する pytest テスト
├── scripts/                      # 開発・リポジトリ運用を補助するスクリプト
│   └── check_repository.py       # ファイルサイズ、設定形式、秘密鍵などの検査
├── openspec/                     # SDD の仕様と変更成果物
│   ├── changes/                  # 進行中の変更（生成・検証・アーカイブの対象）
│   ├── specs/                    # アーカイブ済みの最新仕様
│   ├── schemas/                  # OpenSpec のカスタムスキーマと成果物テンプレート
│   ├── config.yaml               # OpenSpec 共通コンテキストと運用ルール
│   ├── product.md                # プロダクト概要
│   ├── structure.md              # 本文書
│   └── tech.md                   # 技術スタックと開発基準
├── .agents/                      # AI エージェント向けのローカルスキル設定
├── .github/prompts/              # GitHub Copilot 向け OpenSpec プロンプト
├── .claude/                      # Claude Code 向け設定（存在する場合）
├── pyproject.toml                # Python プロジェクト、ツール、依存関係の設定
├── uv.lock                       # Python 依存関係の再現可能なロックファイル
├── .python-version               # 使用する Python のメジャー・マイナーバージョン
├── .pre-commit-config.yaml       # コミット前に実行する品質チェック
├── package.json                  # OpenSpec を含む Node.js 開発依存関係
├── package-lock.json             # Node.js 依存関係のロックファイル
└── README.md                     # 利用方法、開発手順、採用パッケージの説明
```

生成物・ローカル環境は Git 管理しない。代表例は `.venv/`、`node_modules/`、`__pycache__/`、`.pytest_cache/`、`.ruff_cache/` であり、`.gitignore` の定義に従う。

## 配置原則

### アプリケーションコード

- 実行時に使用する Python コードは必ず `src/python_template/` 配下に置く。プロジェクトをテンプレートとして利用する際は、パッケージ名と `pyproject.toml` のエントリーポイントを同時に変更する。
- CLI の入口は `pyproject.toml` の `[project.scripts]` で公開し、入口関数は引数の受け取りと終了状態の制御に集中させる。業務処理は用途別モジュールへ分離する。
- 新しい機能は責務単位でモジュールを分け、循環依存を作らない。共有処理は、複数の機能に明確な共通責務が生じた場合だけ共通モジュールへ抽出する。
- 外部 I/O（ファイル、ネットワーク、環境変数、標準入出力）は境界に集約し、業務ロジックは可能な限り副作用から分離してテスト可能にする。

### テスト

- テストは `tests/` 配下に配置し、対象モジュールと対応が分かる `test_<module>.py` の名前を使用する。
- 1テストは1つの振る舞いを検証し、テスト名に前提または期待結果を表す動詞を含める。
- 外部サービス、時計、ファイルシステムなどの非決定的な依存は、必要に応じて `pytest-mock` 等で置き換える。実装詳細でなく公開振る舞いを検証する。
- テスト用データはテストの近くに置き、機密情報や実環境の認証情報を含めない。

### 設定・依存関係・スクリプト

- Python の依存関係、対応 Python バージョンの互換性範囲、ツール設定は `pyproject.toml` を唯一の定義元とする。`.python-version` はローカル開発で使用する Python バージョンを固定する補助設定であり、`pyproject.toml` の対応範囲と常に一致させる。依存関係を変更したら `uv.lock` を更新する。
- Node.js の開発依存関係は `package.json` に定義し、変更時は `package-lock.json` を更新する。
- リポジトリ運用や反復作業のスクリプトは `scripts/` に置く。実行時コードを `scripts/` から import しない。
- 環境依存の設定値は環境変数またはローカルの `.env` から与え、`.env` に機密情報をコミットしない。

### OpenSpec 成果物

- 進行中の変更は `openspec/changes/<change-id>/` に置く。`change-id` は変更内容を表す kebab-case とする。
- 最新の正式仕様は `openspec/specs/<capability-path>/spec.md` に置く。capability の新規パス要素は kebab-case とする。
- 仕様は「何を満たすか」、設計は「どの責務がどのように満たすか」、タスクは「どの順で何を変更・検証するか」を記述し、同じ情報を重複させない。
- スキーマとテンプレートの変更は `openspec/schemas/my-workflow/` に置き、既存の OpenSpec 生成・検証との互換性を確認する。

## 命名規則

| 対象 | 規則 | 例 |
| --- | --- | --- |
| Python パッケージ・モジュール | 小文字の `snake_case` | `python_template`, `settings.py` |
| Python 関数・変数 | `snake_case` | `load_settings` |
| Python クラス・型 | `PascalCase` | `AppSettings` |
| 定数 | `UPPER_SNAKE_CASE` | `DEFAULT_TIMEOUT_SECONDS` |
| pytest ファイル・テスト関数 | `test_` 接頭辞 + `snake_case` | `test_main_prints_greeting` |
| OpenSpec change / capability パス | `kebab-case` | `add-export`, `identity/user-auth` |
| Markdown 文書 | 役割が分かる小文字の固定名または `kebab-case` | `proposal.md`, `api-contract.md` |

## 変更時の確認

- 新規ファイルは上記の責務と命名規則に従う配置を選択する。不明確な場合は既存の近いモジュールを優先する。
- パッケージ構成、公開 CLI、設定形式、OpenSpec のパスを移動または改名する変更では、参照元、互換性、移行手順を設計に明記する。
- ビルド成果物、キャッシュ、一時ファイル、資格情報を追加しない。必要な例は、値を含まないテンプレートまたは安全なダミー値で提供する。
