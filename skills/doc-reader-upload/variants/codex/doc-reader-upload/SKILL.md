---
name: doc-reader-upload
description: Research, analyze, summarize, or learn a topic, produce an HTML document, and publish it to the DocReader document center at agent101.uk after explicit user confirmation. Use when the user asks to upload a document to DocReader or Agent 101.
---

# DocReader Upload for Codex

Install under `$CODEX_HOME/skills/doc-reader-upload/`; when `CODEX_HOME` is unset, use `~/.codex/skills/doc-reader-upload/`. The `agents/openai.yaml` file in this package carries Codex/OpenAI UI metadata and is part of the package, not an optional decoration.

Authentication is environment-only: expose `DOC_READER_API_KEY` to the Codex process through the host's secret management. Optional `DOC_READER_BASE` defaults to `https://agent101.uk`.

Resolve `bin/upload_doc.py` relative to this skill folder.

## Workflow

1. 先把调研/分析内容做成一个独立 HTML 文件。Use the HTML file produced by the current Codex workflow.
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
