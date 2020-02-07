for value in {1..2000000}
do

python3 refresh.py

python3 ingestStreamThreaded.py \
--maxalert 10000 \
--nthread 1 \
--group LASAIR-DEV2 \
--host 192.41.108.22 \
--topic ztf_20200204_programid1

mysql --user=ztf --database=ztf --password=123password < output_csv.sql

mv /var/lib/mysql-files/out.txt /home/ubuntu/scratch

if [ ! -s /home/ubuntu/scratch/out.txt ]
then
    echo 'No more alerts -- exiting'
    exit 0
fi

out=`hostname`.txt
time scp /home/ubuntu/scratch/out.txt 192.168.140.47:scratch/$out

time ssh 192.168.140.47 "python3 /home/ubuntu/LasairTech/database_tests/ingest/in.py $out"
done
