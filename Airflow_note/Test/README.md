<!-- omit in toc -->
# Introduction
How to test Airflow tasks?

<br />

<!-- omit in toc -->
# Table of Contents
- [Test in a production setting](#test-in-a-production-setting)
  - [use UI](#use-ui)
  - [use CLI](#use-cli)
    - [render](#render)
    - [test](#test)
- [Test in a CI/CD pipeline](#test-in-a-cicd-pipeline)
  - [test works with DAGs and task context](#test-works-with-dags-and-task-context)
  - [test works with external systems](#test-works-with-external-systems)
    - [Methods](#methods)
- [Test complete DAGs](#test-complete-dags)
  - [Goal](#goal)
  - [Method](#method)
    - [Whirl](#whirl)
    - [Create DTAP environments](#create-dtap-environments)

<br />

# Test in a production setting
## use UI
Rendered Template
## use CLI
### render
* If using templated fields in an Operator, the created strings out of the **templated fields** will be shown
* not register anything in the metastore
* still produces task output e.g. data

        airflow tasks render [dag id] [task id] [desired execution date]

<br />

### test 
> required to test
* simulates the scheduler running your task or DAG for a specific date and time, even though it **physically will run now**
* runs task instances locally, outputs their log to stdout
* run a task without:
  * checking for dependencies 
  * recording its state in the database
* still produces:
  * task output e.g. data
  * logs, which requires a **database** for storing logs
        > before testing, make sure the database is for test or `airflow db init` to store test logs in SQLite DB

        > alternatively, using mock or container, so no need to created metastore for airflow test


        airflow tasks test [dag id] [task id] [desired execution date]

<br />


# Test in a CI/CD pipeline
## test works with DAGs and task context
* the test requires the information of task context, which can not set `context=None` in the test function
* there are several steps in running an operator
  * can be seen in the book p. 204
  * Pay attention:
    1. after building task instance context (collecting all variables), the XCom data for current task instance is clearer from Airflow **metastore**
    2. render templated variables with context
    3. ...
    4. after execute(), push returned value to XCom to Airflow **Metastore**

* call the actual method by operator.run()
  * a method on the BaseOperator class
  * the method must be assigned a DAG since Airflow runs a task, referring to the DAG object (e.g. task context)

* since executing tasks requires to store task context in metastore, metastore is needed. Two methods as below:
  1. mock every single database call => cumbersome => alternative: use container
  2. initialize the database `airflow db init`
      * will create a default db: SQLite, stored in `~/airflow/airflow.db`
      * can be set via `AIRFLOW_HOME`

* If running multiple tests requires reusing the DAG several times, `pytest fixtures` is used to avoid duplicated codes

<br />

## test works with external systems
* e.g. write results to a Postgres database

<br />

### Methods
1. create a **Docker** container of a local Postgres database for testing
  > **Benefits**: enable to use the real methods of hooks instead of mocking calls, which makes testing as realistic as possible
2. use `pytest-docker-tools`
  * a wrapper around the Python Docker client
  ```linux
  pip install pytest_docker_tools
  ```
  
3. use helper functions of pytest-docker-tools:
  > they are all **pytest fixture**  => <br /> 1. cannot call it directly <br /> 2. provide it as a parameter to a test
  * fetch
    * fetch a docker image from DockerHub
    * `docker pull`
    * return the pulled image
  * container
    * can configure environment variables, volumes ... based on
    * ports
      * typically map a container port to the same port on the host machine
      * for test, it is not required to persist port or conflict with other ports in use => assign a **random** port on the host machine
        * like `docker run -P`
        * ```python
            container(
                image='{apiserver_image.id}',
                ports={'8080/tcp': None} # {container_port:host_port}
              )
          ```
          * None will map the random port on the host machine
4. initialize database
  * Goal: To create a database structure and data schema 
  * Method: add `sql-file` in the docker directory: `/docker-entrypoint-initdb.d/`
  * put the `sql-file` in the same directory of test
    
5. use absolute path in pytest files
  ```python
    os.path.dirname(__file__)
  ```


# Test complete DAGs
## Goal
* make sure all operators in a DAG work together as expected
## Method
* challenging: it is required to mimic a real production environment. It is impossible to perfectly mimic because of privacy regulations or the size of the data
* Methods to recreate a production environment as below:
### Whirl
* simulate all components of the production environment in Docker containers and manage them with Docker Compose
* challenging: security issue 
### Create DTAP environments
* create development and production environments
* combine with git dev/prod branches
  1. develop locally in branches => merge into develope brach => run dag on the development environment 
  2. merge change into main branch for the production environment