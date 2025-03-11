FROM python:3.11

WORKDIR /app/bot

COPY ./bot/requirements.txt /app/bot

RUN apt-get update
RUN apt-get install libgtk-3-0 -y
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver

RUN apt install ffmpeg -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./bot /app/bot
COPY ./songrec /app/bot

ENV PYTHONPATH=/app
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

CMD ["python", "main.py"]
