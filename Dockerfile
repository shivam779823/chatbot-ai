FROM python:3.9-alpine
LABEL maintainer="shivam"
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
ENV PORT=8081
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app