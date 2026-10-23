#!/bin/sh
# full build: HTML → pre-rendered Mermaid SVG → quote audit
set -e; cd "$(dirname "$0")"
python3 geo.py && python3 build_docs.py && python3 build_pages.py && python3 prerender_mermaid.py && python3 audit.py ../docs/*.html | tail -1
