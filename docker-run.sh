#!/bin/bash

# Sharing for MainConfig.py
if [[ ! -f "/opt/fts/MainConfig.py" ]]
  then
    cp FreeTAKServer/core/configuration/MainConfig.bak /opt/fts/MainConfig.py
fi
if [[ ! -f "FreeTAKServer/core/configuration/MainConfig.py" ]]
  then
    ln -s /opt/fts/MainConfig.py FreeTAKServer/core/configuration/MainConfig.py
fi

# Sharing for FTSConfig.yaml
if [[ ! -f "/opt/fts/FTSConfig.yaml" ]]
  then
    python -c "from FreeTAKServer.core.configuration.configuration_wizard import autogenerate_config; autogenerate_config()"
fi

python -m FreeTAKServer.controllers.services.FTS