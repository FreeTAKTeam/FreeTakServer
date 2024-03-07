#!/bin/bash

# Sharing for FTSConfig.yaml
if [[ ! -f "/opt/fts/FTSConfig.yaml" ]]
  then
    python -c "from FreeTAKServer.core.configuration.configuration_wizard import autogenerate_config; autogenerate_config()"
fi

python -m FreeTAKServer.controllers.services.FTS