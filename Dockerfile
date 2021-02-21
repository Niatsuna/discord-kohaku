FROM python:3.7-buster

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python3 app.py $BOT_TOKEN $FIRE_PRIVATE_KEY_ID \"$FIRE_PRIVATE_KEY\" $FIRE_CLIENT_ID"]
