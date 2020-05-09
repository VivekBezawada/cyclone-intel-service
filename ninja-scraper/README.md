
### About
This is a flask server which will schedule cyclone information and stores to the database.
  

### How it works?

Upon hitting the API (Postman collection in the repository's root directory), a job runs to fetch active cyclones and it's infomraion on location and time. There is a also a forecast infomration which is available in some cyclones. The API takes an extra parameter to only write the information after a certain timeatamp. This helps in keeping it light weight and skipping already fetched data.

  

### How to run?

Go to the repository's root directory and follow instructions

  

### How to check if the service is running?

Hit `localhost:8081/sanity` to see if the service is up and running.