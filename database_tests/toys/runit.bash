dir='LasairTech/database_tests/toys'
archive='192.168.140.23'
python3 start_again.py
python3 driver_local.py 1000000 100000
time scp /home/ubuntu/scratch/out.txt $archive:scratch
time ssh         $archive "mysql --user=ztf --password=123password < $dir/load.sql"
