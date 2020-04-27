# LasairTech
Kafka testing

`$ git clone https://github.com/RoyWilliams/LasairTech.git`

`$ cd LasairTech/kafkatests`

`$ git clone https://github.com/ZwickyTransientFacility/ztf-avro-alert.git`

Use a new 'group' argument in the command to start again

Run the code ingest.py many times like this

`for i in {1..20}`

`do`

`python ingest.py --maxalert 10000 --nthread 1 \`

`    --timeout 60 --group LASAIR8 --host 192.41.108.22 --topic ztf_test`

`done`
