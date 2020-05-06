# Dormitory Service
REST API created for working and managing with students dormitories.
Based on Django, Django-Rest-Framework.
For emails used Sendgrid service and queues worked on Celery and Redis as broker.

## Installation (For Linux (Mac), need docker):
* git clone https://github.com/antl31/Dormitory_app
* cd Dormitory_app/
* docker-compose build
* docker-compose up 
* docker exec -it django sh  
in container:
  * python3 manage.py migrate
  * python3 manage.py collectstatic
 
 ### API Endpoints:
* /users/ - user view (get,post)
* /rooms/ - room view (get,post)
* /v1/login/ - get auth token


