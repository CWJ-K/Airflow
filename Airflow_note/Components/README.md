<!-- omit in toc -->
# Introduction
Take notes of the main components involved in Airflow.

<br />

<!-- omit in toc -->
# Table of Contents
- [Main components](#main-components)
  - [Dag files](#dag-files)
  - [Scheduler](#scheduler)
  - [Workers](#workers)
  - [Database](#database)
- [Environment Variables](#environment-variables)
  - [AIRFLOW_HOME](#airflow_home)
  - [AIRFLOW__CORE__DAGS_FOLDER](#airflow__core__dags_folder)
  - [airflow db init](#airflow-db-init)
    - [airflow db init](#airflow-db-init-1)
    - [airflow db restart](#airflow-db-restart)

<br />

# Main components

## Dag files
users write pipelines as DAGs, stored in the Dag folder

<br />

## Scheduler
* scheduler reads Dag folder to extract corresponding **tasks, dependents** and **schedule interval** of each Dag
* scheduler checks if the schedule interval for the DAG had passed since the last time it was read. If passed, the tasks are added to the execution queue
* scheduler checks if the dependencies of tasks have been completed 
* scheduler wait until the new loop

<br />

## Workers

<br />

## Database

<br />

# Environment Variables
## AIRFLOW_HOME
* the location where Airflow stores logs, dags and such

<br />

## AIRFLOW__CORE__DAGS_FOLDER
* default: inside AIRFLOW_HOME, Airflow searches for a `/dags` directory
  
<br />

## airflow db init
### airflow db init
* initialize a local SQLite database inside AIRFLOW_HOME
* to be used only the first time that the database is created from the airflow.cfg
### [airflow db restart](https://stackoverflow.com/questions/59556501/apache-airflow-initdb-vs-resetdb)
* delete all entries from the metadata database. This includes all dag runs, Variables and Connections
  *  Variables and connections can be annoying to recreate as they often contain secret and sensitive data, which may not be duplicated as a matter of security best practice

