This repo contains the setup for a simple data pipeline. This code is based on the FreeCodeCamp's Data Engineering [course](https://www.freecodecamp.org/news/learn-the-essentials-of-data-engineering/). 

Here we build an ELT (extract, load, transform) process using a Python script, Docker containers and PostgreSQL for database management. 

## Docker compose file:
- establishes 2 PostgreSQL databases: source, where we get data from and destination, where we want to tranfer the data. 
- creates the network for the different containers to communicate on
- creates the volume to persist the data. 

## ELT Script (elt/elt.py)
- ensures the source database is ready 
- creates tables and inserts data into the source database
- loads the data from the source database into the destination database.


