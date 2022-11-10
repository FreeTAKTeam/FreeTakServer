FROM ubuntu:20.04

LABEL maintainer="FreeTAKTeam"

ARG FTS_VERSION=1.9.9.2

# UTC for buildtimes
RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime

#APT
RUN apt-get update && \
    apt-get install -y libssl-dev libffi-dev curl python3 python3-pip \
            libxml2-dev libxslt-dev python3-lxml python3-dev \
            python3-setuptools build-essential iproute2 &&\
    rm -rf /var/lib/apt/lists/*


#PIP3
RUN pip3 install supervisor &&\
    pip3 install requests &&\
    pip3 install FreeTAKServer==${FTS_VERSION} && \
    pip3 install defusedxml &&\
    pip3 install pyopenssl &&\
    pip3 install pytak

# Create FTS user
RUN addgroup --gid 1000 fts && \
    adduser --disabled-password --uid 1000 --ingroup fts --home /home/fts fts

# Supervisord conf
COPY support/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# Logrotation
COPY support/ftsrotate /etc/logrotate.d/ftsrotate

COPY support/fatalexit /usr/local/bin/fatalexit
RUN  chmod +x /usr/local/bin/fatalexit


# Start script
# This handles env variables and starts the service
COPY support/start-fts.sh /start-fts.sh
RUN chmod +x /start-fts.sh

# FTS ports
EXPOSE 8080
EXPOSE 8087
EXPOSE 8089
EXPOSE 8443
EXPOSE 9000
EXPOSE 19023

# FTS MainConfig changes
RUN sed -i 's+first_start = .*+first_start = False+g' /usr/local/lib/python3.8/dist-packages/FreeTAKServer/controllers/configuration/MainConfig.py   &&\
    sed -i 's/\r$//' /start-fts.sh

VOLUME ["/data"]
RUN mkdir /data && chown 1000:1000 /data && chmod 700 /data

COPY support/FTSConfig.yaml /opt/FTSConfig.yaml

ENV APPIP=0.0.0.0

# Use non root user
#USER fts

ENTRYPOINT ["/bin/bash", "/start-fts.sh"]
