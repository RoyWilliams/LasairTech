"""
Settings for the LasairTech parallel ingestion.
"""

# the local and master databases have the same passwords
DB_HOST_LOCAL    = 'localhost'
DB_USER_WRITE    = 'ztf'
DB_PASS_WRITE    = '123password'
DB_DATABASE      = 'ztf'

# where to fetch data from
#KAFKA_PRODUCER  = 'public.alerts.ztf.uw.edu'
KAFKA_PRODUCER   = '192.41.108.22'

# Group ID for the fetch. All worker nodes use the same.
KAFKA_GROUPID    = 'LASAIR-DEV3'

# Threads per worker node to use in the ingestion
KAFKA_THREADS    = 1

# Wait to see if there are more
KAFKA_TIMEOUT    = 60

# Batch size
KAFKA_MAXALERTS  = 10000

# If no alerts to fetch, time to wait before retry
INGEST_WAIT_TIME = 600

# address of the archive node
DB_HOST_REMOTE   = '192.168.140.47'
