import sys
import settings
import date_nid


from subprocess import Popen, PIPE
import time


while 1:
    nid  = date_nid.nid_now()
    date = date_nid.nid_to_date(nid)
    topic  = 'ztf_' + date + '_programid1'
    fh = open('/home/ubuntu/logs/' + topic + '.log', 'a')

    process = Popen(['python3', 'ingest.py'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    rc = process.returncode

    stdout = stdout.decode('utf-8')
    fh.write(stdout)
    stderr = stderr.decode('utf-8')
    fh.write(stderr)
    print('written')

    if rc == 1:  # no more to get
        fh.write("waiting %d seconds ..." % settings.INGEST_WAIT_TIME)
        fh.close()
        time.sleep(settings.INGEST_WAIT_TIME)
    else:
        fh.close()
