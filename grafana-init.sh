#!/bin/bash
set -e
INDEX=/usr/share/grafana/public/views/index.html
if ! grep -q 'catppuccin' "$INDEX"; then
  sed -i 's|</head>|<link rel="stylesheet" href="/public/catppuccin.css"></head>|' "$INDEX"
  echo "Grafana: Catppuccin CSS injected"
fi
exec /run.sh "$@"
