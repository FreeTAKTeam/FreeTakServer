FROM python:3

WORKDIR /app

COPY TAKfreeServer/requirements.txt ./TAKfreeServer/requirements.txt
RUN pip install -r ./TAKfreeServer/requirements.txt

COPY . .
RUN sed -i 's/Your IP/0.0.0.0/g' TAKfreeServer/constants.py

EXPOSE 8080
EXPOSE 8087

ENTRYPOINT [ "python", "TAKfreeServer/run.py", "-p", "8087" ]