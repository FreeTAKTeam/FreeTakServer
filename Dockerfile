FROM python:3.8-slim-buster

RUN useradd -m -s /bin/bash freetak
RUN mkdir /opt/FTSData && chown -R freetak:freetak /opt/FTSData
USER freetak

ENV FTS_DATA_PATH="/opt/FTSData/"

WORKDIR /FreeTAKServer
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080 8087 8089 8443 9000 19023

ENTRYPOINT [ "python3", "-m", "FreeTAKServer.controllers.services.FTS", "-DataPackageIP", "0.0.0.0", "-AutoStart", "True"]
