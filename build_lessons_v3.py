import json

items = json.load(open('g11_all_items.json'))
remaining = [it for it in items if not it.get('done_already')]
codes = [it['code'] for it in remaining]
by_code = {it['code']: it for it in remaining}

cls = json.load(open('classification.json'))
PAIRS = [tuple(p) for p in cls['PAIRS']]
pair_start = {a: b for a, b in PAIRS}
pair_members = set()
for a, b in PAIRS:
    pair_members.add(a); pair_members.add(b)

links = json.load(open('/home/claude/g11_planner/g12_reference_links.json'))
links_by_code = {l['code']: l for l in links}

def item_payload(code):
    it = by_code[code]
    lk = links_by_code.get(code, {})
    return {
        'code': code,
        'text': it['text'],
        'level': it['level'],
        'topic': it['topic_code'],
        'slidesUrl': lk.get('slides_url', ''),
        'exitTicketUrl': lk.get('exit_url', ''),
    }

# Build content lesson "units" (1 or 2 items) in original sequence order.
units = []
i = 0
while i < len(codes):
    c = codes[i]
    if c in pair_start:
        partner = pair_start[c]
        assert codes[i+1] == partner
        units.append([c, partner])
        i += 2
    elif c in pair_members:
        # second half of a pair already consumed
        i += 1
    else:
        units.append([c])
        i += 1

print('content lesson units:', len(units))
assert sum(len(u) for u in units) == 110

d = json.load(open('debug_summary.json'))
all_slots = d['all_slots']
ia_slots = {s['date'] for s in d['ia_slots']}
assessment_dates = {s['date'] for s in d['assessment_fridays']}
content_capable = d['content_capable_slots']  # list of slot dicts, in date order

n_total = len(content_capable)
n_units = len(units)
n_buffer = n_total - n_units
print('content_capable slots:', n_total, ' units needed:', n_units, ' buffer:', n_buffer)
assert n_buffer >= 0

# Evenly distribute n_buffer buffer slots across the n_total content-capable slots
# (Bresenham-style spacing), same approach used for the original build.
buffer_positions = set()
for pos in range(n_total):
    if ((pos + 1) * n_buffer) // n_total != (pos * n_buffer) // n_total:
        buffer_positions.add(pos)
assert len(buffer_positions) == n_buffer

lessons = []
unit_i = 0
for pos, slot in enumerate(content_capable):
    base = {'date': slot['date'], 'day': slot['day'], 'period': slot['period'], 'time': slot['time']}
    if pos in buffer_positions:
        lessons.append({**base, 'type': 'buffer', 'items': [], 'completed': False,
                         'slidesUrl': '', 'exitTicketUrl': ''})
    else:
        unit = units[unit_i]; unit_i += 1
        lessons.append({**base, 'type': 'content',
                         'items': [item_payload(c) for c in unit],
                         'completed': False})
assert unit_i == len(units)

# Assessment lessons: assessedCodes = every content code taught strictly before this
# assessment's date, and strictly after the previous assessment's date (or from the
# start, for the first assessment).
content_lessons_sorted = sorted([l for l in lessons if l['type'] == 'content'], key=lambda l: l['date'])
assessment_fridays_sorted = sorted(d['assessment_fridays'], key=lambda s: s['date'])

prev_date = None
for slot in assessment_fridays_sorted:
    lo = prev_date
    hi = slot['date']
    assessed = []
    for cl in content_lessons_sorted:
        if cl['date'] < hi and (lo is None or cl['date'] > lo):
            assessed.extend(i['code'] for i in cl['items'])
    lessons.append({'date': slot['date'], 'day': slot['day'], 'period': slot['period'], 'time': slot['time'],
                     'type': 'assessment', 'items': [], 'assessedCodes': assessed, 'completed': False,
                     'slidesUrl': '', 'exitTicketUrl': ''})
    prev_date = slot['date']

for slot in d['ia_slots']:
    lessons.append({'date': slot['date'], 'day': slot['day'], 'period': slot['period'], 'time': slot['time'],
                     'type': 'ia', 'items': [], 'completed': False, 'slidesUrl': '', 'exitTicketUrl': ''})

lessons.sort(key=lambda l: (l['date'], l['period']))

print('total lessons:', len(lessons))
from collections import Counter
print(Counter(l['type'] for l in lessons))
print('bundle (2-item) lessons:', sum(1 for l in lessons if l['type']=='content' and len(l['items'])>1))

json.dump(lessons, open('g11_lessons_v3.json', 'w'), indent=None)
print('written g11_lessons_v3.json')
