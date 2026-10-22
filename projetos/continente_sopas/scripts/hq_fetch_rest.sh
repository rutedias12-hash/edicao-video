#!/bin/bash
# Descarrega os clipes que faltam, um de cada vez: extrai os pedaços da montagem e apaga o clipe grande.
set -euo pipefail
V=/home/user/edicao-video/videos
LIST=/tmp/claude-0/-home-user-edicao-video/758a7deb-4170-5dbb-8449-875aadb8186a/scratchpad/hq_list.json
python3 -c "import json;[print(i,p.split('/')[-1]) for i,p in json.load(open('$LIST'))]" | while read id name; do
  if python3 -c "import json,sys;sys.exit(0 if '$name' in json.load(open('$V/hq_pedacos/duracoes.json')) else 1)"; then continue; fi
  echo "== $name"
  gdown "$id" -O "$V/clipes_hq/$name" -q < /dev/null
  python3 "$V/edit/scripts/hq_extract.py" < /dev/null | grep -v "^$"
  rm -f "$V/clipes_hq/$name"
done
echo FIM
