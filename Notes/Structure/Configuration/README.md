<!-- omit in toc -->
# Introduction
Understand configurations in Airflow to deploy Airflow 

<br />

<!-- omit in toc -->
# Table of Contents
- [Fundamental Concepts](#fundamental-concepts)
  - [1. Configuration](#1-configuration)
- [Arguments](#arguments)
  - [1. AIRFLOW__CORE__FERNET_KEY](#1-airflow__core__fernet_key)
    - [1.1. Fernet](#11-fernet)
      - [1.1.1. Generate Fernet key](#111-generate-fernet-key)
  - [2. AIRFLOW__CORE__STORE_DAG_CODE](#2-airflow__core__store_dag_code)
  - [3. AIRFLOW__CORE__STORE_SERIALIZED_DAGS](#3-airflow__core__store_serialized_dags)
  - [4. AIRFLOW__WEBSERVER__EXPOSE_CONFIG](#4-airflow__webserver__expose_config)
  - [5. AIRFLOW_CONN_MY_POSTGRES](#5-airflow_conn_my_postgres)
  - [6. AIRFLOW__CORE__SQL_ALCHEMY_CONN](#6-airflow__core__sql_alchemy_conn)
  - [7. AIRFLOW__API__AUTH_BACKEND](#7-airflow__api__auth_backend)
  - [8. AIRFLOW_HOME](#8-airflow_home)
  - [9. AIRFLOW__CORE__DAGS_FOLDER](#9-airflow__core__dags_folder)
  - [10. Connectionss](#10-connectionss)
    - [10.1. syntax](#101-syntax)
    - [10.2. e.g. connect to S3 by Minio](#102-eg-connect-to-s3-by-minio)
- [Commands](#commands)
  - [1. airflow db init](#1-airflow-db-init)
  - [2. airflow db restart](#2-airflow-db-restart)

<br />

# Fundamental Concepts

## 1. Configuration 
* airflow.cfg (configuration) is created when Airflow is first started
  * contain configurations, such as password

<br />

# Arguments

## 1. AIRFLOW__CORE__FERNET_KEY

### 1.1. Fernet
* to encrypt passwords in the connection configuration and the variable configuration
* a password encrypted cannot be manipulated or read without the key

#### 1.1.1. Generate Fernet key

    from cryptography.fernet import Fernet

    fernet_key = Fernet.generate_key()
    print(fernet_key.decode())

<br />

## 2. AIRFLOW__CORE__STORE_DAG_CODE
* If True, Webserver reads file contents from DB instead of accessing files in a DAG folder

<br />

## 3. AIRFLOW__CORE__STORE_SERIALIZED_DAGS
* to make [Airflow Webserver stateless](https://airflow.apache.org/docs/apache-airflow/stable/dag-serialization.html) (using Cache save data)
* If True, Webserver reads from DB instead of parsing DAG files

<br />

## 4. AIRFLOW__WEBSERVER__EXPOSE_CONFIG
* If True, configuration becomes accessible to anyone via the web server

<br />

## 5. [AIRFLOW_CONN_MY_POSTGRES](https://kids-first.github.io/kf-airflow-dags/connections.html#using-connections)
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

## 6. AIRFLOW__CORE__SQL_ALCHEMY_CONN
* SqlAlchemy connection string to the metadata database

<br />

## 7. AIRFLOW__API__AUTH_BACKEND
* to authenticate users of the API

<br />

## 8. AIRFLOW_HOME
* the location where Airflow stores logs, dags and such

<br />

## 9. AIRFLOW__CORE__DAGS_FOLDER
* default: inside AIRFLOW_HOME, Airflow searches for a `/dags` directory
  
<br />


## 10. Connectionss

### 10.1. syntax
`AIRFLOW_CONN_<conn_id>=<http://username:password@hostname:port>`

### 10.2. e.g. connect to S3 by Minio
`AIRFLOW_CONN_S3='s3://@?host=http://minio:9000&aws_access_key_id=<key_id>&aws_secret_access_key=<secret_key>'`
> @: where you expect to set the hostname
> host=http://minio:9000 => hostname provided by via extras



# Commands

## 1. airflow db init

* initialize a local SQLite database inside AIRFLOW_HOME
* to be used only in the first time that the database is created from the airflow.cfg
* will not affect existing databases, therefore, it enables to be recalled several times 

<br />

## 2. [airflow db restart](https://stackoverflow.com/questions/59556501/apache-airflow-initdb-vs-resetdb)
* delete all entries from the metadata database. This includes all dag runs, Variables and Connections
  *  Variables and connections can be annoying to recreate as they often contain secret and sensitive data, which may not be duplicated as a matter of security best practice