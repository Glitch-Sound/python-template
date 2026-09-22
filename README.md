# Python Template
`uv` と `OpenSpec` を使用した `Python` 開発用テンプレートです。


## 1. 開発環境
- `Python` 3.13
- `uv`
- `OpenSpec`


### 1.1. 対応 AI コーディングエージェント
- `OpenAI Codex`
- `GitHub Copilot`
- `Claude Code`


## 2. クイックスタート
依存関係をインストールします。

```bash
uv sync --locked
npm ci
```

OpenSpec を更新して生成済みの agent 用 instructions を更新する場合は、更新内容をレビューしたうえで次を実行します。`.agents/`、`.claude/`、`.github/` の各 instruction は OpenSpec が対象エージェント向けに生成する成果物であり、手作業で片方だけを変更しません。

```bash
npx openspec update
```

アプリケーションを実行します。

```bash
uv run python-template
```

## 3. 開発

コミット前には高速な基礎検査を実行します。初回だけフックを有効化してください。

```bash
uv run --locked pre-commit install
uv run --locked pre-commit run --all-files
```

PR を出す前、または雛形の広範な変更後は、CI と同じ品質検査を実行します。

```bash
npm run check
```

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

コミット時には以下のチェックを実行します。

| チェック | 内容 |
| --- | --- |
| `Ruff lint` | `Python` コードを静的解析します。<br />バグ、インポート順、モダンな構文、簡略化、静的に検出できるセキュリティ上の問題を確認します。 |
| `Ruff format` | `Python` コードが `Ruff` のフォーマットに従っているか確認します。 |
| `Repository checks` | 1 MB を超えるファイル、マージ競合の痕跡、不正な `YAML`/`TOML`、秘密鍵、末尾改行・行末の空白を検出します。 |

コミットを速く保つため、型検査、全テスト、OpenSpec のトレーサビリティ、依存関係の脆弱性検査は CI で実行します。CI は pull request、`main` への push、毎週月曜の定期実行、および手動実行で動きます。`npm run check` は CI と同じ format・lint・型検査・テスト・リポジトリ検査・全進行中 change のトレーサビリティ検査を実行します。

`Safety` の現行 `scan` コマンドは非対話 CI では API キーを必要とするため、雛形では互換性のある `safety check` を CI に限定して使用しています。Safety の CI 用認証を導入する案件では `scan` に置き換えてください。

### 3.1. AI コーディングエージェントの指示

共通の開発方針は [AGENTS.md](AGENTS.md) を正本とし、OpenAI Codex、Claude Code、GitHub Copilot から参照します。雛形・文書・振る舞いを変えない保守は直接変更できます。一方、外部から観測できる振る舞い、API、データ、セキュリティ、性能、外部連携、移行・運用を変える作業は OpenSpec change を先に作成します。曖昧な場合は要件を作り出さず、利用者に確認してください。


## 4. SDD
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


### 4.1. 初期設定
事前に以下プロダクト全体に関連する定義を行なってください。

| ファイル | 定義内容 |
| --- | --- |
| config.yaml | 追加ルール、適用・保存時の運用リストなど |
| product.md | 目的・スコープ・中核機能・ユースケース・ドメインなど |
| tech.md | アーキテクチャ・主要ライブラリ・開発基準・テストなど |
| structure.md | ディレクトリ構造・命名規則・配置原則など |


### 4.2. 開発の流れ
以下の順番で開発を進めてください。


#### 4.2.1. 調査・検討
```text
$openspec-explore [テーマ]
```
どのように進めていくか、チャットベースで相談してください。


#### 4.2.2. 作業ディレクトリ生成
```text
$openspec-new-change [変更名]
```
`openspec/config.yaml` の `schema: my-workflow` を既定スキーマとして、`openspec/changes/変更名/` が生成されます。各 change の `.openspec.yaml` に使用スキーマが記録されるため、以後の成果物生成・実装・検証でも同じワークフローが使用されます。


#### 4.2.3. 補足資料を用意（任意）
要件定義書、既存設計、調査結果などの補足資料がある場合は、`openspec/changes/変更名/input.md` に格納できます。<br />
`input.md` は OpenSpec が自動で読み込むファイルではないため、次の工程で「`input.md` を参照する」と明示して使用してください。


#### 4.2.4. ドキュメント生成
```text
$openspec-ff-change [変更名] [input.md を参照]
```
変更内容と、明示的に参照を依頼した `input.md` を基に、実装に必要なドキュメントを生成します。

生成される成果物では、次の対応関係を管理します。

| 成果物 | 記載する内容 |
| --- | --- |
| `spec.md` | 機能要件は `REQ-001`、非機能要件は `NREQ-001`、各要件のScenario、および試験方針 (`Test Policy`) |
| `design.md` | Scenarioごとの試験ケースID (`TC-001`)、pytest実装先、試験内容、網羅性 (`Coverage Confirmation`) |
| `tasks.md` | 要件ID・Scenario ID・TC-IDに対応する実装とpytestテスト作成・実行タスク |

実装変更を伴うScenarioには、自動テストコードを作成します。文書のみの変更など、テストコードが不要な場合は、`design.md` の `Test Exceptions` に理由、承認者、期限を記録します。

成果物の対応は、任意の時点で次のコマンドにより確認できます。これはコミットごとには実行せず、設計レビュー、実装前、verify / archive 前、PR の CI で実行してください。

```bash
# 指定した変更を確認
uv run --locked python scripts/check_openspec_traceability.py --change <change-name>

# 進行中の全変更を確認
uv run --locked python scripts/check_openspec_traceability.py --all
```

検査対象は、全REQ/NREQのScenario、全ScenarioのTC-IDとpytest実装先、全TC-IDのpytestテスト作成・実行タスクです。


#### 4.2.5. ドキュメント改善
```text
$openspec-update-change [変更名] [修正内容]
```
生成したドキュメントを壁打ちしながら品質を向上させます。


#### 4.2.6. 実装
```text
$openspec-apply-change [変更名]
```
生成したドキュメントから実装を行います。


#### 4.2.7. 検証
```text
$openspec-verify-change [変更名]
```
実装内容が問題ないか検証します。


#### 4.2.8. 仕様反映
```text
$openspec-archive-change [変更名]
```
変更内容を正式仕様として反映します。

アーカイブ前には、OpenSpec の厳密検証とトレーサビリティ検査の両方を通します。

```bash
npx openspec validate <change-name> --strict
uv run --locked python scripts/check_openspec_traceability.py --change <change-name>
```


## 5. 事前設定
このテンプレートは以下のコマンドを用いて作成しています。


### 5.1. プロジェクトの作成
```bash
uv init python-template \
  --name python_template \
  --app \
  --python "==3.13"
```


### 5.2. アプリケーションの依存関係
アプリケーションの実行時に使用するパッケージです。

```bash
uv add typer loguru pydantic-settings rich
```

| パッケージ | 説明 |
| --- | --- |
| `typer` | 型ヒントを利用して `CLI` アプリケーションを構築するためのライブラリです。<br />コマンド、引数、オプション、ヘルプなどを簡潔に定義できます。 |
| `loguru` | `Python` 標準の `logging` よりシンプルな `API` でログ出力を扱うためのライブラリです。<br />ログレベル、ファイル出力、ローテーションなどを簡単に設定できます。 |
| `pydantic-settings` | 環境変数や `.env` などからアプリケーション設定を読み込み、`Pydantic` による型検証を行うためのライブラリです。 |
| `rich` | ターミナル出力を見やすく装飾するためのライブラリです。<br />色付きテキスト、テーブル、進捗表示、例外トレースバックなどを表示できます。 |


### 5.3. 開発用の依存関係
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


#### 5.3.1. 開発ツール
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


### 5.4. OpenSpec
`OpenSpec` はプロジェクトローカルの開発用依存関係としてインストールしています。

```bash
npm install --save-dev @fission-ai/openspec@latest
```

`Codex`、`GitHub Copilot`、`Claude Code` 向けに `OpenSpec` を初期化しています。

```bash
npx openspec init --tools codex,github-copilot,claude
```

`OpenSpec` の拡張機能を有効にします。

```bash
npx openspec config profile

> workflows only

? Select workdlows to make available:
[x] New change
[x] Fast-forword
[x] Verify change

? Apply chamges to this project now?
Y
```

## 6. プロジェクト構成
```text
python-template/
├── .agents/              # AI エージェント用スキル
├── .claude/              # Claude Code
├── .github/              # GitHub Copilot
├── openspec/             # OpenSpec specifications
│
├── scripts/              # リポジトリ運用・OpenSpec検査スクリプト
│
├── src/
│   └── app/
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


## 7. 依存関係の管理
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
