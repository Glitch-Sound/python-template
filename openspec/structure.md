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
- 公開CLIやライブラリの入口はプロジェクト設定で定義し、業務処理は仕様・機能上の責務ごとに分ける。
- OpenSpecの仕様は「何を満たすか」、設計は「どのように満たすか」、タスクは「どの順で実装・検証するか」を扱う。
- 進行中の変更は `openspec/changes/<change-id>/`、正式仕様は `openspec/specs/<capability-path>/spec.md` に置く。

## アプリケーションの責務と配置

新規プロジェクトでは、仕様、入出力、変更理由、既存の依存関係を先に確認し、独立して変更・検証しやすい責務を見つける。責務が明確になった時点で `src/app/<capability>/` を作り、その能力に属するCLI入口と処理をまとめる。小規模なうちは `src/app/` にまとめてよく、不要な階層や空の能力別パッケージを先に作らない。

- 複数の能力で実際に共有する設定、入出力契約、パス、実行基盤などだけを `src/app/common/` に置く。再利用できそうという予想だけで共通化しない。用途の曖昧な `utils.py` や、責務を見失うほど細かいファイル分割を避ける。
- 能力間の直接importは原則避け、受け渡す型、保存形式、パスなどの契約を明示する。`common/` は個別の能力に依存させない。直接依存が必要な例外は、理由と依存方向を構成文書または設計に記録する。
- 能力とパッケージの対応、共有契約、依存方向、ファイル配置の判断基準をプロジェクトの構成文書に記録し、仕様や責務から実装場所を探せるようにする。CLI、設定、成果物の保存先、境界を守るテストも対応付ける。
- OpenSpecのcapabilityとPythonパッケージは同じ数・名前に揃える規則ではない。仕様の責務と実装の変更境界を照合し、対応を文書化する。

次は構成を考えるための**仮の例**である。`input_handling` と `result_delivery` は全プロジェクトに必要な能力名ではなく、フォルダ数も案件ごとに決める。ファイル名や分割の粒度も、実際の責務に合わせる。

```text
src/app/
├── __init__.py              # 公開入口が必要ならここで公開する
├── input_handling/           # 仮の能力: 入力を受け取る責務
│   ├── cli.py               # この能力のCLI入口
│   └── processing.py        # この能力の処理
├── result_delivery/          # 仮の能力: 結果を渡す責務
│   ├── cli.py
│   └── processing.py
└── common/                   # 両能力で実際に共有する契約や基盤だけ
    ├── contracts.py
    └── settings.py
```

構成を決める際は、次を短く確認する。

1. **責務の境界**: どの仕様・入出力・変更理由を一つの能力にまとめるか。
2. **共有する契約**: 複数能力が使う型、保存形式、パス、設定は何か。
3. **依存方向**: 能力間の受け渡しと `common/` への依存をどう示すか。例外の理由は何か。
4. **CLI・設定・成果物への影響**: 公開入口、設定値、保存先をどこで扱うか。
5. **テストで守る境界**: 各能力と共有契約のどの振る舞いを検証するか。

このテンプレート自体はサンプルの `src/app/__init__.py` に公開入口 `app:main` を置き、`tests/test_app.py` で確認する。能力別の責務や実際の共有契約がまだないため、例の階層は作成していない。

## 複数 capability の構成

change は一回の変更計画、capability は継続管理する規範的な能力であり、一つのchangeで複数capabilityを追加・変更できる。分割は主な観測結果、責務、入出力、独立した変更・検証の境界を基準にする。実装ファイルや処理順だけを理由に分割しない。

例えばデータ処理を次の境界で管理できる。

| Capability | 主な入力 | 観測できる結果 | 独立した検証対象 |
| --- | --- | --- | --- |
| `data-processing/input-preparation` | 元データと準備条件 | 後続処理で使える入力と除外理由 | 入力検証、準備結果、元データの保持 |
| `data-processing/processing` | 準備済み入力と処理条件 | 再現可能な処理結果 | 処理規則、失敗時の状態、再実行 |
| `data-processing/result-reporting` | 処理結果 | 利用者が判断できる報告 | 表示・保存契約、未処理の扱い |

各パスの `spec.md` が一つのcapabilityである。親の `data-processing/` は名前空間であり、親仕様は自動生成されない。`data-processing/spec.md` を追加すれば独立した第4のcapabilityになるため、目次として作らない。

複数仕様を束ねる `openspec/specs/data-processing/README.md` は、次の内容を持つ非規範的な案内文書として作成する。

- 各capabilityの正式仕様へのリンクと提供する能力
- 分割理由と、入力・出力・検証対象の比較
- 仕様間で引き渡す入力・結果と、処理全体の関係
- 横断要件の正本と適用範囲、新しい要件の配置基準
- 利用手順や導入時のchangeへのリンク

同じ横断要件を複数の `spec.md` に複写しない。主な観測結果と責務を持つcapabilityへ置き、適用される処理と他仕様の入力・出力契約を説明する。独立した能力として管理する必要が生じた場合だけ、新しいcapabilityを検討する。案内文書には要件の正本が各 `spec.md` であることを明記し、既存仕様と異なる規範的な条件を追加しない。

## 命名規則

| 対象 | 規則 | 例 |
| --- | --- | --- |
| Pythonパッケージ・モジュール | 小文字の `snake_case` | `app_core`, `settings.py` |
| Python関数・変数 | `snake_case` | `load_settings` |
| Pythonクラス・型 | `PascalCase` | `AppSettings` |
| pytestファイル・関数 | `test_` 接頭辞 + `snake_case` | `test_feature_returns_result` |
| OpenSpec change / capability | `kebab-case` | `add-export`, `identity/user-auth` |
