<!-- omit in toc -->

# Introduction
How to pass data between tasks in Airflow ?

<br />

<!-- omit in toc -->

# Table of Contents
- [Introduction](#introduction)
- [Table of Contents](#table-of-contents)
- [Fundamental Concepts](#fundamental-concepts)
  - [1. Operator](#1-operator)
  - [2. Hook](#2-hook)
  - [TaskInstance](#taskinstance)
- [Two Methods to Write and Read Results Between Tasks](#two-methods-to-write-and-read-results-between-tasks)
  - [1. Use Airflow Metastore](#1-use-airflow-metastore)
    - [1.1. XComs](#11-xcoms)
    - [1.2. Taskflow API](#12-taskflow-api)
  - [2. Use a persistent location (e.g. disk or database)](#2-use-a-persistent-location-eg-disk-or-database)
    - [2.1. Store connection credentials in Airflow](#21-store-connection-credentials-in-airflow)
      - [2.1.1. CLI](#211-cli)
      - [2.1.2. Airflow UI](#212-airflow-ui)
    - [2.2. Other Systems](#22-other-systems)
      - [2.2.1. PostgresOperator](#221-postgresoperator)
- [Commands](#commands)
  - [1. Different methods of XComs](#1-different-methods-of-xcoms)
    - [1.1. xcom_pull => templates](#11-xcom_pull--templates)
    - [task instance ti](#task-instance-ti)
    - [1.2. Automatically Pushing XComs Values](#12-automatically-pushing-xcoms-values)
      - [1.2.1. BashOperator](#121-bashoperator)
      - [1.2.2. PythonOperator](#122-pythonoperator)
    - [1.3. Taskflow API](#13-taskflow-api)

<br />

# Fundamental Concepts

## 1. Operator
determine what has to be done

## 2. Hook
determine how to do something

## TaskInstance
* To push or pull, it is required to access to the TaskInstance object of the current run, which is only available through context

<br />

# Two Methods to Write and Read Results Between Tasks
publish the value to make it available for other tasks

<br />

## 1. Use Airflow Metastore 

### 1.1. XComs
* allow stores and reads picklable objects
    > pickle: can be stored on disk and read again later  
    > non-picklable object: e.g. database connection, file handlers
* only store small picklable objects
* Customize XComs is to inherit BaseXCom base class
  * for the storage of XCom values in cloud storage
   
### 1.2. Taskflow API
* to simplify python tasks using PythonOperators and XComs
* drawback: the code is not easily readable and is confusing

<br />

## 2. Use a persistent location (e.g. disk or database)

### 2.1. Store connection credentials in Airflow

#### 2.1.1. CLI
        airflow connections add --conn-type postgres --conn-host localhost --conn-login postgres --conn-password mypassword my_postgres

#### 2.1.2. Airflow UI
admin > connections

### 2.2. Other Systems
* required to install packages for operators


#### 2.2.1. PostgresOperator
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
  
<br />

# Commands

## 1. Different methods of XComs
* xcom_push; xcom_pull

      def _train_model(**context):
        model_id = str(uuid.uuid4())
        context["task_instance"].xcom_push(key="model_id", value=model_id)

      def _deploy_model(**context):
          model_id = context["task_instance"].xcom_pull(
              task_ids="train_model", key="model_id"
          )
          print(f"Deploying model {model_id}")
      
      train_model = PythonOperator(task_id="train_model", python_callable=_train_model)

      deploy_model = PythonOperator(task_id="deploy_model", python_callable=_deploy_model)

      train_model >> deploy_model

<br />

### 1.1. xcom_pull => templates

    def _train_model(**context):
      model_id = str(uuid.uuid4())
      context["task_instance"].xcom_push(key="model_id", value=model_id)


    def _deploy_model(templates_dict, **context):
        model_id = templates_dict["model_id"]
        print(f"Deploying model {model_id}")

    train_model = PythonOperator(task_id="train_model", python_callable=_train_model)

    deploy_model = PythonOperator(
            task_id="deploy_model",
            python_callable=_deploy_model,
            templates_dict={
                "model_id": "{{task_instance.xcom_pull(task_ids='train_model', key='model_id')}}"
            },
        )

    train_model >> deploy_model

<br />

### task instance [ti](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html)

```python
  process_taxi_data = PandasOperator(
    task_id="process_taxi_data",
    input_callable_kwargs={
        "pandas_read_callable": pd.read_csv,
        "bucket": "datalake",
        "paths": "{{ ti.xcom_pull(task_ids='download_taxi_data') }}",
    },

```

### 1.2. Automatically Pushing XComs Values

#### 1.2.1. BashOperator
* push the last line written to stdout as an XCom value
    BashOperator (..., xcom_push=True)

#### 1.2.2. PythonOperator
  * publish any value returned from the Python callable

        def _train_model(**context):
          model_id = str(uuid.uuid4())
          return model_id


        def _deploy_model(templates_dict, **context):
          model_id = templates_dict["model_id"]
          print(f"Deploying model {model_id}")


        train_model = PythonOperator(
          task_id="train_model", python_callable=_train_model
        )


        deploy_model = PythonOperator(
            task_id="deploy_model",
            python_callable=_deploy_model,
            templates_dict={
                "model_id": "{{task_instance.xcom_pull(task_ids='train_model', key='model_id')}}"
            },
        )

        train_model >> deploy_model
  
<br />

### 1.3. Taskflow API

    with DAG(
        dag_id="taskflow",
        start_date=airflow.utils.dates.days_ago(3),
        schedule_interval="@daily",
    ) as dag:

      @task
      def train_model():
          model_id = str(uuid.uuid4())
          return model_id

      @task
      def deploy_model(model_id: str):
          print(f"Deploying model {model_id}")

      model_id = train_model()
      deploy_model(model_id)

      get_datasets = DummyOperator(task_id="get_datasets")


      # not intuitionally
      get_datasets >> model_id 
