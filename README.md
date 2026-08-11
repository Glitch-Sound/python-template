# Python Template

`uv` と `OpenSpec` を使用した `Python` 開発用テンプレートです。

## 開発環境

- `Python` 3.13
- `uv`
- `OpenSpec`

### 対応 AI コーディングエージェント

- `OpenAI Codex`
- `GitHub Copilot`
- `Claude Code`

## クイックスタート

依存関係をインストールします。

```bash
uv sync --locked
npm ci
```

アプリケーションを実行します。

```bash
uv run python-template
```

## 開発

テストを実行します。

```bash
uv run --locked pytest
```

リントを実行します。

```bash
uv run --locked ruff check .
```

フォーマットを実行します。

```bash
uv run --locked ruff format .
```

型チェックを実行します。

```bash
uv run --locked pyright
```

`pre-commit` フックを有効化し、すべてのチェックを実行します。

```bash
uv run --locked pre-commit install
uv run --locked pre-commit run --all-files
```

コミット時には、以下のチェックを実行します。

| チェック | 内容 |
| --- | --- |
| `Ruff lint` | `Python` コードを静的解析します。<br />バグ、インポート順、モダンな構文、簡略化、静的に検出できるセキュリティ上の問題を確認し、自動修正可能なものは修正します。 |
| `Ruff format` | `Python` コードが `Ruff` のフォーマットに従っているか確認します。 |
| `Pyright` | 型の不整合を検査します。 |
| `pytest` | テストを実行します。<br />テストの失敗や収集エラーがある場合は、コミットを中断します。 |
| `Safety` | 依存パッケージを `Safety` の脆弱性データベースと照合します。 |
| `Repository checks` | 1 MB を超えるファイル、マージ競合の痕跡、不正な `YAML`/`TOML`、秘密鍵、末尾改行・行末の空白を検出します。 |


## SDD

各ユースケースでの開発の方法です。<br />
なお、ここでは `Codex` での手順を基準とします。

主に `openspec` 配下で管理され、以下構造となります。

```text
python-template/
└── openspec/
    ├── specs/            # 最新仕様
    ├── changes/          # 変更計画
    │
    ├── schemas/          # 成果物定義
    │
    ├── config.yaml       # 共通ルール
    ├── product.md        # プロダクト定義
    ├── tech.md           # 利用技術定義
    └── structure.md      # 構造定義
```

### 初期設定

事前に以下プロダクト全体に関連する定義を行なってください。

#### config.yaml

追加ルール、適用・保存時の運用リストなどあれば定義してください。

#### product.md

何を作るかを定義してください。
目的・スコープ・中核機能・ユースケース・ドメインなどを記載します。

#### tech.md

どう作るかの制約を定義してください。
アーキテクチャ・主要ライブラリ・開発基準・テストなどを記載します。

#### structure.md

どこになにを置くかを定義してください。
ディレクトリ構造・命名規則・配置原則などを記載します。

### TODO

SSDの進め方を記載予定です。

## 事前設定

このテンプレートは、以下のコマンドを用いて作成しています。

### プロジェクトの作成

```bash
uv init python-template \
  --name python_template \
  --app \
  --python "==3.13"
```

### アプリケーションの依存関係

アプリケーションの実行時に使用するパッケージです。

```bash
uv add typer loguru pydantic-settings
```

| パッケージ | 説明 |
| --- | --- |
| `typer` | 型ヒントを利用して `CLI` アプリケーションを構築するためのライブラリです。<br />コマンド、引数、オプション、ヘルプなどを簡潔に定義できます。 |
| `loguru` | `Python` 標準の `logging` よりシンプルな `API` でログ出力を扱うためのライブラリです。<br />ログレベル、ファイル出力、ローテーションなどを簡単に設定できます。 |
| `pydantic-settings` | 環境変数や `.env` などからアプリケーション設定を読み込み、`Pydantic` による型検証を行うためのライブラリです。 |

### 開発用の依存関係

開発、テスト、静的解析で使用するパッケージです。

```bash
uv add --dev pre-commit pyright pytest pytest-mock ruff safety
```

| パッケージ | 説明 |
| --- | --- |
| `pytest` | `Python` のテストフレームワークです。<br />シンプルな `assert` を使って単体テストや結合テストを記述できます。 |
| `pytest-mock` | `pytest` からモックを扱いやすくするプラグインです。<br />`mocker` フィクスチャを利用して、関数やオブジェクトの差し替え、呼び出し検証などを行えます。 |
| `ruff` | 高速な `Python` リンター／フォーマッターです。<br />コード品質のチェックとコードフォーマットを担当します。 |
| `safety` | 依存パッケージを既知の脆弱性データベースと照合します。 |
| `pyright` | `Python` の静的型チェッカーです。<br />型ヒントを解析し、実行前に型の不整合を検出します。 |

#### 開発ツール

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

Pyright
└── Type Check
    └── 型ヒントの不整合を静的解析
```

### `OpenSpec`

`OpenSpec` は、プロジェクトローカルの開発用依存関係としてインストールしています。

```bash
npm install --save-dev @fission-ai/openspec@latest
```

`Codex`、`GitHub Copilot`、`Claude Code` 向けに `OpenSpec` を初期化しています。

```bash
npx openspec init --tools codex,github-copilot,claude
```

## プロジェクト構成

```text
python-template/
├── .agents/              # AI エージェント用スキル
├── .claude/              # Claude Code
├── .github/              # GitHub Copilot
├── openspec/             # OpenSpec specifications
│
├── src/
│   └── python_template/
│
├── tests/
│
├── pyproject.toml        # Python プロジェクト設定
├── uv.lock               # Python の依存関係ロックファイル
├── .python-version       # Python バージョン
│
├── package.json          # OpenSpec の依存関係
├── package-lock.json     # Node.js の依存関係ロックファイル
│
└── README.md
```

## 依存関係の管理

公開 `PyPI` および `npm` レジストリへの直接接続は行いません。<br />
依存関係の追加・更新は、社内承認済みのパッケージレジストリまたはキャッシュを設定した環境でのみ実施してください。

`Python` パッケージを追加します。

```bash
uv add <package>
```

開発用のパッケージを追加します。

```bash
uv add --dev <package>
```

依存関係を同期します。

```bash
uv sync
```

`OpenSpec` を含む `Node.js` の依存関係を同期します。

```bash
npm ci
```
