FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    mariadb-dev \
    linux-headers \
    python3-dev \
    bash \
    curl

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "a_core.wsgi:application", "--bind", "0.0.0.0:8000"]
