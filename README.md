# Alles Taco - API v1.0

![CAlles Taco](https://github.com/Planet-Express-Inc/AllesTaco/blob/master/frontend/allestaco_logo.png?raw=true)

## Installation
### Debian/Ubuntu
Install git, docker and docker-compose.

```
sudo apt-get update
sudo apt-get install git docker.io docker-compose
```

You can also install the latest version of docker by unsing the official documentation.

Add your user to the docker group:

```
sudo usermod -a -G docker john
```
"john" is an example. To use docker commands, it is sometimes nessasary to reload your shell.

Clone the repository
```
git clone https://github.com/Planet-Express-Inc/AlletTaco.git
cd AlletTaco
```

## Getting started
### Certificate setup
You need a working SSL/TLS Certificate.
Name them like:
fullchain.pem
privkey.pem

```
cp /your/cert/fullchain.pem docker/cert/fullchain.pem
cp /your/cert/privkey.pem docker/cert/privkey.pem
chmod +r docker/*.pem
```

### Configure CORS origins and cookie secret
You have to change your URL in order to have CORS working.
Edit.
```
backend/config.py
```
Add your frontend URL and your own cookie secrert.
```
# Origins for CORS
origins=["https://yourdomain.com"]

# Secret for cookies
secret_key = "super_secret_124g+#f43g"
```

### Copy database template
Copy the database template file for later use in container.
```
cp database_creation/allestacoDB_template.sql database/allestacoDB_template.sql
```

### Build and start all containers
```
cd docker
docker-compose build
docker-compose up -d
```

### Load in database template
Copy the root password for the database, you will need it later for the creation of the database.
```
cat docker/docker-compose.yml | grep "MYSQL_ROOT_PASSWORD:"
```

Load in the template.
```
docker exec -it tacodb /bin/bash
mariadb -u root -p < /var/lib/mysql/allestacoDB_template.sql
exit
```

### Restart containers
If you have to restart the containers use:
```
cd docker
./restart.sh
```

## API docs
You can see the Swagger documentation for the API at:
```
https://yourdomain.com:5000/apidocs/
```

## Frontend
You can see the README.md for the frontend in:
```
frontend/README.md
```
