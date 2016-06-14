from copy import deepcopy
import json
import requests

numpy100 = requests.get('https://raw.githubusercontent.com/rougier/numpy-100/master/README.rst')

qs = []
currq = None
for l in numpy100.text.split('\n'):
    if l.startswith('#.'):
        currq = [l[2:].strip()]
    elif currq is not None:
        if '.. code-block:: python' in l:
            q = ' '.join(currq)
            idx = q.rfind('(')
            if idx != -1:
                q = q[:idx]
            if not q.endswith('?'):
                q = q + '?'
            qs.append(q.strip())
            currq = None
        else:
            currq.append(l.strip())


with open('numpy-100.templ') as f:
    j = json.load(f)

cells = j['cells']
for i, cell in enumerate(cells):
    if '<question>' in ''.join(cell['source']):
        qidx = i
    if '<answer>' in ''.join(cell['source']):
        aidx = i

qcell = cells[qidx]
acell = cells[aidx]
acell['source'] = ''

del cells[aidx]
del cells[qidx]

for i, q in enumerate(qs):
    cell = deepcopy(qcell)
    cell['source'][0] = cell['source'][0].replace('<question>', str(i+1) + ': ' + q)
    cells.append(cell)
    cells.append(acell)


with open('numpy100-qs.ipynb', 'w') as f:
    json.dump(j, f)
