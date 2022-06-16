<!-- omit in toc -->
# (**WIP**)



<!-- omit in toc -->
# Table of Contents

<br />


# Introduction
Transfer data between a Postgres database containing Airbnb data. 

* Dataset: Airbnb data in Amsterdam between April 2015 and December 2019
  
* Goal: transfer data from PostgreSQL to Amazon S3
* Tools: PostgreSQL, Amazon S3, docker, Python pandas

# Structure
Docker container: Postgres
* holds a Postgres image with Airbnb data
* image name on Docker Hub: airflowbook/insiderbnb
* 

Docker container: python
* start a container to process data using Pandas