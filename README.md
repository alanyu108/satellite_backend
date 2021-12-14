## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Hosted website](#hosted-website)

## General info
This project creates a Django API which connects to a MongoDB database to retrieve information about the satellite and debris.
	
## Technologies
Project is created with:
* Django
* MongoDB
	
## Setup
To run this project, first create an env file with the following variables:

```
SECRET_KEY=
MONGO_URI=
DEBUG =
```

The `SECRET_KEY` is the database secret key and can be any value of your choosing. 
The `MONGO_URI` is the connection string that MongoDB provides in order to connect to their cloud servers.
`DEBUG` is just a boolean, `True` for running in development and `False` for running in production.

Once this file is setup, `pip install` all the required packages in `requirements.txt`.

To start up a local server, run 

```
$ python manage.py runserver
```

## Hosted website

https://alanyu108-satellite-backend.herokuapp.com/api/
