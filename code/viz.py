"""Visualize several annotated CARRADA RD frames, with clearly visible boxes.

Usage on the server:
    python code/viz.py                 # 4 frames
    python code/viz.py --n 6           # 6 frames
    python code/viz.py --seq <name>    # another sequence
"""
import argparse
import glob
import json
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ap = argparse.ArgumentParser()
ap.add_argument('--root', default=os.environ.get('CARRADA_ROOT', '/data/xysun/Carrada'))
ap.add_argument('--seq', default=os.environ.get('CARRADA_SEQ', '2019-09-16-12-52-12'))
ap.add_argument('--n', type=int, default=4, help='how many frames to draw')
ap.add_argument('--out', default='outputs/viz_grid.png')
args = ap.parse_args()

R = os.path.join(args.root, args.seq)
ann = json.load(open(os.path.join(R, 'annotations/box/range_doppler_light.json')))
frames = sorted(ann)
counts = [len(ann[fid]['boxes']) for fid in frames]
n_npy = len(glob.glob(os.path.join(R, 'range_doppler_numpy', '*.npy')))

print('sequence   :', args.seq)
print('npy frames :', n_npy)
print('annotated  :', len(frames), frames[0], frames[-1], '(%.1f%%)' % (100.0 * len(frames) / n_npy))
print('boxes      : total %d, per frame min %d max %d' % (sum(counts), min(counts), max(counts)))

picked = [frames[i] for i in np.linspace(0, len(frames) - 1, args.n).astype(int)]

ncol = 2
nrow = int(np.ceil(len(picked) / float(ncol)))
fig, axes = plt.subplots(nrow, ncol, figsize=(4.2 * ncol, 6.2 * nrow), squeeze=False)

for ax, fid in zip(axes.ravel(), picked):
    rd = np.load(os.path.join(R, 'range_doppler_numpy', fid + '.npy'))
    vmin, vmax = np.percentile(rd, 50), np.percentile(rd, 99.9)
    ax.imshow(rd, aspect='auto', origin='lower', cmap='jet', vmin=vmin, vmax=vmax)

    ax.axvline(rd.shape[1] // 2, color='cyan', ls='--', lw=0.9, alpha=0.7)

    for b, l in zip(ann[fid]['boxes'], ann[fid]['labels']):
        rmin, dmin, rmax, dmax = b
        pad = 1.5
        ax.add_patch(patches.Rectangle((dmin - pad, rmin - pad),
                                       (dmax - dmin) + 2 * pad, (rmax - rmin) + 2 * pad,
                                       fill=False, edgecolor='white', linewidth=2.5))
        ax.text(dmin - pad, rmax + pad + 1, str(l), color='black', fontsize=8,
                bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none'))

    ax.set_title('%s   boxes=%d' % (fid, len(ann[fid]['boxes'])), fontsize=9)
    ax.set_xlabel('doppler bin', fontsize=8)
    ax.set_ylabel('range bin', fontsize=8)
    ax.tick_params(labelsize=7)

for ax in axes.ravel()[len(picked):]:
    ax.axis('off')

plt.tight_layout()
outdir = os.path.dirname(args.out)
if outdir:
    os.makedirs(outdir, exist_ok=True)
plt.savefig(args.out, dpi=130)
print('drawn      :', ' '.join(picked))
print('saved      :', os.path.abspath(args.out))
