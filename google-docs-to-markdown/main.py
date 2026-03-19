#!/usr/bin/env venv/bin/python3
"""
Convert a Google Doc to Markdown.

Usage:
    python main.py <google-doc-url-or-id> [-o output.md]

Authentication:
    1. Go to https://console.cloud.google.com/
    2. Create a project, enable the Google Docs API
    3. Create OAuth 2.0 credentials (Desktop app), download as credentials.json
    4. Place credentials.json in this directory
    5. Run the script — a browser window will open to authorise access
    6. A token.json is saved for future runs (keep it secret)
"""

import os
import re
import argparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]

HEADING_PREFIX = {
    "HEADING_1": "# ",
    "HEADING_2": "## ",
    "HEADING_3": "### ",
    "HEADING_4": "#### ",
    "HEADING_5": "##### ",
    "HEADING_6": "###### ",
    "TITLE": "# ",
    "SUBTITLE": "## ",
}


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def get_credentials(credentials_file: str = "credentials.json", token_file: str = "token.json") -> Credentials:
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, "w") as fh:
            fh.write(creds.to_json())
    return creds


# ---------------------------------------------------------------------------
# Conversion helpers
# ---------------------------------------------------------------------------

def _text_run_to_md(text_run: dict) -> str:
    content = text_run.get("content", "")
    if content in ("\n", ""):
        return content

    style = text_run.get("textStyle", {})
    bold = style.get("bold", False)
    italic = style.get("italic", False)
    strikethrough = style.get("strikethrough", False)
    link = (style.get("link") or {}).get("url")

    # Pull off trailing newline so formatting markers wrap only the text
    trailing = "\n" if content.endswith("\n") else ""
    text = content.rstrip("\n")

    if not text:
        return trailing

    if link:
        text = f"[{text}]({link})"
    if bold and italic:
        text = f"***{text}***"
    elif bold:
        text = f"**{text}**"
    elif italic:
        text = f"*{text}*"
    if strikethrough:
        text = f"~~{text}~~"

    return text + trailing


def _paragraph_to_md(paragraph: dict, lists: dict) -> str:
    style_name = paragraph.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
    prefix = HEADING_PREFIX.get(style_name, "")

    # Build inline text from all elements
    parts = []
    for element in paragraph.get("elements", []):
        if "textRun" in element:
            parts.append(_text_run_to_md(element["textRun"]))
        elif "inlineObjectElement" in element:
            parts.append("![image]")
    text = "".join(parts).rstrip("\n")

    bullet = paragraph.get("bullet")
    if bullet:
        level = bullet.get("nestingLevel", 0)
        indent = "  " * level
        list_id = bullet.get("listId", "")
        marker = "-"
        if list_id in lists:
            nesting_levels = lists[list_id].get("listProperties", {}).get("nestingLevels", [])
            if level < len(nesting_levels):
                glyph_type = nesting_levels[level].get("glyphType", "BULLET")
                if glyph_type not in ("BULLET", ""):
                    marker = "1."
        return f"{indent}{marker} {text}"

    return prefix + text


def _table_to_md(table: dict, lists: dict) -> str:
    rows = table.get("tableRows", [])
    if not rows:
        return ""

    md_rows = []
    for i, row in enumerate(rows):
        cells = []
        for cell in row.get("tableCells", []):
            cell_lines = []
            for block in cell.get("content", []):
                if "paragraph" in block:
                    cell_lines.append(_paragraph_to_md(block["paragraph"], lists))
            cells.append(" ".join(cell_lines).strip())
        md_rows.append("| " + " | ".join(cells) + " |")
        if i == 0:
            md_rows.append("| " + " | ".join(["---"] * len(cells)) + " |")

    return "\n".join(md_rows)


def _content_to_md(content: list, lists: dict) -> str:
    blocks = []
    for element in content:
        if "paragraph" in element:
            md = _paragraph_to_md(element["paragraph"], lists)
            if md.strip():
                blocks.append(md)
        elif "table" in element:
            md = _table_to_md(element["table"], lists)
            if md.strip():
                blocks.append(md)
    return "\n\n".join(blocks)


def doc_to_markdown(doc: dict, tab_id: str | None = None) -> str:
    if tab_id:
        for tab in doc.get("tabs", []):
            if tab.get("tabProperties", {}).get("tabId") == tab_id:
                doc_tab = tab.get("documentTab", {})
                content = doc_tab.get("body", {}).get("content", [])
                lists = doc_tab.get("lists", {})
                return _content_to_md(content, lists)
        # Tab not found — fall through to main body
    content = doc.get("body", {}).get("content", [])
    lists = doc.get("lists", {})
    return _content_to_md(content, lists)


# ---------------------------------------------------------------------------
# URL parsing
# ---------------------------------------------------------------------------

def parse_url(url: str) -> tuple[str, str | None]:
    """Return (doc_id, tab_id) from a URL or bare document ID."""
    doc_id_match = re.search(r"/document/d/([a-zA-Z0-9_-]+)", url)
    doc_id = doc_id_match.group(1) if doc_id_match else url

    tab_id_match = re.search(r"tab=t\.([a-zA-Z0-9]+)", url)
    tab_id = tab_id_match.group(1) if tab_id_match else None

    return doc_id, tab_id


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a Google Doc to Markdown")
    parser.add_argument("url", help="Google Doc URL or document ID")
    parser.add_argument("-o", "--output", help="Output file path (default: print to stdout)")
    parser.add_argument("--credentials", default="credentials.json", help="Path to credentials.json")
    parser.add_argument("--token", default="token.json", help="Path to token cache file")
    args = parser.parse_args()

    doc_id, tab_id = parse_url(args.url)

    creds = get_credentials(args.credentials, args.token)
    service = build("docs", "v1", credentials=creds)

    doc = service.documents().get(documentId=doc_id, includeTabsContent=True).execute()
    markdown = doc_to_markdown(doc, tab_id)

    if args.output:
        with open(args.output, "w") as fh:
            fh.write(markdown)
        print(f"Saved to {args.output}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
