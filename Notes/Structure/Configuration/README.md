<!-- omit in toc -->

# Introduction
Take notes of parameter in docker-compose of Airflow

<br />

<!-- omit in toc -->

# Table of Contents
- [Introduction](#introduction)
- [Table of Contents](#table-of-contents)
- [Fundamental Concepts](#fundamental-concepts)
  - [1. Configuration](#1-configuration)
  - [2. AIRFLOW__CORE__FERNET_KEY](#2-airflow__core__fernet_key)
    - [2.1. Fernet](#21-fernet)
      - [2.1.1. Generate Fernet key](#211-generate-fernet-key)
  - [3. AIRFLOW__CORE__STORE_DAG_CODE](#3-airflow__core__store_dag_code)
  - [4. AIRFLOW__CORE__STORE_SERIALIZED_DAGS](#4-airflow__core__store_serialized_dags)
  - [5. AIRFLOW__WEBSERVER__EXPOSE_CONFIG](#5-airflow__webserver__expose_config)
  - [6. AIRFLOW_CONN_MY_POSTGRES](#6-airflow_conn_my_postgres)
  - [7. AIRFLOW__CORE__SQL_ALCHEMY_CONN](#7-airflow__core__sql_alchemy_conn)
  - [8. apache-airflow-providers-postgres](#8-apache-airflow-providers-postgres)
  - [9. AIRFLOW__API__AUTH_BACKEND](#9-airflow__api__auth_backend)
- [Connections](#connections)
  - [syntax](#syntax)
  - [connect to S3 by Minio](#connect-to-s3-by-minio)

<br />

# Fundamental Concepts

## 1. Configuration 
* airflow.cfg (configuration) is created when Airflow is first started
  * contain configurations, such as password

<br />

## 2. AIRFLOW__CORE__FERNET_KEY

### 2.1. Fernet
* to encrypt passwords in the connection configuration and the variable configuration
* a password encrypted cannot be manipulated or read without the key

#### 2.1.1. Generate Fernet key

    from cryptography.fernet import Fernet

    fernet_key = Fernet.generate_key()
    print(fernet_key.decode())

<br />

## 3. AIRFLOW__CORE__STORE_DAG_CODE
* If True, Webserver reads file contents from DB instead of accessing files in a DAG folder

<br />

## 4. AIRFLOW__CORE__STORE_SERIALIZED_DAGS
* to make [Airflow Webserver stateless](https://airflow.apache.org/docs/apache-airflow/stable/dag-serialization.html) (using Cache save data)
* If True, Webserver reads from DB instead of parsing DAG files

<br />

## 5. AIRFLOW__WEBSERVER__EXPOSE_CONFIG
* If True, configuration becomes accessible to anyone via the web server

<br />

## 6. [AIRFLOW_CONN_MY_POSTGRES](https://kids-first.github.io/kf-airflow-dags/connections.html#using-connections)
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

## 7. AIRFLOW__CORE__SQL_ALCHEMY_CONN
* SqlAlchemy connection string to the metadata database


## 8. apache-airflow-providers-postgres
* in Dockerfile
* a provider package for postgres provider

## 9. AIRFLOW__API__AUTH_BACKEND
* to authenticate users of the API



#  Connections
## syntax
`AIRFLOW_CONN_<conn_id>=<http://username:password@hostname:port>`

## connect to S3 by Minio
`AIRFLOW_CONN_S3='s3://@?host=http://minio:9000&aws_access_key_id=<key_id>&aws_secret_access_key=<secret_key>'`
> @: where you expect to set the hostname
> host=http://minio:9000 => hostname provided by via extras


