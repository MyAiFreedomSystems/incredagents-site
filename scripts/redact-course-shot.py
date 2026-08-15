#!/usr/bin/env python3
"""Selective redaction: blur ONLY identifying regions (community/course name,
sidebar course outline, any faces), keep the lesson body readable so viewers
can tell it's a real classroom. Raw source stays in gitignored asset-src."""
from pathlib import Path
from PIL import Image, ImageFilter

SRC = Path("/Users/alethea/Documents/kimi/workspace/SkillManager_Public/site/asset-src/course-shots/03_the-five-layers.png")
OUT = Path("/Users/alethea/Documents/kimi/workspace/SkillManager_Public/site/assets/ex-tmcf-source-circle.png")

im = Image.open(SRC).convert("RGB")

# (left, top, right, bottom) boxes on the 1280x720 capture:
# 1. header course/community name "AIOS: AI Operating Systems"
# 2. right sidebar: the course outline (lesson titles identify the course)
BOXES = [
    (38, 8, 345, 58),
    (918, 80, 1250, 720),
]

for box in BOXES:
    region = im.crop(box)
    small = region.resize((max(1, region.width // 12), max(1, region.height // 12)), Image.BILINEAR)
    region = small.resize(region.size, Image.NEAREST).filter(ImageFilter.GaussianBlur(radius=4))
    im.paste(region, box)

im.save(OUT, optimize=True)
print(f"saved {OUT} {im.size}")
