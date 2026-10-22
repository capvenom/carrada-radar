"""Visualize one CARRADA frame: RD map with bounding boxes."""
import glob
import json
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

DATA_ROOT = os.environ.get('CARRADA_ROOT', '/data/xysun/Carrada')
SEQ = os.environ.get('CARRADA_SEQ', '2019-09-16-12-52-12')
OUT_DIR = os.environ.get('OUT_DIR', 'outputs')

R = os.path.join(DATA_ROOT, SEQ)
ann = json.load(open(os.path.join(R, 'annotations/box/range_doppler_light.json')))
frames = sorted(ann)

n_npy = len(glob.glob(os.path.join(R, 'range_doppler_numpy', '*.npy')))
print('npy frames :', n_npy)
print('annotated  :', len(frames), frames[0], frames[-1])

fid = frames[0]
rd = np.load(os.path.join(R, 'range_doppler_numpy', fid + '.npy'))
print('rd shape   :', rd.shape, round(float(rd.min()), 1), round(float(rd.max()), 1))
print('boxes      :', ann[fid]['boxes'])
print('labels     :', ann[fid]['labels'])

fig, ax = plt.subplots(figsize=(5, 9))
ax.imshow(rd, aspect='auto', origin='lower', cmap='jet')

for b, l in zip(ann[fid]['boxes'], ann[fid]['labels']):
    rmin, dmin, rmax, dmax = b
    ax.add_patch(patches.Rectangle((dmin, rmin), dmax - dmin, rmax - rmin,
                                   fill=False, edgecolor='lime', linewidth=1.5))
    ax.text(dmin, rmin, ' ' + str(l), color='lime', fontsize=9)

ax.set_xlabel('doppler bin')
ax.set_ylabel('range bin')
ax.set_title('frame ' + fid)
plt.tight_layout()

os.makedirs(OUT_DIR, exist_ok=True)
out = os.path.join(OUT_DIR, 'viz_' + fid + '.png')
plt.savefig(out, dpi=150)
print('saved      :', os.path.abspath(out))
