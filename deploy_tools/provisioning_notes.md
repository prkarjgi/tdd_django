Provisioning a new site
===

## Required packages
- nginx
- Python 3.8
- venv and pip3
- git

e.g. on Ubuntu:
- sudo apt-add-repository ppa:deadsnakes/ppa
- sudo apt update
- sudo apt install nginx git python3.8 python3.8-venv

## Nginx Virtual Host config
- see the nginx.template.conf replace the DOMAIN term with the domain of the site e.g. staging.test-driven.prkarjgi.com

## Gunicorn Systemd Service
- see the gunicorn-systemd.template.service file and replace the DOMAIN term with the domain of the site e.g. staging.test-driven.prkarjgi.com

## Folder Structure

Assume we have a user called ubuntu with a home folder
```
/home/ubuntu/
|-- sites
    |-- DOMAIN1
    |    |-- .env
    |    |-- db.sqlite3
    |    |-- manage.py
    |        .
    |        .
    |    |-- static
    |    |--venv
    |
    |-- DOMAIN2
         |-- .env
         |-- db.sqlite3
         |-- etc

```

