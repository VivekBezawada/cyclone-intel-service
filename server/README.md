### About 
This is a flask server which will retrieve cyclone information from the database.

### How to install without docker?

#### 1. Make sure Python3 is installed

#### 2. install `virtualenv` using `pip3`

#### 3. Run `virtualenv venv` to install necessary requirements

#### 4.  `source venv/bin/activate` to Activate the environment

#### 5.  `pip3 install -r requirements.txt` will install the necessary packages

  

### How to Run ?

Simply start the application with `python3 app.py`
Alternatively go to the repository's root directory and follow instructions.

  
  

### How to install and run with docker?

Go to root directory and simply run `docker-compose up build -d`. This will take care of setting up everythinga dn runs a dev server.

  

### How to check if the service is running?

Hit `localhost:8080/sanity` to see if the service is up and running.

  

### How it works?

Postman collection is published in the root directory to fetch information.