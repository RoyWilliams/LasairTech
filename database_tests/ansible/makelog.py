import os
import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

alldata = json.loads(open('logs.json').read())
n = len(alldata.keys())
fig, axes = plt.subplots(1, n)
j = 0
for (host, data) in alldata.items():
    start = []
    apm = []
    run = []
    for d in data:
        start.append (d['start'])
        apm.append(d['alerts']*60.0/d['run'])
        run.append   (d['run'])
    axes[j].bar(start, apm, run, align='edge')
    axes[j].set(ylabel='alerts per minute ' + host)
    axes[j].set_ylim(ymax=400)
    j += 1
plt.show()
