#!/usr/bin/env bash
# fullpage.sh <url> <out.png> — overshoots page height, then crops at the
# first large (>=400px) trailing blank gap so fixed-bottom artifacts like
# the scroll hint never count as content. Nothing gets cut off.
set -e
URL="$1"; OUT="$2"
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CH" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,12000 \
  --virtual-time-budget=8000 --screenshot="$OUT" "$URL" 2>/dev/null
python3 - "$OUT" << 'EOF'
import sys
from PIL import Image
p = sys.argv[1]
im = Image.open(p).convert("RGB"); w,h = im.size; px = im.load()
bg = px[w//4, h-1]  # bottom quarter-point = page background, away from edge shadows
def rowblank(y):
    return all(abs(px[x,y][0]-bg[0])+abs(px[x,y][1]-bg[1])+abs(px[x,y][2]-bg[2])<=18 for x in range(0,w-120,11))
last_content = 0; blank_run = 0; cut = h
y = 0
while y < h:
    if rowblank(y):
        blank_run += 1
    else:
        if blank_run >= 400:
            cut = last_content + 60
            break
        blank_run = 0
        last_content = y
    y += 1
else:
    cut = min(h, last_content + 60)
im.crop((0,0,w,cut)).save(p)
print(f"{p}: {w}x{cut}")
EOF
