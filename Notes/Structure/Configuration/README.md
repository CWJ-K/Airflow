<!-- omit in toc -->
# Introduction
Take notes of parameter in docker-compose of Airflow

<br />

<!-- omit in toc -->
# Table of Contents
- [Fundamental Concepts](#fundamental-concepts)
  - [Configuration](#configuration)
  - [AIRFLOW__CORE__FERNET_KEY](#airflow__core__fernet_key)
    - [Fernet](#fernet)
      - [Generate Fernet key](#generate-fernet-key)
  - [AIRFLOW__CORE__STORE_DAG_CODE](#airflow__core__store_dag_code)
  - [AIRFLOW__CORE__STORE_SERIALIZED_DAGS](#airflow__core__store_serialized_dags)
  - [AIRFLOW__WEBSERVER__EXPOSE_CONFIG](#airflow__webserver__expose_config)
  - [AIRFLOW_CONN_MY_POSTGRES](#airflow_conn_my_postgres)
  - [AIRFLOW__CORE__SQL_ALCHEMY_CONN](#airflow__core__sql_alchemy_conn)
  - [apache-airflow-providers-postgres](#apache-airflow-providers-postgres)
  - [AIRFLOW__API__AUTH_BACKEND](#airflow__api__auth_backend)

<br />

# Fundamental Concepts
## Configuration 
* airflow.cfg (configuration) is created when Airflow is first started
  * contain configurations, such as password

<br />

## AIRFLOW__CORE__FERNET_KEY
### Fernet
* to encrypt passwords in the connection configuration and the variable configuration
* a password encrypted cannot be manipulated or read without the key

#### Generate Fernet key

    from cryptography.fernet import Fernet

    fernet_key = Fernet.generate_key()
    print(fernet_key.decode())

<br />

## AIRFLOW__CORE__STORE_DAG_CODE
* If True, Webserver reads file contents from DB instead of accessing files in a DAG folder

<br />

## AIRFLOW__CORE__STORE_SERIALIZED_DAGS
* to make [Airflow Webserver stateless](https://airflow.apache.org/docs/apache-airflow/stable/dag-serialization.html) (using Cache save data)
* If True, Webserver reads from DB instead of parsing DAG files

<br />

## AIRFLOW__WEBSERVER__EXPOSE_CONFIG
* If True, configuration becomes accessible to anyone via the web server

<br />

## [AIRFLOW_CONN_MY_POSTGRES](https://kids-first.github.io/kf-airflow-dags/connections.html#using-connections)
* If the connection that needs to be added does not condense into a simple connection string, it should have this parameter 
* **TOOD** may be added through Airflow UI
  
        # AIRFLOW_CONN_MY_POSTGRES should in the environment

        task = PostgresOperator(
            "SELECT count(*) FROM users;",
            postgres_conn_id="my_postgres",
            database="profiles",
            dag=dag
        )

<br />

## AIRFLOW__CORE__SQL_ALCHEMY_CONN
* SqlAlchemy connection string to the metadata database


## apache-airflow-providers-postgres
* in Dockerfile
* a provider package for postgres provider

## AIRFLOW__API__AUTH_BACKEND
* to authenticate users of the API