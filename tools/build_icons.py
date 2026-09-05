"""
Генератор иконок бота Become Butter.

Держит один источник правды — векторные описания 41 иконки (28 дней марафона,
экранные действия и статусы прогресса). Пишет .svg в assets/icons/svg/ и
растеризует их в .png (512x512) в assets/icons/png/ через headless-браузер.

Запуск:  python tools/build_icons.py
PNG-файлы коммитятся в репозиторий — при обычной работе бота скрипт не нужен,
он только для пересборки после правок вектора.
"""
from __future__ import annotations

import math
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG_DIR = ROOT / "assets" / "icons" / "svg"
PNG_DIR = ROOT / "assets" / "icons" / "png"
RENDER_SIZE = 512

PAL = dict(
    ink="#2C2417", butter="#F4C24E", deep="#DE9E2C", cream="#FBF3DF",
    milk="#E6EBE6", sage="#86A691", green="#5C8A55", rust="#C46B45",
    w1="#CFE0D6", w2="#F6E3B0", w3="#EFC978", w4="#EBB63F",
)


def star(cx: float, cy: float, r: float) -> str:
    pts = []
    for i in range(10):
        a = math.pi / 5 * i - math.pi / 2
        rr = r * 0.42 if i % 2 else r
        pts.append(f"{'L' if i else 'M'}{cx + rr * math.cos(a):.1f} {cy + rr * math.sin(a):.1f}")
    return " ".join(pts) + " Z"


def rays(cx: float, cy: float, r1: float, r2: float) -> str:
    lines = []
    for i in range(8):
        a = math.pi / 4 * i
        lines.append(
            f'<line x1="{cx + r1 * math.cos(a):.1f}" y1="{cy + r1 * math.sin(a):.1f}" '
            f'x2="{cx + r2 * math.cos(a):.1f}" y2="{cy + r2 * math.sin(a):.1f}"/>'
        )
    return f'<g stroke="{{ink}}" stroke-width="4" stroke-linecap="round">{"".join(lines)}</g>'


# name -> (background palette key, inner art template with {palette} fields)
ICONS: dict[str, tuple[str, str]] = {}


def add(name: str, bg: str, art: str) -> None:
    ICONS[name] = (bg, art)


# ---------------------------------------------------------------- actions
add("action_start", "cream", f"""
  {rays(60, 58, 20, 30)}
  <rect x="38" y="42" width="44" height="44" rx="9" fill="{{butter}}" stroke="{{ink}}" stroke-width="4"/>
  <path d="M38 60 h44" stroke="{{ink}}" stroke-width="3"/>
  <circle cx="52" cy="54" r="3" fill="{{ink}}"/><circle cx="68" cy="54" r="3" fill="{{ink}}"/>
  <path d="M52 70 q8 7 16 0" stroke="{{ink}}" stroke-width="4" fill="none" stroke-linecap="round"/>""")

add("action_profile", "w2", """
  <circle cx="60" cy="60" r="34" fill="none" stroke="{cream}" stroke-width="8"/>
  <path d="M60 26 A34 34 0 0 1 90 76" fill="none" stroke="{deep}" stroke-width="8" stroke-linecap="round"/>
  <rect x="46" y="46" width="28" height="28" rx="6" fill="{butter}" stroke="{ink}" stroke-width="4"/>
  <path d="M46 58 h28" stroke="{ink}" stroke-width="3"/>""")

add("action_next_task", "cream", """
  <rect x="24" y="50" width="20" height="20" rx="5" fill="{butter}" stroke="{ink}" stroke-width="4"/>
  <path d="M44 60 h30" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>
  <path d="M64 44 l18 16 l-18 16" fill="none" stroke="{ink}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>""")

add("action_return_task", "w2", """
  <path d="M86 66 A26 26 0 1 1 60 34" fill="none" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>
  <path d="M60 34 l10 -5 M60 34 l4 11" fill="none" stroke="{ink}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="50" y="50" width="20" height="20" rx="5" fill="{butter}" stroke="{ink}" stroke-width="4"/>""")

add("action_rest_start", "w1", """
  <path d="M38 54 h34 v16 a13 13 0 0 1 -13 13 h-8 a13 13 0 0 1 -13 -13 z" fill="{butter}" stroke="{ink}" stroke-width="4"/>
  <path d="M72 58 h6 a8 8 0 0 1 0 16 h-3" fill="none" stroke="{ink}" stroke-width="4"/>
  <path d="M46 46 q5 -6 0 -13 M56 46 q5 -6 0 -13 M66 46 q5 -6 0 -13" stroke="{ink}" stroke-width="3" fill="none" stroke-linecap="round"/>""")

add("action_rest_end", "w3", """
  <path d="M22 82 h76" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>
  <path d="M40 82 a20 20 0 0 1 40 0 z" fill="{butter}" stroke="{ink}" stroke-width="4"/>
  <g stroke="{ink}" stroke-width="4" stroke-linecap="round">
    <line x1="60" y1="40" x2="60" y2="30"/><line x1="86" y1="52" x2="93" y2="45"/><line x1="34" y1="52" x2="27" y2="45"/>
  </g>""")

add("action_done", "cream", """
  <rect x="28" y="32" width="64" height="56" rx="11" fill="{butter}" stroke="{ink}" stroke-width="4"/>
  <path d="M28 48 h64" stroke="{ink}" stroke-width="3"/>
  <path d="M42 62 l11 11 l24 -26" fill="none" stroke="{green}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>""")

add("action_failed", "w1", """
  <rect x="30" y="30" width="60" height="40" rx="9" fill="{butter}" stroke="{ink}" stroke-width="4"/>
  <path d="M40 70 q0 16 -7 21 q-8 -5 -8 -14 q1 -5 6 -9 z" fill="{butter}" stroke="{ink}" stroke-width="4"/>
  <path d="M62 44 l14 14 M76 44 l-14 14" stroke="{rust}" stroke-width="6" stroke-linecap="round"/>""")

# ---------------------------------------------------------------- statuses
add("status_0_raw_cream", "milk", """
  <path d="M42 32 h36 l-4 54 a6 6 0 0 1 -6 5 h-10 a6 6 0 0 1 -6 -5 z" fill="{cream}" stroke="{ink}" stroke-width="4"/>
  <path d="M41 58 h38 l-2 26 a4 4 0 0 1 -4 4 h-26 a4 4 0 0 1 -4 -4 z" fill="{w2}"/>
  <path d="M43 52 q17 7 34 0" stroke="{ink}" stroke-width="3" fill="none"/>""")

add("status_7_whipped_butter", "w2", """
  <path d="M30 56 a30 20 0 0 0 60 0 z" fill="{butter}" stroke="{ink}" stroke-width="4"/>
  <path d="M38 56 q5 -16 10 0 q6 -16 12 0 q6 -14 10 0" fill="{cream}" stroke="{ink}" stroke-width="3"/>
  <path d="M70 52 l12 -28" stroke="{ink}" stroke-width="4" stroke-linecap="round"/>
  <path d="M64 42 q12 -3 16 -16 q0 14 -9 22 z" fill="none" stroke="{ink}" stroke-width="3"/>""")

add("status_14_smooth_texture", "w3", """
  <rect x="30" y="46" width="60" height="34" rx="7" fill="{butter}" stroke="{ink}" stroke-width="4"/>
  <path d="M32 56 q28 -15 56 0" stroke="{cream}" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M72 28 l16 7 l-32 15 l-9 -5 z" fill="{cream}" stroke="{ink}" stroke-width="3" stroke-linejoin="round"/>""")

add("status_21_premium_block", "w4", f"""
  <rect x="26" y="42" width="66" height="40" rx="7" fill="{{cream}}" stroke="{{ink}}" stroke-width="4"/>
  <rect x="52" y="42" width="15" height="40" fill="{{deep}}" stroke="{{ink}}" stroke-width="4"/>
  <path d="{star(88, 30, 9)}" fill="{{butter}}" stroke="{{ink}}" stroke-width="2"/>""")

add("status_28_solid_gold", "w4", f"""
  <path d="M42 40 h36 l-4 18 a14 14 0 0 1 -28 0 z" fill="{{butter}}" stroke="{{ink}}" stroke-width="4"/>
  <path d="M42 44 h-9 a9 9 0 0 0 9 10 M78 44 h9 a9 9 0 0 1 -9 10" fill="none" stroke="{{ink}}" stroke-width="4"/>
  <rect x="54" y="58" width="12" height="11" fill="{{butter}}" stroke="{{ink}}" stroke-width="4"/>
  <rect x="43" y="69" width="34" height="10" rx="3" fill="{{deep}}" stroke="{{ink}}" stroke-width="4"/>
  <path d="{star(60, 30, 7)}" fill="{{cream}}" stroke="{{ink}}" stroke-width="2"/>""")

# ---------------------------------------------------------------- 28 days
DAY_ART = {
    1: """
      <path d="M28 34 h64 l-21 25 v22 l-22 9 v-31 z" fill="{butter}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
      <circle cx="40" cy="24" r="4" fill="{rust}"/><circle cx="58" cy="21" r="4" fill="{rust}"/><circle cx="76" cy="24" r="4" fill="{rust}"/>
      <circle cx="60" cy="98" r="5" fill="{green}"/>""",
    2: """
      <path d="M74 26 a30 30 0 1 0 18 52 a24 24 0 0 1 -18 -52 z" fill="{butter}" stroke="{ink}" stroke-width="4"/>
      <rect x="28" y="58" width="22" height="36" rx="4" fill="{cream}" stroke="{ink}" stroke-width="4"/>
      <path d="M32 64 l14 24 M46 64 l-14 24" stroke="{rust}" stroke-width="4" stroke-linecap="round"/>""",
    3: """
      <path d="M30 42 h30 v10 h12 v12" fill="none" stroke="{ink}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
      <rect x="24" y="34" width="12" height="16" rx="3" fill="{butter}" stroke="{ink}" stroke-width="4"/>
      <path d="M72 68 q6 11 0 18 q-6 -7 0 -18 z" fill="{butter}" stroke="{ink}" stroke-width="3"/>
      <circle cx="72" cy="94" r="5" fill="{butter}" stroke="{ink}" stroke-width="3"/>""",
    4: """
      <path d="M44 34 h30 l-4 50 a6 6 0 0 1 -6 5 h-10 a6 6 0 0 1 -6 -5 z" fill="{cream}" stroke="{ink}" stroke-width="4"/>
      <path d="M42 58 h34 l-3 26 a4 4 0 0 1 -4 4 h-20 a4 4 0 0 1 -4 -4 z" fill="{w1}"/>
      <circle cx="84" cy="34" r="8" fill="none" stroke="{ink}" stroke-width="4"/>
      <g stroke="{ink}" stroke-width="4" stroke-linecap="round"><line x1="84" y1="20" x2="84" y2="26"/><line x1="84" y1="42" x2="84" y2="48"/><line x1="70" y1="34" x2="76" y2="34"/><line x1="92" y1="34" x2="98" y2="34"/></g>""",
    5: """
      <circle cx="58" cy="62" r="28" fill="none" stroke="{ink}" stroke-width="5"/>
      <circle cx="58" cy="62" r="15" fill="none" stroke="{ink}" stroke-width="5"/>
      <circle cx="58" cy="62" r="4" fill="{rust}"/>
      <path d="M92 30 l-24 24" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>
      <path d="M80 28 l12 2 l2 12" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>""",
    6: """
      <path d="M30 50 l30 -13 l30 13 l-30 13 z" fill="{butter}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
      <path d="M32 52 v27 l27 12 v-27 z" fill="{deep}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
      <path d="M88 52 v27 l-27 12 v-27 z" fill="{butter}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
      <path d="M60 22 l3 9 M74 24 l-3 9 M48 25 l4 8" stroke="{ink}" stroke-width="3" stroke-linecap="round"/>""",
    7: f"""
      {rays(44, 44, 13, 21)}
      <circle cx="44" cy="44" r="12" fill="{{butter}}" stroke="{{ink}}" stroke-width="4"/>
      <rect x="58" y="54" width="24" height="38" rx="5" fill="{{cream}}" stroke="{{ink}}" stroke-width="4"/>
      <path d="M50 50 l40 46" stroke="{{rust}}" stroke-width="5" stroke-linecap="round"/>""",
    8: """
      <rect x="34" y="28" width="44" height="60" rx="6" fill="{cream}" stroke="{ink}" stroke-width="4"/>
      <g stroke="{ink}" stroke-width="3">
        <rect x="41" y="40" width="7" height="7" rx="1.5" fill="none"/><line x1="53" y1="43.5" x2="70" y2="43.5" stroke-linecap="round"/>
        <rect x="41" y="53" width="7" height="7" rx="1.5" fill="none"/><line x1="53" y1="56.5" x2="70" y2="56.5" stroke-linecap="round"/>
        <rect x="41" y="66" width="7" height="7" rx="1.5" fill="none"/><line x1="53" y1="69.5" x2="70" y2="69.5" stroke-linecap="round"/>
      </g>
      <path d="M82 24 a10 10 0 1 0 7 16 a8 8 0 0 1 -7 -16 z" fill="{butter}" stroke="{ink}" stroke-width="3"/>""",
    9: """
      <ellipse cx="60" cy="66" rx="28" ry="20" fill="{green}" stroke="{ink}" stroke-width="4"/>
      <circle cx="46" cy="44" r="10" fill="{green}" stroke="{ink}" stroke-width="4"/>
      <circle cx="74" cy="44" r="10" fill="{green}" stroke="{ink}" stroke-width="4"/>
      <circle cx="46" cy="43" r="3" fill="{ink}"/><circle cx="74" cy="43" r="3" fill="{ink}"/>
      <path d="M48 72 q12 9 24 0" stroke="{ink}" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path d="M34 82 l-8 7 M86 82 l8 7" stroke="{ink}" stroke-width="4" stroke-linecap="round"/>""",
    10: """
      <circle cx="60" cy="66" r="26" fill="{rust}" stroke="{ink}" stroke-width="4"/>
      <path d="M52 40 q8 -12 16 0" fill="{green}" stroke="{ink}" stroke-width="3"/>
      <rect x="56" y="32" width="8" height="10" rx="2" fill="{green}" stroke="{ink}" stroke-width="3"/>
      <path d="M60 66 v-15 M60 66 l11 6" stroke="{cream}" stroke-width="4" stroke-linecap="round"/>""",
    11: """
      <line x1="34" y1="22" x2="34" y2="98" stroke="{ink}" stroke-width="4" stroke-linecap="round"/>
      <g stroke="{ink}" stroke-width="3"><line x1="34" y1="34" x2="42" y2="34"/><line x1="34" y1="50" x2="44" y2="50"/><line x1="34" y1="66" x2="42" y2="66"/><line x1="34" y1="82" x2="44" y2="82"/></g>
      <circle cx="66" cy="34" r="8" fill="{butter}" stroke="{ink}" stroke-width="4"/>
      <path d="M66 42 v30 M66 52 h-11 M66 52 h11 M66 72 l-9 18 M66 72 l9 18" stroke="{ink}" stroke-width="4" stroke-linecap="round" fill="none"/>""",
    12: """
      <path d="M44 68 q0 -28 16 -28 q16 0 16 28 l5 8 h-42 z" fill="{butter}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
      <path d="M53 84 a7 7 0 0 0 14 0" fill="none" stroke="{ink}" stroke-width="4"/>
      <path d="M30 32 l60 58" stroke="{rust}" stroke-width="5" stroke-linecap="round"/>""",
    13: """
      <circle cx="46" cy="30" r="7" fill="{butter}" stroke="{ink}" stroke-width="4"/>
      <path d="M46 37 l1 22 M47 45 l-10 8 M47 45 l11 6 M47 59 l-10 24 M47 59 l13 20" stroke="{ink}" stroke-width="4" stroke-linecap="round" fill="none"/>
      <line x1="84" y1="92" x2="84" y2="60" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>
      <circle cx="84" cy="48" r="16" fill="{green}" stroke="{ink}" stroke-width="4"/>""",
    14: """
      <rect x="28" y="28" width="44" height="54" rx="6" fill="{cream}" stroke="{ink}" stroke-width="4"/>
      <path d="M36 58 l9 -9 l8 6 l11 -15" fill="none" stroke="{deep}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="74" cy="74" r="14" fill="none" stroke="{ink}" stroke-width="5"/>
      <line x1="84" y1="84" x2="94" y2="94" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>""",
    15: f"""
      <path d="M28 46 q16 -8 32 0 q16 -8 32 0 v34 q-16 -8 -32 0 q-16 -8 -32 0 z" fill="{{cream}}" stroke="{{ink}}" stroke-width="4" stroke-linejoin="round"/>
      <line x1="60" y1="46" x2="60" y2="80" stroke="{{ink}}" stroke-width="4"/>
      <path d="{star(60, 28, 9)}" fill="{{butter}}" stroke="{{ink}}" stroke-width="2"/>""",
    16: """
      <path d="M26 38 h68 v34 h-42 l-14 12 v-12 h-12 z" fill="{butter}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
      <path d="M60 48 c-6 -8 -18 -3 -13 8 c3 7 13 13 13 13 c0 0 10 -6 13 -13 c5 -11 -7 -16 -13 -8 z" fill="{rust}" stroke="{ink}" stroke-width="3"/>""",
    17: """
      <circle cx="60" cy="60" r="15" fill="{rust}" stroke="{ink}" stroke-width="4"/>
      <path d="M45 60 l-15 -9 v18 z M75 60 l15 -9 v18 z" fill="{butter}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
      <circle cx="60" cy="60" r="30" fill="none" stroke="{ink}" stroke-width="5"/>
      <line x1="39" y1="39" x2="81" y2="81" stroke="{ink}" stroke-width="5"/>""",
    18: """
      <path d="M40 68 q-11 -5 -7 -18 q-5 -13 8 -17 q6 -11 19 -5 q13 -5 17 8 q11 4 7 17 q5 13 -9 17 q-8 9 -20 3 q-11 5 -22 -5 z" fill="{butter}" stroke="{ink}" stroke-width="4"/>
      <path d="M60 44 v-16" stroke="{ink}" stroke-width="3" stroke-linecap="round"/>
      <path d="M60 34 q-9 -1 -9 -11 q9 0 9 9 M60 36 q9 -1 9 -11 q-9 0 -9 9" fill="{green}" stroke="{ink}" stroke-width="3"/>""",
    19: f"""
      <path d="{star(38, 52, 9)}" fill="{{butter}}" stroke="{{ink}}" stroke-width="3"/>
      <path d="{star(60, 40, 12)}" fill="{{butter}}" stroke="{{ink}}" stroke-width="3"/>
      <path d="{star(82, 54, 9)}" fill="{{butter}}" stroke="{{ink}}" stroke-width="3"/>
      <rect x="34" y="66" width="52" height="24" rx="5" fill="{{cream}}" stroke="{{ink}}" stroke-width="4"/>
      <g stroke="{{ink}}" stroke-width="3" stroke-linecap="round"><line x1="42" y1="74" x2="78" y2="74"/><line x1="42" y1="82" x2="66" y2="82"/></g>""",
    20: """
      <rect x="30" y="38" width="34" height="34" rx="4" fill="{butter}" stroke="{ink}" stroke-width="4"/>
      <circle cx="64" cy="55" r="8" fill="{butter}" stroke="{ink}" stroke-width="4"/>
      <path d="M30 55 h-8 a8 8 0 0 0 8 8" fill="none" stroke="{ink}" stroke-width="4"/>
      <text x="60" y="86" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="22" fill="{ink}">Aa</text>""",
    21: """
      <rect x="42" y="26" width="36" height="66" rx="9" fill="{cream}" stroke="{ink}" stroke-width="4"/>
      <circle cx="60" cy="59" r="14" fill="{butter}" stroke="{ink}" stroke-width="3"/>
      <path d="M64 50 a11 11 0 1 0 7 18 a9 9 0 0 1 -7 -18 z" fill="{deep}"/>""",
    22: """
      <path d="M22 88 l24 -42 l16 24 l12 -18 l22 36 z" fill="{butter}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
      <path d="M46 46 l-7 -10 l5 -2 l6 8 z" fill="{cream}" stroke="{ink}" stroke-width="2"/>
      <path d="M60 40 q7 6 1 13 q-9 -1 -5 -11 q2 5 4 -2 z" fill="{rust}" stroke="{ink}" stroke-width="2"/>""",
    23: """
      <rect x="28" y="46" width="58" height="38" rx="7" fill="{butter}" stroke="{ink}" stroke-width="4"/>
      <path d="M28 56 h58" stroke="{ink}" stroke-width="3"/>
      <circle cx="74" cy="65" r="6" fill="{deep}" stroke="{ink}" stroke-width="3"/>
      <circle cx="52" cy="32" r="9" fill="{deep}" stroke="{ink}" stroke-width="3"/>
      <text x="52" y="37" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="12" fill="{ink}">&#8381;</text>""",
    24: """
      <path d="M20 84 h80" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>
      <path d="M42 84 a18 18 0 0 1 36 0 z" fill="{butter}" stroke="{ink}" stroke-width="4"/>
      <g stroke="{ink}" stroke-width="4" stroke-linecap="round">
        <line x1="60" y1="44" x2="60" y2="34"/><line x1="85" y1="54" x2="92" y2="47"/><line x1="35" y1="54" x2="28" y2="47"/>
        <path d="M46 34 l6 -8 l6 8 M74 34 l-6 -8 -6 8" fill="none"/></g>""",
    25: """
      <path d="M60 24 l26 10 v22 c0 20 -14 30 -26 34 c-12 -4 -26 -14 -26 -34 v-22 z" fill="{butter}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
      <line x1="46" y1="58" x2="74" y2="58" stroke="{rust}" stroke-width="7" stroke-linecap="round"/>""",
    26: """
      <circle cx="52" cy="28" r="7" fill="{butter}" stroke="{ink}" stroke-width="4"/>
      <path d="M52 35 l-5 20 l-12 9 M48 44 l14 6 l9 -8 M48 55 l-9 24 M48 55 l16 15 l-3 15" stroke="{ink}" stroke-width="4" stroke-linecap="round" fill="none"/>
      <g stroke="{ink}" stroke-width="3" stroke-linecap="round"><line x1="74" y1="26" x2="86" y2="26"/><line x1="72" y1="35" x2="82" y2="35"/></g>""",
    27: """
      <rect x="28" y="40" width="60" height="42" rx="5" fill="{cream}" stroke="{ink}" stroke-width="4"/>
      <path d="M28 44 l30 22 l30 -22" fill="none" stroke="{ink}" stroke-width="4"/>
      <circle cx="82" cy="78" r="13" fill="{butter}" stroke="{ink}" stroke-width="4"/>
      <path d="M82 71 v7 l5 4" stroke="{ink}" stroke-width="3" stroke-linecap="round" fill="none"/>""",
    28: f"""
      <path d="M42 40 h36 l-4 18 a14 14 0 0 1 -28 0 z" fill="{{butter}}" stroke="{{ink}}" stroke-width="4"/>
      <path d="M42 44 h-9 a9 9 0 0 0 9 10 M78 44 h9 a9 9 0 0 1 -9 10" fill="none" stroke="{{ink}}" stroke-width="4"/>
      <rect x="54" y="58" width="12" height="11" fill="{{butter}}" stroke="{{ink}}" stroke-width="4"/>
      <rect x="43" y="69" width="34" height="10" rx="3" fill="{{deep}}" stroke="{{ink}}" stroke-width="4"/>
      <path d="M49 40 l5 -10 l6 7 l6 -7 l5 10 z" fill="{{butter}}" stroke="{{ink}}" stroke-width="3" stroke-linejoin="round"/>
      <circle cx="26" cy="34" r="3" fill="{{rust}}"/><circle cx="94" cy="40" r="3" fill="{{green}}"/>
      <circle cx="28" cy="72" r="3" fill="{{deep}}"/><circle cx="92" cy="74" r="3" fill="{{rust}}"/>""",
}

for _day, _art in DAY_ART.items():
    _week_bg = {1: "w1", 2: "w2", 3: "w3", 4: "w4"}[(_day - 1) // 7 + 1]
    add(f"day_{_day:02d}", _week_bg, _art)


def build_svg(bg_key: str, art: str) -> str:
    bg = PAL[bg_key]
    inner = art.format(**PAL).strip()
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{RENDER_SIZE}" height="{RENDER_SIZE}" '
        f'viewBox="0 0 120 120">\n'
        f'  <rect width="120" height="120" fill="{bg}"/>\n'
        f'  {inner}\n'
        f'</svg>\n'
    )


def find_browser() -> str | None:
    candidates = [
        shutil.which("msedge"),
        shutil.which("chrome"),
        shutil.which("chromium"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for c in candidates:
        if c and Path(c).exists():
            return c
    return None


def main() -> int:
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    PNG_DIR.mkdir(parents=True, exist_ok=True)

    for name, (bg_key, art) in sorted(ICONS.items()):
        (SVG_DIR / f"{name}.svg").write_text(build_svg(bg_key, art), encoding="utf-8")
    print(f"SVG: {len(ICONS)} файлов -> {SVG_DIR.relative_to(ROOT)}")

    browser = find_browser()
    if not browser:
        print("Браузер (Edge/Chrome) не найден — PNG не собраны. SVG на месте.", file=sys.stderr)
        return 1

    fails = 0
    for name in sorted(ICONS):
        src = (SVG_DIR / f"{name}.svg").resolve()
        out = (PNG_DIR / f"{name}.png").resolve()
        cmd = [
            browser, "--headless", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", f"--window-size={RENDER_SIZE},{RENDER_SIZE}",
            f"--screenshot={out}", src.as_uri(),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if not out.exists():
            fails += 1
            print(f"  FAIL {name}: {res.stderr.strip()[:200]}", file=sys.stderr)
    print(f"PNG: {len(ICONS) - fails}/{len(ICONS)} собрано -> {PNG_DIR.relative_to(ROOT)}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
