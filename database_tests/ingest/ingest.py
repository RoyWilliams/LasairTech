import os,sys
from socket import gethostname
import settings
import date_nid

if len(sys.argv) > 1:
    nid = int(sys.argv[1])
else:
    nid  = date_nid.nid_now()

date = date_nid.nid_to_date(nid)
topic  = 'ztf_' + date + '_programid1'

os.system('date')
print('--------------- CLEAR LOCAL CACHES ------------')
cmd = 'python3 refresh.py'
os.system(cmd)

print('--------------- INGEST FROM KAFKA ------------')
os.system('date')
print("Topic is %s, nid is %d" % (topic, nid))

cmd =  'python3 ingestStreamThreaded.py '
cmd += '--maxalert %d ' % settings.KAFKA_MAXALERTS
cmd += '--nthread %d '  % settings.KAFKA_THREADS
cmd += '--group %s '    % settings.KAFKA_GROUPID
cmd += '--host %s '     % settings.KAFKA_PRODUCER
cmd += '--topic ' + topic

os.system('date')
print('--------------- MAKE CSV ------------')
cmd = 'mysql --user=ztf --database=ztf --password=%s < output_csv.sql' % settings.DB_PASS_WRITE
os.system(cmd)
cmd = 'mv /var/lib/mysql-files/out.txt /home/ubuntu/scratch'
os.system(cmd)
out = gethostname()

print('--------------- COPY INGEST TO ARCHIVE ------------')
cmd = 'scp /home/ubuntu/scratch/out.txt %s:scratch/%s' % (settings.DB_HOST_REMOTE, out)
os.system(cmd)

cmd = 'ssh %s "python3 /home/ubuntu/LasairTech/database_tests/ingest/in.py %s"' % (settings.DB_HOST_REMOTE, out)
os.system(cmd)
os.system('date')
