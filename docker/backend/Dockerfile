FROM docker.io/python:3.11

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./api.py" ]

EXPOSE 5000
