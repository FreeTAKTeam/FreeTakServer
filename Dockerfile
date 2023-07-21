FROM python:3.8

# don't use root, let's not have FTS be used as a priv escalation in the wild
RUN groupadd -r freetak && useradd -m -r -g freetak freetak
RUN mkdir /opt/fts ; chown -R freetak:freetak /opt/fts ; chmod a+w /var/log
USER freetak

# This needs the trailing slash
ENV FTS_DATA_PATH="/opt/fts/"

WORKDIR /app

RUN pip3 install flask lxml flask_login

COPY --chown=freetak:freetak ./requirements.txt setup.py README.md ./
RUN pip3 install -e /app

COPY --chown=freetak:freetak . ./

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
# APIPort
EXPOSE 19023

#ENTRYPOINT [ "python", "TAKfreeServer/run.py", "-p", "8087" ]
CMD [ "python3", "-m", "FreeTAKServer.controllers.services.FTS", "-DataPackageIP", "0.0.0.0", "-AutoStart", "True"]
