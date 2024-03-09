FROM python:3.9-alpine
LABEL maintainer="shivam"
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
ENV PORT=8081
# Define environment variables for MySQL connection
# ENV MYSQL_HOST=localhost
# ENV MYSQL_USER=test
# ENV MYSQL_PASSWORD=12345678
# ENV MYSQL_DB=pharmaco
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
