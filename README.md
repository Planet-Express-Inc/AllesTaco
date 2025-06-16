# Alles Taco - API v1.0

![CAlles Taco](https://github.com/Planet-Express-Inc/AlletTaco/blob/b112a78ea47c88eaff629c93e72ff0dd0527acc5/Multi/Bilder/taco_logo.png)

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