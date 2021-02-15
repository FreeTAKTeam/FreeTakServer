# Docker Quickstart

:warning: **THIS IS NOT WELL SUPPORTED BY THE FTS TEAM RIGHT NOW, YOU ARE IN UNCHARTED TERRITORY** :warning:

I'd like to set this repo up to use github actions to push to pip and docker hub at the same time. Until that happens, here's how you can build and use this repo to build a docker image and run a container from it. It assumes you've already cloned it where you plan to use it. It _also_ means you'll be running whatever's in development, _not_ what's been released / in Pypi. 

:warning: **That means you might be running unreleased code with this method**

## Persistence
By default, docker will save pretty much nothing between runs of this container. So before we run this, we _really_ want somewhere for FreeTAKServer to store data. This container expects you to mount that volume at `/opt/FTSData/` inside the container. Let's put this in your home directory, for now. 

```shell
# This should work for all dockers, linux, windows, etc
docker volume create ftsdata 
```

:warning: FTS will store its database, data packages, ExCheck lists, and importantly, your _certificates_ in this volume. Keep all of these safe. 

## Creating a docker image from this repo.
`docker build . -t fts:local`

## Run the container
OK, there's a lot to put in this command line, because there's lots of options we want to pass.

Let's run this interactively to start, so we can control the server. This assumes you want to use your public IP for the relevant IP Address configurations.

```shell
docker run -it \ # run the container interactively (hold the shell open)
	-e FTS_DP_ADDRESS="$(curl ifconfig.me)" \ # dynamically get your address from iconfig.me for datapackages
	--mount src=ftsdata,target=/opt/FTSData \ # mount the volume for FTSData
	-p 8080:8080 -p 8087:8087 -p 8443:8443 \ # expose ports
	-p 9000:9000 -p 19023:19023 \ #expose more ports. Check the docs for explanations
	fts:local # the container for docker to run
```

Once this is running, point your ATAK clients at it, and make sure it works. Once your sure it works, we're gonna set it to run in the background and restart all the time, unless you intentionally stop it for some reason, with `docker stop`. 

```shell 
docker run --restart unless-stopped \ # run the container forever, unless stopped intentionally
	-e FTS_DP_ADDRESS="$(curl ifconfig.me)" \ # dynamically get your address from iconfig.me for datapackages
	--mount src=ftsdata,target=/opt/FTSData \ # mount the volume for FTSData
	-p 8080:8080 -p 8087:8087 -p 8443:8443 \ # expose ports
	-p 9000:9000 -p 19023:19023 \ #expose more ports. Check the docs for explanations
	fts:local # the container for docker to run
```