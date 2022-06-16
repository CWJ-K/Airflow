<!-- omit in toc -->
# Introduction
How to test Airflow tasks?

<br />

<!-- omit in toc -->
# Table of Contents
- [Methods](#methods)
  - [use UI](#use-ui)
  - [use CLI](#use-cli)
    - [render](#render)
    - [test](#test)


# Methods
## use UI
Rendered Template
## use CLI
### render
* If using templated fields in an Operator, the created strings out of the **templated fields** will be shown
* not register anything in the metastore
* still produces task output e.g. data

        airflow tasks render [dag id] [task id] [desired execution date]

### test
* run a task without:
  * checking for dependencies 
  * recording its state in the database
* still produces:
  * task output e.g. data
  * logs, which requires a **database** for storing logs
        > before testing, make sure the database is for test or `airflow db init` to store test logs in SQLite DB


        airflow tasks test [dag id] [task id] [desired execution date]

