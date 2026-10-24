#!/bin/sh
# Wrap the artifact page (audible-sdr.html) into a standalone index.html.
set -e
cd "$(dirname "$0")"
{
  echo '<!doctype html>'
  echo '<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>'
  cat audible-sdr.html
  echo '</body></html>'
} > index.html
