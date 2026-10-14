# Install — OpenClaw

```bash
cp -R doc-reader-upload <openclaw-workspace>/skills/
```

Configure the key in `~/.openclaw/openclaw.json` (keep the real value out of git):

```json5
{
  skills: {
    entries: {
      "doc-reader-upload": {
        enabled: true,
        env: {
          DOC_READER_API_KEY: "<inject from your secret store>",
          DOC_READER_BASE: "https://agent101.uk"
        }
      }
    }
  }
}
```

OpenClaw injects `skills.entries.*.env` into the host process for the agent turn. Start a new session after installing so the skill is discovered.
