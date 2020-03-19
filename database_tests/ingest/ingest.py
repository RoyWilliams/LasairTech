"""
This script is meant to run in parallel on the ingest nodes of the LasairTech 
cluster. It runs a subprocess ingestStreamThreaded that pulls Kafka alerts,
which processes the alerts, then puts them into a local MySQL database.
When that is finished, a CSV file is made from the database, and pushed 
(with scp) to the archive node that has the master database.
"""

import os,sys
import time
from socket import gethostname
from datetime import datetime
import settings
import date_nid

if len(sys.argv) > 1:
    nid = int(sys.argv[1])
else:
    nid  = date_nid.nid_now()

date = date_nid.nid_to_date(nid)
topic  = 'ztf_' + date + '_programid1'

os.system('date')
print('clear local caches')
cmd = 'python3 refresh.py'
os.system(cmd)

print('INGEST start %s' % datetime.utcnow().strftime("%H:%M:%S"))
print('ingest from kafka')
print("Topic is %s, nid is %d" % (topic, nid))
t = time.time()

cmd =  'python3 ingestStreamThreaded.py '
cmd += '--maxalert %d ' % settings.KAFKA_MAXALERTS
cmd += '--nthread %d '  % settings.KAFKA_THREADS
cmd += '--group %s '    % settings.KAFKA_GROUPID
cmd += '--host %s '     % settings.KAFKA_PRODUCER
cmd += '--topic ' + topic

# Run the ingestion
print(cmd)
os.system(cmd)
print('INGEST duration %.1f seconds' % (time.time() - t))

# The command that makes the CSV file
t = time.time()
print('SEND to ARCHIVE')
cmd = 'mysql --user=ztf --database=ztf --password=%s < output_csv.sql' % settings.DB_PASS_WRITE
os.system(cmd)

outfile = '/home/ubuntu/scratch/out.txt'
cmd = 'mv /var/lib/mysql-files/out.txt %s' % outfile
os.system(cmd)

# Detect if nothing came from the ingest; if so exit
if os.path.exists(outfile) and os.stat(outfile).st_size == 0:
    print('SEND outfile is empty')
    print('SEND %.1f seconds' % (time.time() - t))
    sys.exit(1)

# Push the CSV file to the archive node, with a name corresponding 
# to the name of this node
out = gethostname()
cmd = 'scp /home/ubuntu/scratch/out.txt %s:scratch/%s' % (settings.DB_HOST_REMOTE, out)
os.system(cmd)

# Run the command on the archive node to read in the CSV file 
# to the master database
cmd = 'ssh %s "python3 /home/ubuntu/LasairTech/database_tests/ingest/archive_in.py %s"' % (settings.DB_HOST_REMOTE, out)
os.system(cmd)
print('SEND %.1f seconds' % (time.time() - t))

sys.exit(0)
