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
    - [XComs](#xcoms)
    - [Taskflow API](#taskflow-api)
  - [Use a persistent location (e.g. disk or database)](#use-a-persistent-location-eg-disk-or-database)
    - [Store connection credentials in Airflow](#store-connection-credentials-in-airflow)
      - [CLI](#cli)
      - [Airflow UI](#airflow-ui)
    - [Other Systems](#other-systems)
      - [PostgresOperator](#postgresoperator)
- [Commands](#commands)
  - [Different methods of XComs](#different-methods-of-xcoms)
    - [xcom_pull => templates](#xcom_pull--templates)
    - [Automatically Pushing XComs Values](#automatically-pushing-xcoms-values)
      - [BashOperator](#bashoperator)
      - [PythonOperator](#pythonoperator)
    - [Taskflow API](#taskflow-api-1)

<br />

# Fundamental Concepts
## Operator
determine what has to be done
## Hook
determine how to do something

<br />

# Two Methods to Write and Read Results Between Tasks
publish the value to make it available for other tasks

<br />

## Use Airflow Metastore 
### XComs
* allow stores and reads picklable objects
    > pickle: can be stored on disk and read again later  
    > non-picklable object: e.g. database connection, file handlers
* only store small picklable objects
* Customize XComs is to inherit BaseXCom base class
  * for the storage of XCom values in cloud storage
   
### Taskflow API
* to simplify python tasks using PythonOperators and XComs
* drawback: the code is not easily readable and is confusing

<br />

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
  
<br />

# Commands

## Different methods of XComs
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

### xcom_pull => templates

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

### Automatically Pushing XComs Values
#### BashOperator
* push the last line written to stdout as an XCom value
    BashOperator (..., xcom_push=True)
#### PythonOperator
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

### Taskflow API

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
