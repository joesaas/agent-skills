# agent-skills

A growing collection of reusable AI-agent skills. Skills are **not** copied as one generic folder: each skill is packaged per agent runtime, because discovery paths, metadata files, path variables, and secret injection differ by agent.

## Repository layout

```text
skills/
  <canonical-skill-name>/
    README.md                 # what the skill does + variant index
    shared/                   # runtime-neutral reference implementation, when useful
    variants/
      muse/<package-name>/    # Muse package; package name gets the -muse suffix
      claude-code/<package-name>/
      codex/<package-name>/   # may add agents/openai.yaml
      openclaw/<package-name>/
      generic/<package-name>/
docs/
  format-matrix.md            # the per-agent packaging differences
catalog.json                  # machine-readable skill index
scripts/
  validate_skills.py          # structural checks for the collection
```

## Naming rule

- The canonical skill name is the directory under `skills/` (example: `doc-reader-upload`).
- A runtime package may adjust the package name for that runtime.
- **Muse packages always use the `-muse` suffix** (example: `doc-reader-upload-muse`).
- Other runtimes keep the canonical package name unless their format requires otherwise.

## Skills

| Skill | Purpose | Variants |
|---|---|---|
| [`doc-reader-upload`](skills/doc-reader-upload/README.md) | Publish confirmed HTML research documents to DocReader / Agent 101 | Muse, Claude Code, Codex, OpenClaw, Generic |

## Installing a skill

Open the variant folder for your agent and follow its `INSTALL.md`. Never install the `muse` variant into another runtime and expect Muse connector authentication to travel with it — credentials are configured per environment, never stored in this repository.

## Adding a new skill

1. Create `skills/<canonical-name>/` with a `README.md` and a `variants/` tree.
2. Make every variant self-contained: instructions + scripts + runtime metadata.
3. Personalize the format, install path, path variables, invocation, and secret injection for each runtime; do not just rename folders.
4. Add the skill to `catalog.json`.
5. Run `python3 scripts/validate_skills.py`.
