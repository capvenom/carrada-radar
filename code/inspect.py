"""Inspect CARRADA annotations across ALL sequences."""
import collections
import json
import os

ROOT = os.environ.get('CARRADA_ROOT', '/data/xysun/Carrada')

ann = json.load(open(os.path.join(ROOT, 'annotations_frame_oriented.json')))
print('sequences        :', len(ann))

rows = []
labels = collections.Counter()
tot_frames = tot_annot = tot_obj = 0
max_per_frame = 0
multi_seq = 0

for seq, frames in ann.items():
    n_frames = len(frames)
    n_annot = sum(1 for v in frames.values() if v)
    n_obj = sum(len(v) for v in frames.values())
    mx = max((len(v) for v in frames.values()), default=0)

    rows.append((seq, n_frames, n_annot, n_obj, mx))
    tot_frames += n_frames
    tot_annot += n_annot
    tot_obj += n_obj
    max_per_frame = max(max_per_frame, mx)
    if mx > 1:
        multi_seq += 1

    for v in frames.values():
        for obj in v.values():
            labels[obj.get('label', -1)] += 1

print('frames total     :', tot_frames)
print('frames annotated :', tot_annot, '(%.1f%%)' % (100.0 * tot_annot / max(tot_frames, 1)))
print('objects total    :', tot_obj)
print('max objects/frame:', max_per_frame)
print('seqs with >1 obj :', multi_seq, '/', len(ann))
print('label counts     :', dict(sorted(labels.items())))
print()
print('%-22s %7s %7s %7s %4s' % ('sequence', 'frames', 'annot', 'objs', 'max'))
print('-' * 52)
for seq, n_frames, n_annot, n_obj, mx in rows:
    print('%-22s %7d %7d %7d %4d' % (seq, n_frames, n_annot, n_obj, mx))
