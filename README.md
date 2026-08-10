# Python Template

`uv` + OpenSpec を使用した Python 開発用テンプレート。

## Environment

- Python 3.13
- uv
- OpenSpec

### AI Coding Agents

- OpenAI Codex
- GitHub Copilot
- Claude Code

## Quick Start

依存関係をインストールします。

```bash
uv sync
npm ci
```

アプリケーションを実行します。

```bash
uv run python-template
```

## Development

テストを実行します。

```bash
uv run pytest
```

Lintを実行します。

```bash
uv run ruff check .
```

Formatを実行します。

```bash
uv run ruff format .
```

型チェックを実行します。

```bash
uv run ty check
```

pre-commitフックを有効化し、すべてのチェックを実行します。

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

コミット時には以下をチェックします。

| Check | 内容 |
| --- | --- |
| Ruff lint | Pythonコードを静的解析し、自動修正できる問題を修正します。 |
| Ruff format | PythonコードがRuffのフォーマットに従っているか確認します。 |
| pytest | テストを実行します。テストが未作成の場合のみ成功として扱い、失敗・収集エラーはコミットを中断します。 |
| Safety | インストール済み依存パッケージの既知の脆弱性を検査します。 |
| Basic file checks | 大きすぎる追加ファイル、マージ競合の痕跡、不正なYAML/TOML、秘密鍵を検出します。末尾改行の追加と行末空白の削除も行います。 |

## Pre-configured

このテンプレートは以下のコマンドで構築しています。

### Create Project

```bash
uv init python-template \
  --name python_template \
  --app \
  --python "==3.13"
```

### Application Dependencies

アプリケーションの実行時に使用するパッケージです。

```bash
uv add typer loguru pydantic-settings
```

| Package | Description |
| --- | --- |
| `typer` | 型ヒントを利用してCLIアプリケーションを構築するためのライブラリ。コマンド、引数、オプション、ヘルプなどを簡潔に定義できます。 |
| `loguru` | Python標準の`logging`よりシンプルなAPIでログ出力を扱うためのライブラリ。ログレベル、ファイル出力、ローテーションなどを簡単に設定できます。 |
| `pydantic-settings` | 環境変数や`.env`などからアプリケーション設定を読み込み、Pydanticによる型検証を行うためのライブラリ。 |

### Development Dependencies

開発、テスト、静的解析で使用するパッケージです。

```bash
uv add --dev pre-commit pytest pytest-mock ruff safety ty
```

| Package | Description |
| --- | --- |
| `pytest` | Pythonのテストフレームワーク。シンプルな`assert`を使って単体テストや結合テストを記述できます。 |
| `pytest-mock` | pytestからモックを扱いやすくするプラグイン。`mocker` fixtureを利用して関数やオブジェクトの差し替え、呼び出し検証などを行えます。 |
| `ruff` | 高速なPython Linter / Formatter。コード品質のチェックとコードフォーマットを担当します。 |
| `safety` | 依存パッケージに既知の脆弱性がないか検査します。 |
| `ty` | Pythonの静的型チェッカー。型ヒントを解析し、実行前に型の不整合を検出します。 |

#### Development Tools

各ツールの主な役割は以下のとおりです。

```text
pytest
└── Test
    └── コードが期待どおり動作するか検証

pytest-mock
└── Mock
    └── テスト対象の依存関係を差し替え

Ruff
├── Lint
│   └── コード上の問題を静的解析
└── Format
    └── コードスタイルを統一

ty
└── Type Check
    └── 型ヒントの不整合を静的解析
```

### OpenSpec

OpenSpecはプロジェクトローカルの開発依存としてインストールしています。

```bash
npm install --save-dev @fission-ai/openspec@latest
```

Codex、GitHub Copilot、Claude Code向けにOpenSpecを初期化しています。

```bash
npx openspec init --tools codex,github-copilot,claude
```

## Project Structure

```text
python-template/
├── .agents/              # AI agent skills
├── .claude/              # Claude Code
├── .github/              # GitHub Copilot
├── openspec/             # OpenSpec specifications
│
├── src/
│   └── python_template/
│
├── tests/
│
├── pyproject.toml        # Python project configuration
├── uv.lock               # Python dependency lock
├── .python-version       # Python version
│
├── package.json          # OpenSpec dependency
├── package-lock.json     # Node.js dependency lock
│
└── README.md
```

## Dependency Management

Pythonパッケージを追加します。

```bash
uv add <package>
```

開発用パッケージを追加します。

```bash
uv add --dev <package>
```

依存関係を同期します。

```bash
uv sync
```

OpenSpecを含むNode.js依存関係を同期します。

```bash
npm ci
```
