This repository fetches the active cyclones and stores in the database for analysis.

### Let's talk a bit about the technologies used.

#### - Python

#### - PostgresSQL

#### - Docker

#### - Docker Compose

  

### How to run?

Make sure docker-compose is installed. That's all we need. Follow the below commands for running this service and a scheduler. Installation might take about 3-5 minutes for the first time. (LXML is the package where it spends most of the time). Subsequent installations will be little faster as docker caches each layer if there is no difference.

  

Run `docker-compose up --build` (use `-d` to run in the background)

  

### How to check logs?

Run `docker-compose logs` (Use `-f` to keep tailing)

### How to Stop?

Run `docker-compose down` to stop all containers
(Run `docker system prune -a` to remove unused images and containers)

#### About the repository
There are 3 primary docker containers.

1. Postgres Database for persistence. A volume is created and saved in local (`pgdata is the directory. Don't delete it)

2. A Flask based python server which will fetch the results of active cyclones and the location of the cyclone with real time as well as forecasted time if it's available.

3. There is a scheduler which can run periodically through an API which fetches the info and stores into the database. Scheduler API can takes timestamp to only write the records post the timestamp to make sure all the data is not updated again.

  

##### More details can be found in respective directories.