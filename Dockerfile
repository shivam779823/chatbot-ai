FROM python:3.9-alpine

LABEL maintainer="shivam"

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=8081

CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--workers", "1", "--threads", "8", "app:app"]
