# Install — Claude Code

Personal install:

```bash
mkdir -p ~/.claude/skills
cp -R doc-reader-upload ~/.claude/skills/
```

Project install:

```bash
mkdir -p <project>/.claude/skills
cp -R doc-reader-upload <project>/.claude/skills/
```

Set `DOC_READER_API_KEY` in the environment that launches Claude Code, or in Claude Code settings managed outside this repo. Do not commit the key. Restart or reload Claude Code, then check that `doc-reader-upload` appears in the skills list.
