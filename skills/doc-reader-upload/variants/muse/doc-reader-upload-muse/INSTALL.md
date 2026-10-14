# Install — Muse

```bash
cp -R doc-reader-upload-muse ~/workspace/skills/
python3 ~/workspace/skills/doc-reader-upload-muse/bin/upload_doc.py --help
```

前置条件：Muse 中已连接 `custom.agent101` 连接器。若连接器不可用，可临时设置 `DOC_READER_API_KEY` 作为回退；不要把真 Key 写入仓库文件。
