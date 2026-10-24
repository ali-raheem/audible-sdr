#!/bin/sh
# Rebuild audible-sdr.html and index.html from src/page.html and text.md.
set -e
cd "$(dirname "$0")"
python3 build.py
