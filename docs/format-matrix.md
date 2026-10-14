# Per-agent format matrix

Why this repository ships variants instead of one folder:

| Runtime | Discovery / install location | Instruction file | Runtime-specific personalization in this repo |
|---|---|---|---|
| Muse | `~/workspace/skills/<package>/` | `SKILL.md` | Package name gets `-muse` suffix; auth via the connected `custom.agent101` connector (authd surrogate + Sentinel egress swap), env key only as fallback; writing step pairs with `answer-me-with-html` |
| Claude Code | `~/.claude/skills/<package>/` or `<project>/.claude/skills/<package>/` | `SKILL.md` inside a folder (a bare `.md` file is not a skill) | Folder-skill layout; script path resolved relative to the installed skill folder; API key supplied by the Claude Code process environment |
| Codex | `$CODEX_HOME/skills/<package>/` (default `~/.codex/skills/`) | `SKILL.md` + `agents/openai.yaml` | Adds OpenAI/Codex UI metadata (`display_name`, `short_description`, `default_prompt`) and implicit-invocation policy |
| OpenClaw | active workspace `skills/<package>/` (takes precedence) or `~/.openclaw/skills/<package>/` | `SKILL.md` | Frontmatter keys are single-line and `metadata` is a single-line JSON object; commands use `{baseDir}`; secrets injected via `skills.entries.<name>.env` / `apiKey` |
| Generic / self-built | host-defined tool or plugin directory | `AGENT_INSTRUCTIONS.md` + `tool.json` | No assumed skill loader: ships a tool contract with an explicit `yes` confirmation parameter and environment declaration |

Shared invariants across every variant:

- Dry run first; `--yes` only after the user confirms the exact document, title, and category.
- One category from the fixed DocReader category set.
- Browser User-Agent is mandatory (Cloudflare rejects script-default UAs).
- `--external-id` updates replace in place instead of creating duplicates.
- No real API keys in the repository.
