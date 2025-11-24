#!/bin/bash
export PATH=$PATH:/opt/keycloak/bin

curl --head -fsS http://localhost:9000/health/ready
sleep 60

kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin

kcadm.sh create clients -r master -s clientId=tiled -s enabled=true -s clientAuthenticatorType=client-secret -s secret=d0b8122f-8dfb-46b7-b68a-f5cc4e25d000

for user in alice bob carol oscar; do
  kcadm.sh create users -r master -s username="$user" -s enabled=true
  kcadm.sh set-password -r master --username "$user" --new-password "$user"
done
