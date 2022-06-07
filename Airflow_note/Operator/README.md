<!-- omit in toc -->
# Introduction
Take notes of parameters involved in Airflow.

<br />

<!-- omit in toc -->
# Table of Contents
- [Fundamental Concepts](#fundamental-concepts)
  - [PythonOperator](#pythonoperator)
  - [Dynamic References](#dynamic-references)
  - [Rules of Tasks](#rules-of-tasks)
    - [atomicity](#atomicity)
    - [Idempotent](#idempotent)

<br />

# Fundamental Concepts
## PythonOperator
* python_callable <br />
python function which is callable

<br />

## Dynamic References
* Use Airflow's Jinja based template syntax to reference parameters.

* Available parameters can be found in [Templates reference](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html).

* Example:
  > Execution Date of Airflow is not actually date, but datetime type

      # assign dynamic parameters - execution date, next execution date - into tasks

      fetch_objects = BashOperator(
        task_id = 'fetch_objects',
        bash_command = (
          "mkdir -p /data/events && "
          "curl -o /data/events.json "
          "http://events_api:5000/events? "
          "start_date={{execution_date.strftime('%Y-%m-%d')}}&"
          "end_date={{next_execution_date.strftime('%Y-%m-%d')}}"
        ),
        dag=dag,
      )

<br />

## Rules of Tasks
### atomicity
* should follow atomicity to make sure a task will not produce half work if the task failed. 
  
  <br />
  e.g. a task includes writing data and sending mails if sending mails fails, but data already is stored in the local directory. 

* Solution
  split tasks into multiple tasks => make sure each task has only one purpose 

<br />

### Idempotent
* if a task is called several times, its output should be identical every time 