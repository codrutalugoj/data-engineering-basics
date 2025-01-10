This repo contains the setup for a simple data pipeline. This code is based on the FreeCodeCamp's Data Engineering [course](https://www.freecodecamp.org/news/learn-the-essentials-of-data-engineering/). 

Here we build an ELT (extract, load, transform) process using a Python script, Docker containers and PostgreSQL for database management. We then use dbt 

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

### Building custom dbt models
1. source the data
    - this is simply referencing the tables we have from the destination_db
    - these references are `film_actors.sql`, `actors.sql`, `films.sql`
2. schema - let's dbt run tests against all written models (i.e. sql files) and checks if the files are within the constraints of the schema
3. creating the custom model which creates 2 tables and then joins them - `film_ratings.sql`