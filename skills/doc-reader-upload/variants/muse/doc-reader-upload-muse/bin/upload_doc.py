#!/usr/bin/env python3
"""Upload one HTML document to the user's DocReader 文档中心 (agent101.uk).

Usage:
  upload_doc.py --title "标题" --category agent --html-file page.html --yes

Without --yes the script only prints a summary and exits (dry run).
--yes must be passed ONLY after the user has explicitly confirmed the upload.
API key: taken from the connected custom.agent101 credential (an hsurr:*
surrogate is attached as X-API-Key and Sentinel swaps in the real key on
egress). Falls back to env DOC_READER_API_KEY when the connector is absent.
Base URL: env DOC_READER_BASE, default https://agent101.uk
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")

# Cloudflare's bot filter 403s script-default user agents (verified 2026-10-10:
# python-urllib UA got 403, browser UA got 201). Always send a browser UA.
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def main() -> int:
    ap = argparse.ArgumentParser(description="Upload an HTML doc to DocReader")
    ap.add_argument("--title", required=True)
    ap.add_argument("--category", default="other",
                    help="agent|defi|blockchain|protocol|security|network|engineering|other")
    ap.add_argument("--html-file", required=True, help="path to a standalone HTML file")
    ap.add_argument("--external-id", default=None,
                    help="optional stable id; re-uploading with the same id replaces the doc")
    ap.add_argument("--yes", action="store_true",
                    help="actually upload; without it, dry-run only")
    args = ap.parse_args()

    html = open(args.html_file, encoding="utf-8").read()
    base = os.environ.get("DOC_READER_BASE", "https://agent101.uk").rstrip("/")

    print(f"title:    {args.title}")
    print(f"category: {args.category}")
    print(f"size:     {len(html.encode('utf-8'))} bytes")
    print(f"target:   {base}/api/ai/docs")
    if not args.yes:
        print("DRY RUN — not uploaded. Pass --yes only after user confirmation.")
        return 0

    payload = {"title": args.title, "html": html, "category": args.category}
    if args.external_id:
        payload["externalId"] = args.external_id
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    headers = {"Content-Type": "application/json", "User-Agent": BROWSER_UA}
    req = urllib.request.Request(f"{base}/api/ai/docs", data=data,
                                 headers=headers, method="POST")
    # Preferred auth: the custom.agent101 connector's surrogate credential.
    host = urllib.parse.urlparse(base).hostname or ""
    attached = False
    try:
        from dynamic_credentials import add_surrogate_to_request
        add_surrogate_to_request(req, "custom.agent101", allowed_hosts=[host])
        attached = True
    except Exception as exc:
        print(f"note: connector credential not attached ({exc}); "
              "falling back to DOC_READER_API_KEY env", file=sys.stderr)
    if not attached:
        key = os.environ.get("DOC_READER_API_KEY")
        if key:
            req.add_header("X-API-Key", key)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"UPLOAD FAILED: HTTP {e.code} {e.read().decode('utf-8', 'replace')[:300]}",
              file=sys.stderr)
        return 1

    doc = body.get("doc", {})
    print(json.dumps({"status": body.get("status"), "id": doc.get("id"),
                      "title": doc.get("title"), "category": doc.get("category"),
                      "read": f"{base}/#/doc/{doc.get('id')}"},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
