---
name: doc-reader-upload
description: Use when the user asks Claude Code to research, analyze, summarize, or learn a topic and publish the resulting HTML document to the DocReader document center at agent101.uk, or when the user explicitly asks to upload a document to DocReader/Agent 101. Always obtain confirmation for the exact document before uploading.
---

# DocReader Upload for Claude Code

Install this folder as a folder skill: `~/.claude/skills/doc-reader-upload/SKILL.md` for personal use, or `<project>/.claude/skills/doc-reader-upload/SKILL.md` for one project. Supporting files must stay inside the same folder.

Authentication is environment-only. Before an actual upload, `DOC_READER_API_KEY` must be present in Claude Code's environment (for example through the user's shell or settings `env`, managed outside this repository). `DOC_READER_BASE` is optional and defaults to `https://agent101.uk`.

Run the bundled script by resolving its path relative to this `SKILL.md`'s folder; do not assume the repository checkout path is the installed path.

## Workflow

1. 先把调研/分析内容做成一个独立 HTML 文件。Use the HTML artifact already produced in the current Claude Code workflow; install answer-me-with-html separately if that exact renderer is desired.
2. 按文档主体选择一个类目：

| 类目 | 放什么 |
|---|---|
| `agent` | AI Agent、A2A、agent 产品与框架 |
| `defi` | DeFi 协议、LP、借贷、收益与金库 |
| `protocol` | 协议设计：支付协议、通信协议、授权协议 |
| `blockchain` | 公链、扩容、链上基础设施 |
| `security` | 攻击事件复盘、安全机制、认证授权攻防 |
| `network` | TCP/HTTP/WebSocket 等网络基础 |
| `engineering` | 软件工程、架构、开发实践 |
| `other` | 以上都不贴切 |

3. 先 dry run，只打印标题、类目、大小和目标地址，不上传：

```bash
python3 <this-skill-folder>/bin/upload_doc.py --title "<标题>" --category <类目> --html-file <HTML路径>
```

4. 把标题和类目展示给用户，等待用户对这一篇文档明确确认。
5. 只有确认后才加 `--yes` 真正上传：

```bash
python3 <this-skill-folder>/bin/upload_doc.py --title "<标题>" --category <类目> --html-file <HTML路径> --yes
```

6. 更新已发布文档时，加 `--external-id <稳定ID>`；服务端会按 externalId 替换，不会另建一篇。
7. 回报 `created` / `replaced` / `deduped`、文档 ID 和阅读链接 `https://agent101.uk/#/doc/<id>`。

## Hard rules

- 没有用户对当前文档的明确确认，绝不传 `--yes`。确认过上一篇不等于确认这一篇。
- 标题、内容或类目发生变化，必须重新确认。
- 不要绕过脚本用裸 curl/urllib 上传：服务端前面的 Cloudflare 会拦截脚本默认 UA，脚本已内置浏览器 UA。
- 不要把 API Key 写进 skill、脚本、仓库、聊天记录或命令参数。
- 上传失败时原样报告 HTTP 状态和服务端错误，不要无上限重试。
