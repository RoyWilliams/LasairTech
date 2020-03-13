ansible-playbook --inventory-file=hosts.yml everyone.yml
ansible-playbook --inventory-file=hosts.yml kafka.yml
ansible-playbook --inventory-file=hosts.yml blobs.yml
ansible-playbook --inventory-file=hosts.yml ingest_blobs.yml

