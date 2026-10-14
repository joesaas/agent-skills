# Install — Codex

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R doc-reader-upload "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Provide `DOC_READER_API_KEY` through the environment or secret manager for the Codex process. Keep `agents/openai.yaml` inside the skill folder. Start a new Codex session if the skill list does not refresh.
