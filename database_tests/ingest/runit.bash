python3 refresh.py

python3 ingestStreamThreaded.py \
--maxalert 10000 \
--nthread 1 \
--group LASAIR-DEV2 \
--host 192.41.108.22 \
--topic ztf_20200131_programid1

mysqldbexport --server=ztf:123password@localhost:3306 --format=csv ztf --export=data > ~/scratch/out.txt

time scp /home/ubuntu/scratch/out.txt 192.168.140.23:scratch
time ssh 192.168.140.23 "mysql --user=ztf --password=123password < LasairTech/database_tests/ingest/load.sql"
