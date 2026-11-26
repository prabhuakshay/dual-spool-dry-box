#!/usr/bin/env python3
"""Build DualSpoolDryBox_PRINT_ALL.3mf: one Bambu Studio / OrcaSlicer project with every printed
part, in its required quantity, laid out on 3 plates (256 x 256 mm bed).

Usage (from anywhere):  python dev/tools/build_3mf.py [repo_root]

Reads the print-oriented meshes in src/stl/ and writes DualSpoolDryBox_PRINT_ALL.3mf in the repo root.
The plate format follows Bambu Studio's project 3MF (plates are 1.2 x bed width apart, 2 per row).
Standard library only.
"""
import math, os, struct, sys, uuid, zipfile

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', '..'))
STL = os.path.join(ROOT, 'src', 'stl')
OUT = os.path.join(ROOT, 'DualSpoolDryBox_PRINT_ALL.3mf')
BED = 256.0
STRIDE = BED * 1.2

# (plate name, [(stl file, object name, min x, min y)]) -- every part in its print quantity
PLATES = [
    ('1 - Cradle half A + tray lid + 2 axles + 2 guide nuts', [
        ('01_CradleHalf_x2.stl', 'Cradle half A', 5, 46.75), ('02_TrayLid_x2.stl', 'Tray lid A', 152, 47),
        ('04_Axle_x2.stl', 'Axle 1', 200, 47), ('04_Axle_x2.stl', 'Axle 2', 213, 47),
        ('07_GuideNut_x2.stl', 'Guide nut 1', 228, 60), ('07_GuideNut_x2.stl', 'Guide nut 2', 228, 90)]),
    ('2 - Cradle half B + tray lid + tube dock + 4 spacers', [
        ('01_CradleHalf_x2.stl', 'Cradle half B', 5, 46.75), ('02_TrayLid_x2.stl', 'Tray lid B', 152, 47),
        ('06_TubeDockBridge_x1.stl', 'Tube dock bridge', 200, 47)]
        + [('05_Spacer_x4.stl', 'Spacer %d (brim!)' % (i + 1), 230, 47 + 18 * i) for i in range(4)]),
    ('3 - 8 wheels + drill jig', [
        ('03_Wheel_x8.stl', 'Wheel %d' % (4 * j + i + 1), 20 + 34 * i, 40 + 35 * j) for j in range(2) for i in range(4)]
        + [('08_DrillJig_x1.stl', 'Drill jig (one-time use)', 170, 40)]),
]


def read_stl(path):
    data = open(path, 'rb').read()
    n = struct.unpack_from('<I', data, 80)[0]
    verts, index, tris = [], {}, []
    for t in range(n):
        vals = struct.unpack_from('<12f', data, 84 + 50 * t)
        tri = []
        for k in range(3):
            key = tuple(round(c, 5) for c in vals[3 + 3 * k: 6 + 3 * k])
            if key not in index:
                index[key] = len(verts); verts.append(key)
            tri.append(index[key])
        if len(set(tri)) == 3:
            tris.append(tri)
    lo = tuple(min(v[i] for v in verts) for i in range(3))
    hi = tuple(max(v[i] for v in verts) for i in range(3))
    return verts, tris, lo, hi


cache, objects = {}, []
cols = math.ceil(math.sqrt(len(PLATES)))
for p, (_, items) in enumerate(PLATES):
    ox, oy = (p % cols) * STRIDE, -(p // cols) * STRIDE
    for mesh, name, tx, ty in items:
        if mesh not in cache:
            cache[mesh] = read_stl(os.path.join(STL, mesh))
        _, tris, lo, hi = cache[mesh]
        dx, dy = tx - lo[0], ty - lo[1]
        wid = 2 * (len(objects) + 1)
        objects.append(dict(wid=wid, iid=wid - 1, name=name, mesh=mesh, plate=p, ntri=len(tris),
                            t=(ox + dx, oy + dy, -lo[2]),
                            bb=((lo[0] + dx, lo[1] + dy), (hi[0] + dx, hi[1] + dy))))

# sanity checks: every part on the bed, no two parts closer than 1 mm (bounding boxes)
errors = []
for o in objects:
    (x0, y0), (x1, y1) = o['bb']
    if x0 < 0 or y0 < 0 or x1 > BED or y1 > BED:
        errors.append('%s is off the bed' % o['name'])
for i, a in enumerate(objects):
    for b in objects[i + 1:]:
        (ax0, ay0), (ax1, ay1) = a['bb']; (bx0, by0), (bx1, by1) = b['bb']
        if a['plate'] == b['plate'] and ax0 < bx1 + 1 and bx0 < ax1 + 1 and ay0 < by1 + 1 and by0 < ay1 + 1:
            errors.append('%s overlaps %s' % (a['name'], b['name']))
if errors:
    sys.exit('\n'.join(errors))

CORE = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
PROD = 'http://schemas.microsoft.com/3dmanufacturing/production/2015/06'
BBS = 'http://schemas.bambulab.com/package/2021'
HEAD = ('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" xmlns="%s" '
        'xmlns:BambuStudio="%s" xmlns:p="%s" requiredextensions="p">\n' % (CORE, BBS, PROD))
U = lambda: str(uuid.uuid4())


def mesh_xml(o):
    verts, tris, _, _ = cache[o['mesh']]
    out = [HEAD, ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n <resources>\n',
           '  <object id="%d" p:UUID="%s" type="model">\n   <mesh>\n    <vertices>\n' % (o['iid'], U())]
    out += ['     <vertex x="%g" y="%g" z="%g"/>\n' % v for v in verts]
    out.append('    </vertices>\n    <triangles>\n')
    out += ['     <triangle v1="%d" v2="%d" v3="%d"/>\n' % tuple(t) for t in tris]
    out.append('    </triangles>\n   </mesh>\n  </object>\n </resources>\n <build/>\n</model>\n')
    return ''.join(out)


model = [HEAD, ' <metadata name="Application">BambuStudio-02.02.01.60</metadata>\n',
         ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n',
         ' <metadata name="Title">Dual-Spool Dry Box - complete print kit</metadata>\n',
         ' <metadata name="License">CC BY-SA 4.0</metadata>\n <resources>\n']
for o in objects:
    model.append('  <object id="%d" p:UUID="%s" type="model">\n   <components>\n'
                 '    <component p:path="/3D/Objects/object_%d.model" objectid="%d" p:UUID="%s" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>\n'
                 '   </components>\n  </object>\n' % (o['wid'], U(), o['wid'], o['iid'], U()))
model.append(' </resources>\n <build p:UUID="%s">\n' % U())
for o in objects:
    model.append('  <item objectid="%d" p:UUID="%s" transform="1 0 0 0 1 0 0 0 1 %.4f %.4f %.4f" printable="1"/>\n'
                 % ((o['wid'], U()) + o['t']))
model.append(' </build>\n</model>\n')

cfg = ['<?xml version="1.0" encoding="UTF-8"?>\n<config>\n']
for o in objects:
    cfg.append('  <object id="%d">\n    <metadata key="name" value="%s"/>\n    <metadata key="extruder" value="1"/>\n'
               '    <metadata face_count="%d"/>\n    <part id="%d" subtype="normal_part">\n'
               '      <metadata key="name" value="%s"/>\n      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>\n'
               '      <mesh_stat face_count="%d" edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>\n'
               '    </part>\n  </object>\n' % (o['wid'], o['name'], o['ntri'], o['iid'], o['name'], o['ntri']))
ident = 100
for p, (pname, _) in enumerate(PLATES):
    cfg.append('  <plate>\n    <metadata key="plater_id" value="%d"/>\n    <metadata key="plater_name" value="%s"/>\n'
               '    <metadata key="locked" value="false"/>\n' % (p + 1, pname))
    for o in (o for o in objects if o['plate'] == p):
        ident += 1
        cfg.append('    <model_instance>\n      <metadata key="object_id" value="%d"/>\n      <metadata key="instance_id" value="0"/>\n'
                   '      <metadata key="identify_id" value="%d"/>\n    </model_instance>\n' % (o['wid'], ident))
    cfg.append('  </plate>\n')
cfg.append('</config>\n')

REL = 'http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel'
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml',
               '<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
               ' <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n'
               ' <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>\n'
               ' <Default Extension="png" ContentType="image/png"/>\n <Default Extension="config" ContentType="text/xml"/>\n</Types>\n')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
               ' <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="%s"/>\n</Relationships>\n' % REL)
    z.writestr('3D/3dmodel.model', ''.join(model))
    z.writestr('3D/_rels/3dmodel.model.rels',
               '<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
               + ''.join(' <Relationship Target="/3D/Objects/object_%d.model" Id="rel-%d" Type="%s"/>\n' % (o['wid'], i + 1, REL)
                         for i, o in enumerate(objects)) + '</Relationships>\n')
    for o in objects:
        z.writestr('3D/Objects/object_%d.model' % o['wid'], mesh_xml(o))
    z.writestr('Metadata/model_settings.config', ''.join(cfg))

for p, (pname, _) in enumerate(PLATES):
    print('plate %d: %-55s %d parts' % (p + 1, pname, sum(o['plate'] == p for o in objects)))
print('wrote', OUT)
