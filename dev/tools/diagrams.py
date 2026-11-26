"""Draw the fit-test diagrams (plate map, quarter gauges in the box).
Usage: python dev/tools/diagrams.py [repo_root]  -> writes into dev/fit-tests/images/
"""
import os, struct, sys, math
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import FancyBboxPatch
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'dev', 'fit-tests', 'stl')
OUT = os.path.join(ROOT, 'dev', 'fit-tests', 'images')
SHIFT = (52 - 482.0, 31 + 111.0)
BG, FG, AC = '#ffffff', '#c9a227', '#c0392b'


def tris(path, off=(0.0, 0.0)):
    d = open(path, 'rb').read(); n = struct.unpack_from('<I', d, 80)[0]; out = []
    for i in range(n):
        v = struct.unpack_from('<12f', d, 84 + 50 * i)
        dx, dy = SHIFT[0] + off[0], SHIFT[1] + off[1]
        out.append([(v[3] + dx, v[4] + dy), (v[6] + dx, v[7] + dy), (v[9] + dx, v[10] + dy)])
    return out


# ---------- 1. labelled plate map ----------
# file, label, xy offset (the 4 quarter gauges are one file, nested 6 mm apart on the plate)
pieces = [('01_FloorQuarter_x4', '01 (x4, nested)', (0, 0)), ('01_FloorQuarter_x4', '', (-6, -6)),
          ('01_FloorQuarter_x4', '', (-12, -12)), ('01_FloorQuarter_x4', '', (-18, -18)),
          ('02_BearingRing', '02', (0, 0)), ('03a_AxleSlot', '03a', (0, 0)), ('03b_AxleStub', '03b', (0, 0)),
          ('04a_JointTab', '04a', (0, 0)), ('04b_JointSocket', '04b', (0, 0)), ('05_HygroPocket', '05', (0, 0)),
          ('06a_CouplerThread', '06a', (0, 0)), ('06b_DockSlot', '06b', (0, 0)), ('07_FilamentClip', '07', (0, 0))]
fig, ax = plt.subplots(figsize=(8, 8), facecolor=BG)
for name, label, off in pieces:
    T = tris(os.path.join(SRC, name + '.stl'), off)
    ax.add_collection(PolyCollection(T, facecolor=FG, edgecolor='none'))
    xs = [p[0] for t in T for p in t]; ys = [p[1] for t in T for p in t]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    if not label:
        continue
    if name.startswith('01_'):   # label the outer quarter near its top leg
        cx, cy = min(xs) + 45, max(ys) + 6
    ax.annotate(label, (cx, cy), ha='center', va='center', fontsize=12, fontweight='bold', color=AC,
                bbox=dict(boxstyle='round,pad=0.2', fc='white', ec=AC, lw=1))
ax.add_patch(plt.Rectangle((0, 0), 256, 256, fill=False, ec='#888', ls='--'))
ax.set_xlim(40, 216); ax.set_ylim(20, 240); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Test plate (top view): numbers match the guide', fontsize=13)
plt.tight_layout(); plt.savefig(os.path.join(OUT, '00_plate_map.png'), dpi=90, facecolor=BG); plt.close()


# ---------- 2. corner gauges in the box (top view, annotated) ----------
L, W, R, RIM = 267.0, 165.5, 50.0, 3.0
LEGX, LEGY = L / 2, W / 2


def rrect(ax, l, w, r, **kw):
    pts = []
    for cx, cy, a0 in [(l / 2 - r, w / 2 - r, 0), (-l / 2 + r, w / 2 - r, 90), (-l / 2 + r, -w / 2 + r, 180), (l / 2 - r, -w / 2 + r, 270)]:
        for k in range(31):
            a = math.radians(a0 + 3 * k)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    ax.add_patch(plt.Polygon(pts, closed=True, **kw))


def gauge(sx, sy):
    pts_o, pts_i = [], []
    cx, cy = L / 2 - R, W / 2 - R
    # outer path: leg along x, arc, leg along y
    pts_o.append((L / 2 - LEGX, W / 2))
    for k in range(31):
        a = math.pi / 2 - k * math.pi / 2 / 30
        pts_o.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    pts_o.append((L / 2, W / 2 - LEGY))
    ri = R - RIM
    pts_i.append((L / 2 - RIM, W / 2 - LEGY))
    for k in range(31):
        a = k * math.pi / 2 / 30
        pts_i.append((cx + ri * math.cos(a), cy + ri * math.sin(a)))
    pts_i.append((L / 2 - LEGX, W / 2 - RIM))
    poly = [(sx * x, sy * y) for x, y in pts_o + pts_i]
    return plt.Polygon(poly, fc=FG, ec='#7a5c00', lw=0.8)


fig, ax = plt.subplots(figsize=(10, 6.6), facecolor=BG)
rrect(ax, L, W, R, fc='#eaf2fb', ec='#4a6b8a', lw=2)
for sx in (1, -1):
    for sy in (1, -1):
        ax.add_patch(gauge(sx, sy))
for (x, y) in [(0, W / 2), (0, -W / 2), (L / 2, 0), (-L / 2, 0)]:
    ax.plot(x, y, 'o', ms=14, mfc='none', mec=AC, mew=2)
ax.text(0, W / 2 - 14, 'joins: ends should meet here', ha='center', va='top', color=AC, fontsize=11)
ax.text(0, -8, 'BOX FLOOR (top view)\n4 quarter gauges, each pushed hard into its corner\n(flip 2 of them over for the opposite corners)', ha='center', va='center', fontsize=12, color='#4a6b8a')
ax.text(0, -W / 2 + 30, "gap at a join = box is that much bigger there\nends hit / won't lie flat = box is smaller", ha='center', va='center', fontsize=11, color=AC)
ax.text(L / 2 - 30, W / 2 - 30, 'arc touches\nwall evenly', ha='center', fontsize=9, color='#7a5c00')
ax.set_xlim(-L / 2 - 8, L / 2 + 8); ax.set_ylim(-W / 2 - 8, W / 2 + 8); ax.set_aspect('equal'); ax.axis('off')
plt.tight_layout(); plt.savefig(os.path.join(OUT, '01_quarters_in_box.png'), dpi=90, facecolor=BG); plt.close()


print('ok')
