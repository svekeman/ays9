#!/bin/bash

# start ays
sudo docker exec js9_base js9 'j.atyourservice.server.start()'

# sleep for 30 seconds
sleep 30

# check if the server started
sudo docker exec js9_base js9 'cli=j.clients.atyourservice.get();cli.api.ays.listRepositories()'

# validate all the schemas
pushd /root/gig/github
echo "Validating Schemas"
for schema in $(find -name schema.capnp); do
  echo "Validating $schema"
  capnp compile -oc++ $schema
end
popd
