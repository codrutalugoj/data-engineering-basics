This repo contains the setup for a simple data pipeline. This code is based on the FreeCodeCamp's Data Engineering [course](https://www.freecodecamp.org/news/learn-the-essentials-of-data-engineering/). 

Here we build an ELT (extract, load, transform) process using a Python script, Docker containers and PostgreSQL for database management. We then use dbt to write custom transformations on actor and film data.

# Docker
- we're creating a Docker compose file
- establishes 2 PostgreSQL databases: source, where we get data from and destination, where we want to tranfer the data. 
- creates the network for the different containers to communicate on
- creates the volume to persist the data. 

# ELT Script (elt/elt.py)
- ensures the source database is ready 
- creates tables and inserts data into the source database
- loads the data from the source database into the destination database.


# dbt
dbt helps with custom transformations on the data we just created + loaded in the ELT script. This is useful when the user of the data (e.g. data analysts, data scientists etc.) requires the data to be in a certain format. 

### Installing dbt and setting up a project
- (optional) set up a pip venv and activate it
- install dbt-postgres and dbt-core: `python -m pip install dbt-core dbt-postgres`
- initialize a dbt project: `dbt init`
    - dbt prompts for config details that will be written out in /PATH/.dbt/profiles.yml
- a new folder will be created at the location containing analyses, macros, models and a dbt_project.yml. 
    - within the dbt_project.yml, change the materialized param from 'view' to 'table' so the dbt models are persisted in the data warehouse. 

### Building custom dbt model
1. source the data
    - this is simply referencing the tables we have from the destination_db
    - these references are `film_actors.sql`, `actors.sql`, `films.sql`
2. schema - let's dbt run tests against all written models (i.e. sql files) and checks if the files are within the constraints of the schema
3. create the custom model which creates 2 tables and then joins them - `film_ratings.sql`

### Running the dbt model
- `docker compose up`
- then checking if the new table film_ratings got created:
    - `docker exec -it <destination_container_name> psql -U postgres`
    - connect to database: `\c destination_db`
    - list all tables: `\dt`.

### Notes:
- the build initially failed when creating the dbt model because of an issue with pg_matviews (See https://github.com/schemaspy/schemaspy/issues/636). Upgrading the Postgres version from 9.2 to 10 for source and destination dbs fixed the issue. 


# CRON Job
- Linux package to run scripts/commands at scheduled times
- `start.sh` calls the cron daemon in the background and executes the ELT script

# Airflow 
Open-source orchestration tool that we can use to programatically schedule and monitor workflows.

### Setup:
- `airflow.cfg` - config file 
- Docker compose: add the Airflow services
    - postgres
    - init_airflow
    - webserver
    - scheduler
- running the Airflow workflow:
    - `docker compose up`
    - note: I have to manually trigger the webserver service from the Docker UI to make sure the server starts
    - `docker compose down -v` to take down the containers.