python3 refresh.py

python3 ingestStreamThreaded.py \
--maxalert 1000 \
--nthread 1 \
--group LASAIR-DEV2 \
--host 192.41.108.22 \
--topic ztf_20200204_programid1

mysql --user=ztf --database=ztf --password=123password < output_csv.sql

sudo mv /var/lib/mysql-files/out.txt /home/ubuntu/scratch

out=`hostname`.txt
time scp /home/ubuntu/scratch/out.txt 192.168.140.23:scratch/$out

time ssh 192.168.140.23 "python3 /home/ubuntu/LasairTech/database_tests/ingest/in.py $out"
