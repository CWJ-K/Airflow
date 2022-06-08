<!-- omit in toc -->
# Introduction
How to pass data between tasks in Airflow ?

<br />

<!-- omit in toc -->
# Table of Contents
- [Fundamental Concepts](#fundamental-concepts)
  - [Operator](#operator)
  - [Hook](#hook)
- [Two Methods to Write and Read Results Between Tasks](#two-methods-to-write-and-read-results-between-tasks)
  - [Use Airflow Metastore](#use-airflow-metastore)
    - [XCom](#xcom)
  - [Use a persistent location (e.g. disk or database)](#use-a-persistent-location-eg-disk-or-database)
    - [Store connection credentials in Airflow](#store-connection-credentials-in-airflow)
      - [CLI](#cli)
      - [Airflow UI](#airflow-ui)
    - [Other Systems](#other-systems)
      - [PostgresOperator](#postgresoperator)


# Fundamental Concepts
## Operator
determine what has to be done
## Hook
determine how to do something

# Two Methods to Write and Read Results Between Tasks
## Use Airflow Metastore 
### XCom
* allow stores and reads picklable objects
    > pickle: can be stored on disk and read again later  
    > non-picklable object: e.g. database connection, file handlers
* only store small picklable objects

## Use a persistent location (e.g. disk or database)

### Store connection credentials in Airflow
#### CLI
        airflow connections add --conn-type postgres --conn-host localhost --conn-login postgres --conn-password mypassword my_postgres

#### Airflow UI
admin > connections

### Other Systems
* required to install packages for operators


#### PostgresOperator
* PostgresOperator instantiate hook to communicate Postgres
  * hook can create connection, send query to Postgres and close the connection


    pip install apache-airflow-providers-postgres

    dag = DAG(..., template_searchable='/tmp')

    write_to_postgres = PostgresOperator(
        ...,
        postgres_conn_id='my_postgres',
        sql='postgres_query.sql',
        dag=dag
    )

    
  * template_searchable: path to search for sql file, which Jinja can search for. By default Jinja only searches for DAG folder
  * postgres_conn_id: identify connection to be used
  * sql: SQL query or path to file containing **SQL queries**
  




