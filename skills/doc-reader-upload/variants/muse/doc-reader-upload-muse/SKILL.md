---
name: "doc-reader-upload-muse"
description: "Muse 专用：调研/分析/总结/学习类内容先用 answer-me-with-html 生成 HTML，再经用户确认上传到 DocReader 文档中心（agent101.uk）。当用户在 Muse 中说调研、分析、总结、学习某个主题，或直接说上传到文档中心时使用。"
---

# DocReader Upload for Muse

这是 Muse 变体，包名按约定加 `-muse` 后缀。它使用 Muse 已连接的 `custom.agent101` 连接器：脚本向本机 authd 申请 `hsurr:` 替身并以 `X-API-Key` 附带，Sentinel 只在网络出口把替身换成真 Key。不要把真 Key 写进文件、环境变量或聊天；连接器不可用时，脚本才回退 `DOC_READER_API_KEY`。

安装位置：`~/workspace/skills/doc-reader-upload-muse/`

配套：成文阶段使用 Muse 环境中的 `answer-me-with-html` skill。

## Workflow

1. 先把调研/分析内容做成一个独立 HTML 文件。在 Muse 中优先使用 answer-me-with-html 的渲染结果。
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
python3 ~/workspace/skills/doc-reader-upload-muse/bin/upload_doc.py --title "<标题>" --category <类目> --html-file <HTML路径>
```

4. 把标题和类目展示给用户，等待用户对这一篇文档明确确认。
5. 只有确认后才加 `--yes` 真正上传：

```bash
python3 ~/workspace/skills/doc-reader-upload-muse/bin/upload_doc.py --title "<标题>" --category <类目> --html-file <HTML路径> --yes
```

6. 更新已发布文档时，加 `--external-id <稳定ID>`；服务端会按 externalId 替换，不会另建一篇。
7. 回报 `created` / `replaced` / `deduped`、文档 ID 和阅读链接 `https://agent101.uk/#/doc/<id>`。

## Hard rules

- 没有用户对当前文档的明确确认，绝不传 `--yes`。确认过上一篇不等于确认这一篇。
- 标题、内容或类目发生变化，必须重新确认。
- 不要绕过脚本用裸 curl/urllib 上传：服务端前面的 Cloudflare 会拦截脚本默认 UA，脚本已内置浏览器 UA。
- 不要把 API Key 写进 skill、脚本、仓库、聊天记录或命令参数。
- 上传失败时原样报告 HTTP 状态和服务端错误，不要无上限重试。
