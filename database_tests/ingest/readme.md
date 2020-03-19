# Parallel Kafka Ingestion to a Database

> A set of worker nodes read Kafka into a local MySQL, then they push to a master MySQL on the archive node.

### Setting up the databases
* create_candidates.sql
** Makes the candidates table for ZTF alerts.  This is built on the worker nodes and on the archive node.

### Running the ingestion
Both worker nodes and archive nodes use the settings.py file, with miscellaneous information
* settings.py

A single batch ingestion can be run with this code. It pulls a batch of alerts, puts them into a local MySQL, 
then copies that data to the archive node, where it is put into the master database. Note there are 
two levels of parallelism: each of many worker nodes can run multiple threads.
* ingest.py
 * ingestStreamThreaded.py
 * alertConsumer.py
 * date_nid.py
 * mag.py

This code runs continual ingestion batches, logging into the node-local file system.
* ingest_log.py

This SQL code is used to build a CSV file from the local database, which is pushed by scp to 
the archive node.
* output_csv.sql

This code runs on the archive node to ingest a CSV file. The node makes it run by ssh.
* archive_in.py

This deletes all candidates from the loacl database, once the batch is ingested to the master.
* refresh.py
