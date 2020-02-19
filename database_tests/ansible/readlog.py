import sys, os
import json

if len(sys.argv) < 2:
    print('Usage readlogs.py date: example: readlogs.py 20200216')
    sys.exit()
date = sys.argv[1]

result = {}
for dir in os.listdir('/home/ubuntu'):
    if not dir.startswith('192'):
        continue

    print('host %s' % dir)
    Ls = []
    cmd = 'cd /home/ubuntu/%s; tar xfz logs.tgz' % dir
    print (cmd)
    os.system(cmd)

    filename = '/home/ubuntu/%s/logs/ztf_%s_programid1.log' % (dir, date)
    print(filename)
    hostrecord = []
    s = {}
    try:
        for line in open(filename).readlines():
            if not line.startswith('INGEST'):
                continue
            if 'start' in line:
                s['start'] = int(line.split()[2])
            if 'finished' in line:
                alerts = int(line.split()[4])
                s['alerts'] = alerts
            if 'duration' in line:
                run = float(line.split()[2])
                s['run'] = run
            if 'run' in s:
                if 'alerts' in s and alerts > 0:
                    hostrecord.append(s)
                s = {}
    except:
        print('Found %d records in %s' % (len(hostrecord), dir))
    result[dir] = hostrecord

print(json.dumps(result, indent=2))
