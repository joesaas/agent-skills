# Install — Generic Agent

1. Copy this folder into the host agent's tool/plugin directory.
2. Register `bin/upload_doc.py` using `tool.json` as the tool contract, or expose it as a shell command.
3. Inject `DOC_READER_API_KEY` from the host secret manager at runtime.
4. Preserve the confirmation gate: first run without `--yes`, show title + category, and only run with `--yes` after the user confirms that exact document.
