"""Re-open a built 3MF and draw every plate from the top, to check the layout."""
import sys, zipfile, xml.etree.ElementTree as ET
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

z = zipfile.ZipFile(sys.argv[1])
ns = {'m': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
root = ET.fromstring(z.read('3D/3dmodel.model'))
cfg = ET.fromstring(z.read('Metadata/model_settings.config'))
plate_of = {}
plates = cfg.findall('plate')
for p in plates:
    pid = int(p.find("metadata[@key='plater_id']").get('value'))
    for mi in p.findall('model_instance'):
        plate_of[mi.find("metadata[@key='object_id']").get('value')] = pid
fig, axs = plt.subplots(2, 2, figsize=(10, 10))
tot = 0
for item in root.find('m:build', ns):
    oid = item.get('objectid'); t = list(map(float, item.get('transform').split()))[9:]
    mesh = ET.fromstring(z.read('3D/Objects/object_%s.model' % oid)).find('.//m:mesh', ns)
    V = [(float(v.get('x')) + t[0], float(v.get('y')) + t[1], float(v.get('z')) + t[2]) for v in mesh.find('m:vertices', ns)]
    T = [(int(r.get('v1')), int(r.get('v2')), int(r.get('v3'))) for r in mesh.find('m:triangles', ns)]
    tot += len(T)
    assert abs(min(v[2] for v in V)) < 1e-3
    p = plate_of[oid] - 1; col, row = p % 2, p // 2
    ox, oy = col * 307.2, -row * 307.2
    axs[row][col].add_collection(PolyCollection([[(V[a][0] - ox, V[a][1] - oy) for a in tr] for tr in T], facecolor='#5b6270', edgecolor='none'))
for p, ax in enumerate(axs.flat):
    if p >= len(plates):
        ax.axis('off'); continue
    ax.add_patch(plt.Rectangle((0, 0), 256, 256, fill=False, ec='r'))
    ax.set_xlim(-5, 261); ax.set_ylim(-5, 261); ax.set_aspect('equal')
    ax.set_title(plates[p].find("metadata[@key='plater_name']").get('value'), fontsize=9)
plt.tight_layout(); plt.savefig(sys.argv[2], dpi=70)
print('items', len(root.find('m:build', ns)), 'triangles', tot, 'all on bed, z-min 0')
