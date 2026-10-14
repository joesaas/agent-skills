#!/usr/bin/env python3
"""Portable uploader for the DocReader document center (agent101.uk).

This variant is for agents that do not run inside Muse's connector /
Sentinel environment. Authentication is deliberately environment-only:

  DOC_READER_API_KEY  required when --yes is used
  DOC_READER_BASE     optional, default https://agent101.uk

Without --yes the script only prints a summary and exits (dry run).
--yes must be passed ONLY after the user has explicitly confirmed the
upload of the exact document, title and category being sent.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

# Cloudflare's bot filter 403s script-default user agents (verified
# 2026-10-10: python-urllib UA got 403, browser UA got 201).
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")
CATEGORIES = {"agent", "defi", "blockchain", "protocol", "security",
              "network", "engineering", "other"}


def main() -> int:
    ap = argparse.ArgumentParser(description="Upload an HTML doc to DocReader")
    ap.add_argument("--title", required=True)
    ap.add_argument("--category", default="other", choices=sorted(CATEGORIES))
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
        print("DRY RUN - not uploaded. Pass --yes only after user confirmation.")
        return 0

    key = os.environ.get("DOC_READER_API_KEY")
    if not key:
        print("UPLOAD FAILED: DOC_READER_API_KEY is not set", file=sys.stderr)
        return 2

    payload = {"title": args.title, "html": html, "category": args.category}
    if args.external_id:
        payload["externalId"] = args.external_id
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json", "User-Agent": BROWSER_UA,
               "X-API-Key": key}
    req = urllib.request.Request(f"{base}/api/ai/docs", data=data,
                                 headers=headers, method="POST")
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
