# GitHub Copilot 向け指示

このリポジトリは Python / OpenSpec 開発テンプレートです。作業前に `README.md`、`openspec/product.md`、`openspec/tech.md`、`openspec/structure.md`、および [AGENTS.md](../AGENTS.md) を確認してください。

共通の開発方針と完了条件は `AGENTS.md` を正本とします。雛形・開発基盤の保守、既存仕様の振る舞いを変えないリファクタリング、テストのみの修正は直接変更できます。利用者または外部システムから観測できる振る舞い、公開 API、永続データ、権限・セキュリティ、性能目標、外部連携、移行・運用手順を変える場合は、実装前に OpenSpec change を作成し、その成果物に従ってください。

変更後は `AGENTS.md` に定めた検査を実行し、秘密情報をコード、仕様、ログ、テストデータに含めないでください。
