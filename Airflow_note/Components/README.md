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
* initialize a local SQLite database inside AIRFLOW_HOME

