# Introduction

The goal of this project is to make an API to fetch latest videos sorted reverse chronological order of their publishing time from Youtube-v3 API.

# Prerequisites 
* Install Docker and Docker-compose in your machine.[Docker link](https://docs.docker.com/get-docker/).

# How to Run using Docker 
1. Clone this repo.[Reo link](https://github.com/dheerajram13/fambackend).
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

# How to run without Docker 
1. 1. Clone this repo.[Reo link](https://github.com/dheerajram13/fambackend).
2. Create a `.env` file where manage.py file with the following data. 
    ```
        SECRET_KEY=
        DEBUG=
        CELERY_BROKER=
    ```
3. Install Python3[Python link](https://www.python.org/downloads/).
4. Install Redis[Redis link](https://redis.io/download).
5. Create a virtual env and activate the env. 
6. Type the following commonds in your terminal:
  ```sh
    $ cd youtube
    ```
    ```sh
    $ pip install -r requirements.txt
    ```
    ```sh
    $ python manage.py makemigrations
    ```
    ```sh
    $ python manage.py migrate
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

## Screenshots
<!-- ![Default Home View](__screenshots/home.png?raw=true "Title") -->
