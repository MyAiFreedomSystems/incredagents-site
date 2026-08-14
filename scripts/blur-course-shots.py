#!/usr/bin/env python3
"""Blur raw course captures to illegibility for public example cards.
Raw sources stay in site/asset-src/ (gitignored). Output goes to site/assets/.
Double-blur: gaussian + pixelate so no text survives at full resolution.
"""
from pathlib import Path
from PIL import Image, ImageFilter

SRC = Path("/Users/alethea/Documents/kimi/workspace/SkillManager_Public/site/asset-src/course-shots")
OUT = Path("/Users/alethea/Documents/kimi/workspace/SkillManager_Public/site/assets")

JOBS = [
    ("03_starting-conversations.png", "ex-tmcf-step1-manifest.png"),
    ("03_the-five-layers.png", "ex-tmcf-step2-walk.png"),
    ("03_the-5-step-assessment-methodology.png", "ex-tmcf-step3-resources.png"),
    ("03_llm-theory.png", "ex-tmcf-step4-notes-src.png"),
]

for src_name, out_name in JOBS:
    im = Image.open(SRC / src_name).convert("RGB")
    # Pixelate first (destroys letterforms), then gaussian to smooth blocks.
    small = im.resize((im.width // 14, im.height // 14), Image.BILINEAR)
    im = small.resize(im.size, Image.NEAREST)
    im = im.filter(ImageFilter.GaussianBlur(radius=6))
    im.save(OUT / out_name, optimize=True)
    print(f"{out_name}: {im.size} from {src_name}")
print("done")
