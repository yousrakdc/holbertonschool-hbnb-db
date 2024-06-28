FROM python:3.8-alpine 
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev 
COPY . /app 
WORKDIR /app 
RUN pip install -r requirements.txt 
EXPOSE 5000 
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]