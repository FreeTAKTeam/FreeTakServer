FROM python:3.11

# don't use root, let's not have FTS be used as a priv escalation in the wild
RUN groupadd -r freetak && useradd -m -r -g freetak freetak
RUN mkdir /opt/fts ; chown -R freetak:freetak /opt/fts ; chmod 775 /opt/fts ; chmod a+w /var/log

USER freetak

# This needs the trailing slash
ENV FTS_DATA_PATH = "/opt/fts/"

# Move to the FTS directory, then do the copying and unpacking
WORKDIR /home/freetak/

# Get digitalpy from git
RUN git clone https://github.com/FreeTAKTeam/DigitalPy.git digitalpy
RUN pip install /home/freetak/digitalpy

COPY --chown=freetak:freetak --chmod=774 requirements.txt setup.py README.md docker-run.sh ./

# Install pre-reqs then the base FTS
ENV PATH /home/freetak/.local/bin:$PATH
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e /home/freetak/
COPY --chown=freetak:freetak --chmod=774 . ./

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
