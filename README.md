# rss_project
Scraper RSS reading the exchange rate from the European Central Bank

Whole project is written on python 3.7. Only on this version is tested. Solution is based
on RabbitMq and celery 4.2 . Task is gathering actual currency only in relation to Euro.
Received information currency symbol, value and date. Api returns only list 
of all data. I had some issue with scheduling task. I also had idea to put all
app to docker by using docker-composer but I didn't have enough time to accomplish
that. Used database: sqilite3

1. Installation - Ubuntu 18.10

This set of commands will install docker and pull latest rabbitmq:

sudo apt install docker.io
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo usermod -aG docker $USER
sudo systemctl enable docker
sudo systemctl start docker
docker --version
docker pull rabbitmq:latest
docker run -d -p 5672:5672 -p 15672:15672 -e RABBITMQ_NODENAME=rabbitmq --name rabbitmq --hostname rabbitmq --log-driver=none rabbitmq:management


To run project there is need to create environment. Personally I am using pyenv (https://github.com/pyenv/pyenv) but
you can also use virtualenv. In above link you can get steps to configure pyenv.

pyenv install 3.7.0 
pyenv virtualenv 3.7.0 rss_env
pyenv activate rss_env
pipenv install --ignore-pipfile # This will allow you to install all project environment

2. Run project

I Start rabbitmq container - docker start rabbitmq
II Start celery worker - celery -A rss_project worker -l DEBUG
III Run python manage.py runserver
IV Run python manage.py shell and then:
from rss_project.applications.rss_reader.tasks import *
from rss_project.apps.rss_reader.tasks import read_currencies 
read_currencies.delay() - to spawn task, unfortunately for some reason scheduling is not working

You can check that currency is downloaded on api:
127.0.0.1:8000/rss_reader/api/currency/list
Points II. III, IV you must run in separate terminals.

3. Further Work
- All project it should be run in container with rabbitmq and celery
- More api where you can e.g filter by date and currency
- get rid of unnecessary files
- use configuration from celery 4.2
- fix scheduling read_currencies task.
- check whether configuration solves problem with database lock ('rate_limit': '1/s')
- check whether value field is good for all currency 
- use postgres

