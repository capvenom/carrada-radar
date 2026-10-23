"""Inspect CARRADA annotations: labels, object counts, dense-point stats."""
import collections
import json
import os

ROOT = os.environ.get('CARRADA_ROOT', '/data/xysun/Carrada')
ann = json.load(open(os.path.join(ROOT, 'annotations_frame_oriented.json')))

labels = collections.Counter()
per_frame = collections.Counter()
tot_obj = tot_frames = tot_annot = 0
dense_len = []
no_label = 0
sample = None
box_wh = []

for seq in sorted(ann):
    frames = ann[seq]
    tot_frames += len(frames)
    for fid in sorted(frames):
        objs = frames[fid]
        if objs:
            tot_annot += 1
        per_frame[len(objs)] += 1
        for oid, obj in objs.items():
            tot_obj += 1
            if sample is None:
                sample = (seq, fid, oid, sorted(obj.keys()))

            rd = obj.get('range_doppler', {})
            lab = rd.get('label', None)
            if lab is None:
                no_label += 1
            labels[lab] += 1

            if 'dense' in rd:
                dense_len.append(len(rd['dense']))
            box = rd.get('box')
            if box:
                box_wh.append((abs(box[1][0] - box[0][0]) + 1, abs(box[1][1] - box[0][1]) + 1))

print('frames total     :', tot_frames)
print('frames annotated :', tot_annot, '(%.1f%%)' % (100.0 * tot_annot / max(tot_frames, 1)))
print('objects total    :', tot_obj)
print('objects no label :', no_label)
print()
print('label counts     :')
for k, v in sorted(labels.items(), key=lambda kv: str(kv[0])):
    print('   label %-6s : %d' % (str(k), v))
print()
print('objects per frame:', dict(sorted(per_frame.items())))
print()
print('dense points per object:')
if dense_len:
    print('   min %d  max %d  mean %.1f' % (min(dense_len), max(dense_len), sum(dense_len) / len(dense_len)))
print('box size mean: %.1f x %.1f' % (
    sum(w for w, h in box_wh) / max(len(box_wh), 1),
    sum(h for w, h in box_wh) / max(len(box_wh), 1)))
print()
print('sample object keys:', sample)

for seq in sorted(ann):
    for fid in sorted(ann[seq]):
        objs = ann[seq][fid]
        if objs:
            oid = sorted(objs)[0]
            print()
            print('sample object (%s / %s / %s):' % (seq, fid, oid))
            print(json.dumps(objs[oid], indent=1)[:1200])
            raise SystemExit
