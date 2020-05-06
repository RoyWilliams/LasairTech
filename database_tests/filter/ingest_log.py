"""
This code will run forever on the worker nodes. It repeatedly runs the ingest.py
script, each time getting a batch of alerts into the local database, then flushing 
those to the master database. Logging output goes to a file coded by date.
If there were alerts, it runs again immediately, if not it waits before trying again.
"""
import sys
import settings
import date_nid

from subprocess import Popen, PIPE
import time

while 1:
    if len(sys.argv) > 1:
        nid = int(sys.argv[1])
    else:
        nid  = date_nid.nid_now()

    date = date_nid.nid_to_date(nid)
    topic  = 'ztf_' + date + '_programid1'
    fh = open('/home/ubuntu/logs/' + topic + '.log', 'a')

    args = ['python3', 'ingest.py']
    if nid: args.append('%d'%nid)
    process = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    rc = process.returncode

    stdout = stdout.decode('utf-8')
    fh.write(stdout)
    stderr = stderr.decode('utf-8')
    fh.write(stderr)

    if rc == 1:  # no more to get
        fh.write("END waiting %d seconds ...\n\n" % settings.INGEST_WAIT_TIME)
        fh.close()
        time.sleep(settings.INGEST_WAIT_TIME)
    else:
        fh.write("END getting more ...\n\n")
        fh.close()
