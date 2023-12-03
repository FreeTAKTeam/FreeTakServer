FROM python:3.11

# don't use root, let's not have FTS be used as a priv escalation in the wild
RUN groupadd -r freetak && useradd -m -r -g freetak freetak
RUN mkdir /opt/fts ; chown -R freetak:freetak /opt/fts ; chmod 775 /opt/fts ; chmod a+w /var/log

USER freetak

# This needs the trailing slash
ENV FTS_DATA_PATH = "/opt/fts/"

# Move to the FTS directory, then do the copying and unpacking
WORKDIR /home/freetak/
COPY --chown=freetak:freetak --chmod=774 README.md pyproject.toml docker-run.sh ./
COPY --chown=freetak:freetak --chmod=774 FreeTAKServer/ ./FreeTAKServer/

# Install pre-reqs then the base FTS
# ruamel.yaml is very ornery and has to be force-reinstalled alone
ENV PATH /home/freetak/.local/bin:$PATH
RUN pip install --upgrade pip ; pip install setuptools wheel poetry ; pip install --force-reinstall "ruamel.yaml<0.18"
RUN pip install --no-build-isolation --editable .

# Provide a way to edit the configuration from outside the container
# May need to be updated if the base image changes
RUN cp FreeTAKServer/core/configuration/MainConfig.py FreeTAKServer/core/configuration/MainConfig.bak
RUN mv FreeTAKServer/core/configuration/MainConfig.py /opt/fts/MainConfig.py
RUN ln -s /opt/fts/MainConfig.py FreeTAKServer/core/configuration/MainConfig.py

# Open ports
# note: docker compose documentation suggests that communication between
#       core and ui doesn't need a port explicitly exposed
# DataPackagePort
EXPOSE 8080
# CoTPort
EXPOSE 8087
# SSLCoTPort
EXPOSE 8089
# SSLDataPackagePort
EXPOSE 8443
# FederationPort
EXPOSE 9000
# APIPort - Don't expose by default
#EXPOSE 19023

VOLUME /opt/fts

CMD [ "/home/freetak/docker-run.sh" ]
