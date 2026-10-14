# doc-reader-upload

把调研、分析、总结或学习成果做成 HTML 后，经用户确认，发布到 DocReader / Agent 101 文档中心（https://agent101.uk）。

这不是一个“一份文件打天下”的 skill。不同 Agent 的发现路径、目录约定、变量展开和密钥注入方式不同，所以本目录按运行时拆成自包含变体：

| 变体 | 包名 | 鉴权 | 适用 |
|---|---|---|---|
| Muse | `doc-reader-upload-muse` | `custom.agent101` 连接器 + Sentinel 替身 | 当前 Muse 环境 |
| Claude Code | `doc-reader-upload` | `DOC_READER_API_KEY` 环境变量 | `~/.claude/skills` 或项目 `.claude/skills` |
| Codex | `doc-reader-upload` | `DOC_READER_API_KEY` 环境变量 | `$CODEX_HOME/skills`，附 `agents/openai.yaml` |
| OpenClaw | `doc-reader-upload` | OpenClaw `skills.entries` 注入 env / apiKey | workspace `skills/`，使用 `{baseDir}` |
| Generic | `doc-reader-upload` | 宿主 secret manager 注入环境变量 | 无 SKILL.md 标准的自建 Agent |

`shared/upload_doc.py` 是非 Muse 变体共用的便携脚本副本；每个变体目录内也各带一份，安装时不需要跨目录引用。
