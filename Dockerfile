FROM python:3.9-bullseye

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .
COPY dashboard.py .

RUN pip install -r requirements.txt

EXPOSE 8050

CMD [ "gunicorn", "--workers=1", "--threads=1", "-b 0.0.0.0:8050", "dashboard:server"]
