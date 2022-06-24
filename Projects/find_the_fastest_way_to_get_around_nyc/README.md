<!-- omit in toc -->
# Introduction

The goal of this project is to provide the fastest way to go from A to B in New York City. Two ways of transportation, Citi Bike and Yellow Cab taxi are compared for the fastest way.

<br />

<!-- omit in toc -->
# Table of Contents

<br />


# Environment
> Environment settings are all from Chapter 14 of [Data Pipelines With Apache Airflow](https://github.com/BasPH/data-pipelines-with-apache-airflow)

* Services in Docker containers:
  1. REST API for Citi Bike data
  2. File share for Yellow Cab taxi data
  3. MinIO to store raw data
  4. PostgreSQL database for **querying** and storing data
  5. Flask API to display results


## Structure of Services



# Data
* Since Citi Bike stations are based only in the center of New York. For the comparison at the same level, Yell Cab data is limited to this zone.
* Yellow Cab data only keeps the full hour of data, therefore, it is required database to store historical data.
* Citi Bike API has no limitations in terms of request size. However, in practice, API could limit the number of results to 1,000. 
> Evaluating the amount of data in a certain time periods, which is up to 1,000, is required.
* Citi Bike and Yellow Cab data use different units to identify locations. To make it simple, the accuracy is sacrificed a little to keep the identical units - mapping the latitude/longitude of Citi Bike stations to taxi zones.
* Keep the interval of data is at 15-minute since the smallest intervals is 15-minute in the Yellow Cab data


## Issue
Since raw data stored in PostgreSQL are old, Airflow using c