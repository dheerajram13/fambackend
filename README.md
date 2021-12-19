# Introduction

The goal of this project is to make an API to fetch latest videos sorted reverse chronological order of their publishing time from Youtube-v3 API.

# Prerequisites 
* Install Docker and Docker-compose in your machine.[Download Docker](https://docs.docker.com/get-docker/).

# How to Run using Docker 
1. Clone this repo in your machine.[Repo link](https://github.com/dheerajram13/fambackend).
2. Create a `.env` file where manage.py file with the following data. 
    ```
        SECRET_KEY=
        DEBUG=
        CELERY_BROKER=
    ```
3. On the command line, within this directory, do this to build the image and
   start the container:
   ```sh
    $ docker-compose up -d --build
    ```
4. If that's successful you can then start it up. This will start up the database and web server, and  display the Django `runserver` logs:
    ```sh
    $ docker-compose up
    ```
5. Open http://0.0.0.0:8800 or docker-machine ip:8800 in your browser.
6. Create a superuser using python manage.py createsuperuser.
7. Open the http://0.0.0.0:8800/admin and login to the site with your credentials.
8. Add the API key to the YouTubeAPI Model from the admin page.

# How to run without Docker 
1.  Clone this repo in your machine. [Repo link](https://github.com/dheerajram13/fambackend).
2. Create a `.env` file where manage.py file with the following data. 
    ```
        SECRET_KEY=
        DEBUG=
        CELERY_BROKER=
    ```
3. Install Python3 [Download Python](https://www.python.org/downloads/).
4. Install Redis [Download Redis](https://redis.io/download).
5. Create a virtual env and activate the env. 
6. Type the following commonds in your terminal:
    ```
        $ cd youtube
        pip install -r requirements.txt
        python manage.py makemigrations
        python manage.py migrate
    ```
7. Open a terminal and type following command:
    ```sh
    $ celery -A youtube worker  --pool=solo -l INFO
    ```
8. Open another terminal and type following command:
    ```sh
    $ celery -A youtube beat -l info
    ```
9. Start the web server 
    ```sh
    $ python manage.py runserver
    ```
10. Open http://localhost:8800 in your browser.
11. Create a superuser using python manage.py createsuperuser.
12. Open the http://0.0.0.0:8800/admin and login to the site with your credentials.
13. Add the API key to the YouTubeAPI Model from the admin page.

### Getting Started with the API 
*. Open http://localhost:8800/videos/ in your browser.
1. To make a search query
    * Example `/videos/?search=football`
2. To order the videos   
    * Example `/videos/?orderby=title`
    * only the following arguments can be passed:
    (`published_at`,`-published_at`,`title`,`-title`)
    * Invalid value is ignored and argument isn't considered
3. To go to the page number
    * Example `/videos/?page=2`
4. To view the videos data login to admin page. 

## Screenshots
![Default Home View](__screenshots/3.PNG?raw=true "Docker ")
![Default Home View](__screenshots/1.PNG?raw=true "Celery Worker in a seperate terminal without docker")
![Default Home View](__screenshots/2.PNG?raw=true "Celery beat in a seperate terminal without docker")
![Default Home View](__screenshots/4.PNG?raw=true "Search query")
![Default Home View](__screenshots/5.PNG?raw=true "Videos Orderby")
![Default Home View](__screenshots/6.PNG?raw=true "Page number ")
![Default Home View](__screenshots/7.PNG?raw=true "Admin View")
