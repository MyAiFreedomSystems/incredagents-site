#!/usr/bin/env python3
"""Cohesive logo set for all 16 skills: navy rounded-square badge, gold ring,
white/gold glyph. 256x256 viewBox. Written to site/assets/skill-<slug>.svg"""
import pathlib

OUT = pathlib.Path(__file__).parent.parent / "site" / "assets"

W = 'stroke="#fafaf8" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"'
G = 'stroke="#d9a441" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"'
WF = 'fill="#fafaf8"'
GF = 'fill="#d9a441"'
SF = 'fill="#8ba888"'  # sage accent
TF = 'fill="#c9825d"'  # terracotta accent

GLYPHS = {
 # three brief cards with radio dots
 "brief-me": f'''
  <rect x="52" y="76" width="42" height="104" rx="9" {W}/>
  <rect x="107" y="76" width="42" height="104" rx="9" {W}/>
  <rect x="162" y="76" width="42" height="104" rx="9" {W}/>
  <circle cx="73" cy="100" r="6" {GF}/><circle cx="73" cy="122" r="6" {GF}/>
  <circle cx="128" cy="100" r="6" {GF}/><circle cx="128" cy="122" r="6" {GF}/>
  <circle cx="183" cy="100" r="6" {GF}/>
  <path d="M66 156 h14 M121 156 h14 M176 156 h14" {G}/>''',
 # image frame with sun + mountains + sparkle
 "graphics": f'''
  <rect x="52" y="72" width="152" height="112" rx="12" {W}/>
  <circle cx="92" cy="104" r="12" {GF}/>
  <path d="M60 176 L104 126 L132 156 L156 130 L196 176" {G}/>
  <path d="M196 52 l5 12 12 5 -12 5 -5 12 -5 -12 -12 -5 12 -5 z" {GF}/>''',
 # target with gold bullseye + turn-budget tick ring
 "goal": f'''
  <circle cx="128" cy="128" r="58" {W}/>
  <circle cx="128" cy="128" r="34" {W}/>
  <circle cx="128" cy="128" r="12" {GF}/>
  <path d="M128 52 v18 M128 186 v18 M52 128 h18 M186 128 h18" {G}/>''',
 # continuous improvement: two chasing arrows + rising step
 "kaizen": f'''
  <path d="M168 84 a52 52 0 1 0 14 44" {W}/>
  <path d="M176 58 l8 30 -30 -8 z" {GF}/>
  <path d="M84 158 l20 -20 18 12 34 -34" {G}/>
  <path d="M138 116 h20 v20" {G}/>''',
 # gated checklist: clipboard + gold checks + gate bar
 "pre-build-sop": f'''
  <rect x="66" y="66" width="124" height="132" rx="12" {W}/>
  <rect x="102" y="52" width="52" height="24" rx="9" {GF}/>
  <path d="M84 108 l10 10 18 -18 M84 140 l10 10 18 -18" {G}/>
  <path d="M126 104 h48 M126 136 h48" {W}/>
  <path d="M84 176 h88" {G}/>''',
 # archive box with evidence receipt + check
 "wrapup": f'''
  <path d="M56 96 h144 v22 a8 8 0 0 1 -8 8 h-128 a8 8 0 0 1 -8 -8 z" {W}/>
  <path d="M70 126 v52 a12 12 0 0 0 12 12 h92 a12 12 0 0 0 12 -12 v-52" {W}/>
  <path d="M112 152 l12 12 24 -24" {G}/>
  <path d="M108 82 h40" {G}/>''',
 # hub and spoke team panel
 "moe-build-team": f'''
  <circle cx="128" cy="128" r="20" {GF}/>
  <circle cx="128" cy="62" r="13" {W}/><circle cx="190" cy="100" r="13" {W}/>
  <circle cx="176" cy="172" r="13" {W}/><circle cx="80" cy="172" r="13" {W}/>
  <circle cx="66" cy="100" r="13" {W}/>
  <path d="M128 82 v26 M178 108 l-32 12 M166 164 l-24 -22 M90 164 l24 -22 M78 108 l32 12" {G}/>''',
 # routing matrix: dot grid with a routed arrow path
 "routing-matrix": f'''
  <circle cx="70" cy="70" r="9" {WF}/><circle cx="128" cy="70" r="9" {WF}/><circle cx="186" cy="70" r="9" {WF}/>
  <circle cx="70" cy="128" r="9" {WF}/><circle cx="186" cy="128" r="9" {WF}/>
  <circle cx="70" cy="186" r="9" {WF}/><circle cx="128" cy="186" r="9" {WF}/><circle cx="186" cy="186" r="9" {WF}/>
  <path d="M70 70 h58 v118 h40" {G}/>
  <path d="M178 178 l14 8 -14 8 z" {GF}/>
  <rect x="112" y="112" width="32" height="32" rx="8" {G}/>''',
 # folder with scaffold lines
 "provision-project": f'''
  <path d="M52 90 a10 10 0 0 1 10 -10 h42 l14 16 h76 a10 10 0 0 1 10 10 v72 a10 10 0 0 1 -10 10 h-132 a10 10 0 0 1 -10 -10 z" {W}/>
  <path d="M84 128 h88 M84 152 h64" {G}/>
  <path d="M84 176 h40" {W}/>''',
 # single agent id card with soul spark
 "provision-agent": f'''
  <rect x="58" y="70" width="140" height="116" rx="14" {W}/>
  <circle cx="100" cy="114" r="18" {W}/>
  <path d="M132 104 h48 M132 124 h34" {G}/>
  <path d="M82 164 a22 22 0 0 1 36 0" {G}/>
  <path d="M168 148 l4 10 10 4 -10 4 -4 10 -4 -10 -10 -4 10 -4 z" {GF}/>''',
 # three linked team cards
 "provision-team": f'''
  <rect x="44" y="88" width="72" height="88" rx="12" {W}/>
  <rect x="140" y="88" width="72" height="88" rx="12" {W}/>
  <rect x="92" y="64" width="72" height="88" rx="12" {G}/>
  <circle cx="128" cy="94" r="12" {GF}/>
  <path d="M108 132 a20 20 0 0 1 40 0" {G}/>
  <circle cx="80" cy="116" r="9" {WF}/><circle cx="176" cy="116" r="9" {WF}/>''',
 # hook glyph
 "hooks-guide": f'''
  <circle cx="128" cy="70" r="16" {W}/>
  <path d="M128 86 v40 a34 34 0 1 1 -34 -34" {W}/>
  <path d="M82 82 l14 10 -16 10 z" {GF}/>
  <path d="M150 150 l22 -8 -6 24 z" {GF}/>''',
 # magnet pulling in quote marks
 "harvest": f'''
  <path d="M84 60 v52 a44 44 0 0 0 88 0 v-52" {W}/>
  <path d="M84 60 h26 v26 h-26 z M146 60 h26 v26 h-26 z" {GF}/>
  <path d="M66 196 q6 -14 16 -16 M106 206 q6 -14 16 -16 M146 196 q6 -14 16 -16" {G}/>''',
 # branded card with star + circular photo
 "graphic": f'''
  <rect x="58" y="66" width="140" height="124" rx="14" {W}/>
  <circle cx="128" cy="108" r="18" {G}/>
  <path d="M128 138 l6 12 13 2 -9 9 2 13 -12 -6 -12 6 2 -13 -9 -9 13 -2 z" {GF}/>
  <path d="M84 172 h88" {G}/>''',
 # wall-of-love layout grid
 "display": f'''
  <rect x="52" y="70" width="70" height="52" rx="9" {W}/>
  <rect x="134" y="70" width="70" height="52" rx="9" {W}/>
  <rect x="52" y="134" width="70" height="52" rx="9" {W}/>
  <rect x="134" y="134" width="70" height="52" rx="9" {G}/>
  <path d="M66 88 q4 -9 12 -10 M148 88 q4 -9 12 -10 M66 152 q4 -9 12 -10 M148 152 q4 -9 12 -10" {GF}/>''',
 # theme swatches + hex tag
 "theme": f'''
  <rect x="60" y="66" width="60" height="84" rx="10" {W}/>
  <rect x="98" y="88" width="60" height="84" rx="10" {G}/>
  <rect x="136" y="110" width="60" height="84" rx="10" {W}/>
  <path d="M76 84 h28 M114 106 h28 M152 128 h28" {GF}/>
  <path d="M76 134 h28" {G}/>''',
}

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#1b3a5c"/><stop offset="1" stop-color="#122a45"/>
</linearGradient></defs>
<rect x="8" y="8" width="240" height="240" rx="52" fill="url(#bg)" stroke="#d9a441" stroke-width="6"/>
{glyph}
</svg>
"""

NAME = {
 "brief-me":"brief-me","graphics":"graphics","goal":"goal","kaizen":"kaizen",
 "pre-build-sop":"pre-build-sop","wrapup":"wrapup","moe-build-team":"moe-build-team",
 "routing-matrix":"routing-matrix","provision-project":"provision-project",
 "provision-agent":"provision-agent","provision-team":"provision-team",
 "hooks-guide":"hooks-guide","harvest":"harvest","graphic":"graphic",
 "display":"display","theme":"theme",
}

for slug, glyph in GLYPHS.items():
    (OUT / f"skill-{slug}.svg").write_text(TEMPLATE.format(glyph=glyph))
    print(f"skill-{slug}.svg")
print(len(GLYPHS), "logos")
