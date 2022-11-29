FROM python:3.11 as builder


LABEL maintainer="FreeTAKTeam <FreeTAKTeam@gmail.com>"
LABEL org.opencontainers.image.source="https://github.com/FreeTAKTeam/FreeTakServer"
LABEL org.opencontainers.image.licenses="EPL-2.0"
LABEL org.opencontainers.image.description="FTS is a Python3 implementation of the TAK Server for devices like ATAK, WinTAK, and ITAK, it is cross-platform and runs from a multi node installation on AWS down to the Android edition."

ARG FTS_VERSION
ENV FTS_VERSION=${FTS_VERSION}

# UTC for buildtimes

#PIP3
COPY setup.py /tmp
COPY README.md /tmp
RUN python -m pip install --upgrade pip && \
    cd /tmp && python setup.py egg_info && \
    pip install -r FreeTAKServer.egg-info/requires.txt

COPY FreeTAKServer/ /usr/local/lib/python3.11/site-packages/FreeTAKServer/

FROM python:3.11 as image

RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

# Create FTS user
RUN addgroup --gid 1000 fts && \
    adduser --disabled-password --uid 1000 --ingroup fts --home /home/fts fts

# Supervisord conf
RUN pip install supervisor
COPY support/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# Logrotation
COPY support/ftsrotate /etc/logrotate.d/ftsrotate

COPY support/fatalexit /usr/local/bin/fatalexit

# Start script
# This handles env variables and starts the service
COPY support/start-fts.sh /start-fts.sh

# FTS ports
EXPOSE 8080
EXPOSE 8087
EXPOSE 8089
EXPOSE 8443
EXPOSE 9000
EXPOSE 19023

# FTS MainConfig changes
# RUN sed -i 's+first_start = .*+first_start = False+g' /usr/local/lib/python3.11/site-packages/FreeTAKServer/controllers/configuration/MainConfig.py   &&\
#     sed -i 's/\r$//' /start-fts.sh

VOLUME ["/data"]
RUN mkdir /data && chown 1000:1000 /data && chmod 700 /data

COPY support/FTSConfig.yaml /opt/FTSConfig.yaml

ENV APPIP=0.0.0.0

# Use non root user
#USER fts

ENTRYPOINT ["/bin/bash", "/start-fts.sh"]
