# Python Template
`uv` と `OpenSpec` を使用した `Python` 開発用テンプレートです。


## 1. 開発環境
- `Python` 3.13
- `uv`
- `OpenSpec`


### 1.1. 対応 AI コーディングエージェント
- `OpenAI Codex`
- `Claude Code`
- `GitHub Copilot`


## 2. クイックスタート
依存関係をインストールします。

```bash
uv sync --locked
npm ci
```

### Dev Container (任意)

Docker で開発したい場合は、Docker Engine と Dev Containers に対応したエディターを用意し、このリポジトリをコンテナで再度開いてください。<br />
VS Code では Dev Containers 拡張機能の **Reopen in Container** を使用します。

コンテナには Python 3.13、`uv`、Node.js 22 が含まれ、作成時に `uv sync --locked` と `npm ci` が実行されます。<br />
`.venv`、`node_modules`、パッケージキャッシュは Docker ボリュームに分離されるため、ホストの依存関係やOS固有のバイナリとは混在しません。<br />
依存関係を変更した場合は、コンテナ内で通常どおり次を実行してください。<br />

```bash
uv sync --locked
npm ci
```

### OpenSpec 更新 (任意)

OpenSpec を更新する場合は、先にプロジェクトローカルの CLI とロックファイルを更新してから、生成済みの agent 用 instructions を更新します。<br />
CLI を更新せずに `openspec update` だけを実行しても、新しいワークフローは導入されません。<br />
`.agents/` と `.claude/` の instruction は OpenSpec が対象エージェント向けに生成する成果物であり、手作業で片方だけを変更しません。<br />
生成差分をレビューしたうえで次を実行します。

```bash
npm install --save-dev @fission-ai/openspec@latest
npx --no-install openspec update
```

アプリケーションを実行します。

```bash
uv run python-template
```

### よく使う用語

このテンプレートの文書で使う言葉です。<br />
派生プロジェクトでは、案件固有の言葉に置き換え、必要な語を追加してください。

| 用語 | 意味 |
| --- | --- |
| OpenSpec change | 一回の変更を計画・実装・検証するための成果物一式。継続して管理する能力とは別の単位 |
| capability (仕様上の能力) | 利用者や外部システムに提供する、継続管理する機能・責務の単位。正式仕様は `openspec/specs/<capability-path>/spec.md` に置く |
| 能力別パッケージ | 変更・検証の境界に合わせて作る `src/app/<capability>/`。仕様上のcapabilityと同じ数・名前にする必要はない |
| 共有契約 | 複数の能力の間で受け渡す型、保存形式、パスなどの取り決め |
| 受け入れ条件 | 変更が利用者・運用者の目的を満たしたと判断する条件。proposalでは `AC-001` 形式のIDを付ける |
| 証跡 | 受け入れ条件を確認した手順、環境、結果を後から確かめられる記録 |

### 派生プロジェクトを作成した後

テンプレートから作成しただけでは、配布名や CLI は `python-template` のままです。<br />
開発開始時に次の項目を見直してください。

| 対象 | 見直す内容 |
| --- | --- |
| `pyproject.toml` の `[project]` | `name`、`description`、`authors`、開始時の `version` をプロジェクトに合わせる |
| `[project.scripts]` | CLI の名前と呼び出し先を定め、不要な `python-template = "app:main"` を削除または置換する |
| `src/app/` と `[tool.uv.build-backend]` | パッケージ名を変更する場合は配置と `module-name` を同時に更新し、CLI の参照先とテストの import も合わせる。配布名だけを変更するなら `app` を維持してよい |
| `tests/test_app.py` | 挨拶表示の雛形テストを、変更した入口の期待結果に更新する |
| `README.md` と `.devcontainer/devcontainer.json` | プロジェクト名、起動コマンド、コンテナ名・ボリューム名に残るテンプレート固有名を見直す |
| `README.md` の用語集 | 利用者・開発者・運用者が使う案件固有の用語、略語、同義語を定義し、既存の定義を案件の意味に合わせて見直す |
| OpenSpec の共通文書 | テンプレート基盤の説明と実際のコード・設定の一致を確認する。案件固有の業務要件は change に記載する |

派生プロジェクトでは、初めて参加する人が読む `README.md` に短い用語集を置きます。<br />
長くなる場合は別の文書に分け、READMEからリンクしてください。<br />
用語を新しく使うときや意味を変えるときは定義も更新し、コード・CLI・仕様と呼び方を揃えます。<br />
用語集は理解の入口とし、振る舞いや受け入れ条件の正本は該当する仕様・changeに置きます。

`src/app/` の構成は、仕様、入出力、変更理由、依存関係から責務を見つけてから決めます。<br />
独立して変更・検証する能力が明確なら `src/app/<capability>/` に関連するCLI入口と処理をまとめ、複数能力で実際に共有する契約や基盤だけを `src/app/common/` に置きます。<br />
小規模なうちは分割を強制しません。<br />
能力とパッケージの対応、依存方向、配置の判断基準、確認項目と仮の構成例は [アプリケーションの責務と配置](openspec/structure.md#アプリケーションの責務と配置) を参照してください。

例えば配布名・CLI 名を `my-project` とし、Python パッケージ `app` を維持する場合は、次のように設定します。

```toml
[project]
name = "my-project"
# その他の既存設定は維持し、description 等をプロジェクトに合わせる

[project.scripts]
my-project = "app:main"
```

名前や設定を変更したら、ロックファイルを手編集せず、更新・同期して新しい CLI を起動します。

```bash
uv lock
uv sync --locked
npm ci
uv run --locked my-project
uv run --locked pytest
npm run check
```

旧 CLI 名や `python_template` の参照が残っていないか検索し、由来の説明など意図的に残す箇所を確認してください。

## 3. 開発

### 3.1. 文書の書き方

READMEなどの日本語の案内文書では、本文に複数の文を書くとき、原則として文末の句点の直後で改行します。<br />
同じ段落を続ける場合は、この段落のように `。<br />` と改行を使い、段落を分ける場合は空行を入れます。<br />
表のセル、コードブロック、見出しなど、改行で読みづらくなる箇所は例外です。<br />
括弧は半角の `(` と `)` を使います。<br />
派生プロジェクトでもこの書き方をREADMEと案内文書に引き継いでください。

コミット前には高速な基礎検査を実行します。<br />
初回だけフックを有効化してください。

```bash
uv run --locked pre-commit install
uv run --locked pre-commit run --all-files
```

統合前、または雛形の広範な変更後は、完全な品質検査を実行します。

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

コミットを速く保つため、型検査、全テスト、OpenSpec のトレーサビリティは `npm run check` にまとめています。

### 3.2. AI コーディングエージェントの指示

共通の開発方針は [AGENTS.md](AGENTS.md) を正本とし、OpenAI Codex、Claude Code、GitHub Copilot から参照します。<br />
GitHub Copilot はリポジトリ共通の [`.github/copilot-instructions.md`](.github/copilot-instructions.md) も読み込みます。<br />
雛形・文書・振る舞いを変えない保守は直接変更できます。<br />
一方、外部から観測できる振る舞い、API、データ、セキュリティ、性能、外部連携、移行・運用を変える作業は OpenSpec change を先に作成します。<br />
曖昧な場合は要件を作り出さず、利用者に確認してください。


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
どのように進めていくか、チャットベースで相談してください。
```text
$openspec-explore [テーマ]
```


#### 4.2.2. 作業ディレクトリ生成
`openspec/config.yaml` の `schema: my-workflow` を既定スキーマとして、`openspec/changes/変更名/` が生成されます。<br />
各 change の `.openspec.yaml` に使用スキーマが記録されるため、以後の成果物生成・実装・検証でも同じワークフローが使用されます。
```text
$openspec-new-change [変更名]
```

**change と capability は別の単位です。**<br />
change は一回の変更計画、capability は正式仕様として継続管理する能力です。<br />
一つの change で複数 capability を追加・変更できます。

capability は主な観測結果、責務、入出力、検証対象を基準に分けます。<br />
処理の順番や実装モジュールごとに機械的に分割せず、独立して変更・レビューできる境界を選んでください。<br />
同じ横断要件を複数仕様へ複写せず、主な責務を持つ仕様を正本として、適用範囲と他仕様との関係を明記します。

`openspec/specs/<capability-path>/spec.md` が一つの capability です。<br />
`data-processing/` の下に複数仕様を置いても、親の `data-processing/spec.md` は自動生成されません。<br />
全体案内は非規範的な `README.md` として作成し、子仕様へのリンク、分割理由、入出力、横断要件の正本を説明してください。<br />
詳しい配置基準と構成例は [プロジェクト構成](openspec/structure.md#複数-capability-の構成) を参照してください。


#### 4.2.3. 補足資料を用意 (任意)
要件定義書、既存設計、調査結果などの補足資料がある場合は、`openspec/changes/変更名/input.md` に格納できます。<br />
`input.md` は OpenSpec が自動で読み込むファイルではないため、次の工程で「`input.md` を参照する」と明示して使用してください。

`input.md` は、実装案より先に、利用者と運用者が何を達成・判断するかを整理する資料として作成します。<br />
次の順序が推奨例です。

1. **目的と利用者**: 解決したい問題、結果を使う人、運用する人、外部システムとそれぞれの判断を記載します。
2. **現行・変更後の業務フロー**: 開始条件から完了までの操作、判断、引き継ぎを時系列で記載します。
3. **判定や処理結果の扱い**: 利用者が受け取る結果、保存・通知、次に可能な操作、後続業務への引き継ぎを記載します。
4. **例外時の運用**: 入力不備、処理失敗、未判定、再実行など、該当する事象の表示・状態・復旧・責任分界を記載します。
5. **品質目標と受け入れ条件**: 実際の運用で必要な精度、性能、可用性、安全性と、運用開始を判定する条件を記載します。
6. **データ・環境上の制約**: 利用可能なデータ、入出力形式、実行環境、外部連携、セキュリティや運用時間の制約を記載します。
7. **技術候補・参考資料**: 検討済みの方式、ディレクトリ構成例、設定例、既存設計、調査結果を、事実・制約・候補に分けて記載します。

案件に該当しない項目は、理由を示して省略できます。<br />
特に品質目標の数値、閾値、承認者、例外時の責任分界が未確認な場合は推測で埋めず、「未決」と影響する工程を明記します。<br />
技術候補、ディレクトリ構成例、設定例を含めても構いませんが、それらは design で根拠を確認する候補であり、未確認の業務要件または採用済みの実装方式として確定しません。


#### 4.2.4. ドキュメント生成
変更内容と、明示的に参照を依頼した `input.md` を基に、実装に必要なドキュメントを生成します。
```text
$openspec-ff-change [変更名] input.md を要件の入力資料として参照し、既存の仕様・コード・設定と照合して、実装開始に必要な成果物を生成してください。
矛盾や実装可否を左右する未決事項は推測せず明示してください。
```

通常の開発では、`openspec-ff-change` で proposal、specs、design、tasks を依存関係順に一括生成する方法を既定とします。<br />
一括生成は上流工程やレビューを省略するものではなく、成果物ごとの対話・待ち時間を減らすために使用します。

生成後は proposal → specs → design → tasks の順に内容をレビューします。<br />
上流の前提や要件を修正する場合は、`openspec-update-change` を使って下流の設計・タスクとの整合性も更新します。<br />
未解決の重要事項を残したまま実装へ進みません。

次のように変更の前提や影響が不明確な場合は、一括生成の前に `openspec-explore` で調査・検討します。

- 利用者、運用者、変更後の業務フロー、受け入れ条件が定まっていない。
- 外部 API、権限・セキュリティ、不可逆なデータ移行など、失敗時の影響が大きい。
- 技術候補によって実現できる要件・運用フローが大きく変わる、または既存仕様と `input.md` に矛盾がある。

生成される成果物では、次の対応関係を管理します。

| 成果物 | 記載する内容 |
| --- | --- |
| `proposal.md` | 目的、利用者・運用者、現行・変更後の業務フロー、対象・対象外、`AC-001` 形式のIDを付けた運用開始の受け入れ条件 |
| `spec.md` | 利用者または外部システムから観測できる要件とScenario、試験方針、要件に影響する未決事項 |
| `design.md` | 業務フローを満たす責務、データ契約、失敗時の結果、技術判断、Scenarioごとの試験ケースID (`TC-001`) と確定後のpytest実装先、検証範囲・残る検証・証跡、全受け入れ条件の検証記録 |
| `tasks.md` | 確定した設計から展開した実施作業と完了条件、要件ID・Scenario ID・TC-IDとの対応 |

実装変更を伴う `Scenario` には、自動テストコードを作成します。<br />
文書のみの変更など、テストコードが不要な場合は、`design.md` の「試験例外」に理由、承認者、期限を記録します。

成果物の対応は工程に応じて次のコマンドで確認します。<br />
コミットごとには実行せず、設計レビュー、実装前、実装後、verify / archive 前、統合前に使用してください。

```bash
# 設計時: 対応と参照の書式を確認 (未作成テスト・未完了タスクは許容)
uv run --locked python scripts/check_openspec_traceability.py --change <change-name>

# 実装後: pytest による参照テストの収集可否も確認
uv run --locked python scripts/check_openspec_traceability.py --change <change-name> --phase implementation

# 通常の完了時: 全タスクと全受け入れ条件・証跡も確認
uv run --locked python scripts/check_openspec_traceability.py --change <change-name> --phase complete

# 制限付きアーカイブ時: 延期した受け入れ確認の引き継ぎも確認
uv run --locked python scripts/check_openspec_traceability.py --change <change-name> --phase limited-archive

# 進行中の全変更を確認 (npm run check にも含まれる)
uv run --locked python scripts/check_openspec_traceability.py --all --phase implementation
```

全工程で、REQ/NREQとScenarioの所属・重複、設計が参照する実在タスクと要件ID、全ScenarioとTC-ID、試験設計のID整合、pytest参照書式、全TC-IDのテスト作成タスクを検査します。<br />
試験設計は従来の8列と、検証範囲・残る検証・証跡を追加した11列の両方を読み取れます。

`implementation` と `complete` は、同じPython環境で `pytest --collect-only` を実行します。<br />
通常関数、パラメータ化関数、`tests/...py::TestExample::test_behavior` 形式のクラスメソッドを参照できます。<br />
テスト本体は実行しませんが、conftestやimportは実行します。<br />
収集できることと試験の成功は別に確認してください。

自動テストがテストダブルによる契約だけを確認している場合、その成功を全CLI・実ライブラリ・実機・対象OSの検証完了と扱いません。<br />
試験設計に確認範囲と残る検証を記載し、必要な実機スモークや運用確認を別タスクとして実施します。

受け入れ条件は proposal に `- AC-001: <条件>` の形式で記載し、design の「受け入れ検証」で全IDに次の6列を対応付けます。

| 受け入れID | 検証範囲・条件 | 検証方法 | 残る検証 | 状態 | 証跡 |
| --- | --- | --- | --- | --- | --- |
| AC-001 | 対象OS・実ライブラリで全CLIが完了する | 実機でスモークを実行 | 実機スモーク未実施 | 未検証 | 未作成 |

`complete` は全タスク完了、全AC-IDの状態「検証済み」、残る検証「なし」、リポジトリルート相対の空でない証跡ファイルを必須とします。<br />
証跡にコマンド・手順、実行日、環境・依存版、結果を残してください。<br />
検査は証跡の内容や検証範囲の十分性を保証しないため、レビュー時に内容を確認します。<br />
既存changeの完了検査には、このIDと表を補完します。

実機・対象OS等の環境を現時点で利用できず受け入れ確認だけが残る場合は、制限付きアーカイブを使用できます。<br />
実装・自動試験・品質確認は完了させ、延期する確認タスクだけを未完了のまま残します。<br />
この README の「延期中の受け入れ確認」に change 名、AC-ID、状態「未検証」、未完了タスク番号と確認内容を1行に記録します。<br />
延期するAC-IDは design の「受け入れ検証」でも「未検証」とし、「残る検証」に具体的な内容を残します。<br />
`archive-deferred.md`、実施責任者・再開条件、GitHub Issue や別の spec の作成は必須ではありません。

`limited-archive` は README の行と未完了タスク・AC-IDの対応、受け入れ状態、他タスクの完了、参照テストの収集を検査します。<br />
延期理由が本当に環境制約か、残る検証と証跡の内容が十分かは人がレビューします。<br />
延期は検証済み・運用開始承認を意味しません。


#### 4.2.5. ドキュメント改善
生成したドキュメントを壁打ちしながら品質を向上させます。
```text
$openspec-update-change [変更名] [修正内容]
```


#### 4.2.6. 実装
生成したドキュメントから実装を行います。
```text
$openspec-apply-change [変更名]
```


#### 4.2.7. 検証
実装内容が問題ないか検証します。
```text
$openspec-verify-change [変更名]
```

verify 前に通常は `--phase complete` を通し、受け入れ条件の証跡を確認します。<br />
実機検証などを延期する場合は `--phase limited-archive` を通し、残る検証と引き継ぎを確認します。


#### 4.2.8. 仕様反映
変更内容を正式仕様として反映します。
```text
$openspec-archive-change [変更名]
```

アーカイブ前には、OpenSpec の厳密検証と該当するトレーサビリティ検査の両方を通します。
```bash
npx --no-install openspec validate <change-name> --strict
uv run --locked python scripts/check_openspec_traceability.py --change <change-name> --phase complete
# 制限付きアーカイブの場合はこちらを実行
uv run --locked python scripts/check_openspec_traceability.py --change <change-name> --phase limited-archive
```

通常の完了検査が失敗した場合は、実機等の受け入れ検証だけが残るかを確認します。<br />
制限付きアーカイブでは README の延期行と残るリスクをレビューし、利用者の明示的な了承を得てからアーカイブします。<br />
実装・自動試験・品質確認の未完了や重要な未解決事項があれば進行中に残します。<br />
正式仕様への反映だけが必要なら `$openspec-sync-specs [変更名]` を使います。

通常の `--all` はアーカイブ済み変更を除外します。<br />
保存後の監査は明示して実行できます。

```bash
# 保存済みの一件を確認
uv run --locked python scripts/check_openspec_traceability.py --change archive/<保存名> --phase complete

# 制限付きで保存した一件を確認
uv run --locked python scripts/check_openspec_traceability.py --change archive/<保存名> --phase limited-archive

# 進行中と保存済みの全変更を確認
uv run --locked python scripts/check_openspec_traceability.py --all --include-archived --phase complete
```


#### 4.2.9. 最新仕様とソースコードの整合性確認
最後に、正式仕様である `openspec/specs/` の要件・Scenarioを `src/` の実装と `tests/` の検証内容に照らして確認します。<br />
仕様に対応する実装・テストの不足と、仕様に記載されていない外部から観測できる振る舞いを洗い出し、差異があれば該当ファイルと内容を記録して解消します。

```text
openspec/specs/ の最新仕様をすべて読み、各要件・Scenarioと src/ の実装、tests/ の検証内容を双方向に照合してください。
不足や矛盾があれば、仕様とコードの該当箇所を示して報告してください。
```


## 延期中の受け入れ確認

制限付きアーカイブ時に change 名、AC-ID、状態「未検証」、`タスクX.Y: <確認内容>` を追記します。<br />
検証後はこの行の状態と証跡を更新し、アーカイブ内の受け入れ検証記録にも結果を反映します。

| change | 受け入れID | 状態 | 記録 |
| --- | --- | --- | --- |


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
uv add --dev pre-commit pyright pyyaml pytest pytest-mock ruff
```

| パッケージ | 説明 |
| --- | --- |
| `pytest` | `Python` のテストフレームワークです。<br />シンプルな `assert` を使って単体テストや結合テストを記述できます。 |
| `pytest-mock` | `pytest` からモックを扱いやすくするプラグインです。<br />`mocker` フィクスチャを利用して、関数やオブジェクトの差し替え、呼び出し検証などを行えます。 |
| `PyYAML` | リポジトリ検査スクリプトで `YAML` 設定ファイルを検証します。 |
| `ruff` | 高速な `Python` リンター／フォーマッターです。<br />コード品質のチェックとコードフォーマットを担当します。 |
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

`Codex`、`Claude Code` 向けに `OpenSpec` を初期化しています。

```bash
npx --no-install openspec init --tools codex,claude
```

標準 profile に含まれないワークフロー (`new`、`continue`、`ff`、`verify`、`bulk-archive`、`onboard` など) が必要な場合は、profile で選択してから生成済み instruction を更新します。<br />
選択肢は OpenSpec のバージョンにより変わるため、対話プロンプトの表示例を固定せず、コマンドの案内に従って選択してください。

```bash
npx --no-install openspec config profile
npx --no-install openspec update
```

## 6. プロジェクト構成
```text
python-template/
├── .agents/              # AI エージェント用スキル
├── .claude/              # Claude Code
├── .gitignore             # Git の除外設定
├── .pre-commit-config.yaml # コミット時の基礎検査
├── openspec/             # OpenSpec specifications
│
├── scripts/              # リポジトリ運用・OpenSpec検査スクリプト
│
├── src/
│   └── app/                # 現在は __init__.py のサンプルCLIのみ
│
├── tests/
│
├── AGENTS.md              # AI 開発エージェントの共通指示
├── CLAUDE.md              # Claude Code 用の共通指示入口
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

ロックファイルに従って依存関係を同期します。

```bash
uv sync --locked
```

依存関係を追加・更新した後は、ロックファイルを更新してから同期します。

```bash
uv lock
uv sync --locked
```

`OpenSpec` を含む `Node.js` の依存関係を同期します。

```bash
npm ci
```
