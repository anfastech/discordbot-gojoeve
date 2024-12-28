FROM python:3.12-slim

COPY ./Source/requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./Source/bot.py ./

CMD ["python3", "bot.py"]

# CMD ["python", "bot.py"]
