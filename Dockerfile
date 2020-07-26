
# cd "/mnt/d/Dropbox/Python Projects/covid"
# export DOCKER_CONTENT_TRUST=0
# pip freeze > requirements.txt (remender to first activate the enviroment)
# docker build -t covid-app .
# docker run --name covid-app-oman --env PUSHBULLET_KEY='key goes here' --env RAPIDAPI_KEY='key goes here' -e COUNTRY=oman -d --restart unless-stopped covid-app

FROM python:3-alpine
RUN apk update
# delete cache files
RUN rm -vrf /var/cache/apk/*

WORKDIR "/usr/src/app"

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -U setuptools pip

# Install dependencies:
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Run the application:
COPY app.py .
CMD ["python", "app.py"]