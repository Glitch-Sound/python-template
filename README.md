# Python Template

## Quick Start

アプリケーション実行.
```bash
uv run python-template
```


## Pre-configured

プロジェクト作成
```bash
uv init python-template --name python_template --app --python "==3.13"
```

本番環境向け
```bash
uv add typer loguru pydantic-settings
```

開発環境向け
```bash
uv add --dev pytest pytest-mock ruff
```

OpenSpec導入
```bash
npm install --save-dev @fission-ai/openspec@latest
npx openspec init --tools codex,github-copilot,claude
```

