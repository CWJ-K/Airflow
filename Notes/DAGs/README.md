<!-- omit in toc -->
# Introduction
How do DAGs proceed with tasks? 

<br />

<!-- omit in toc -->
# Table of Contents
- [Fundamental Concepts](#fundamental-concepts)
  - [DAG](#dag)
  - [Backfill](#backfill)
  - [Schedule Interval](#schedule-interval)
    - [schedule intervals vs cron-based intervals](#schedule-intervals-vs-cron-based-intervals)
- [Airflow UI](#airflow-ui)
  - [run_id](#run_id)
  - [Clear](#clear)
- [Arguments](#arguments)
  - [Execution date](#execution-date)
  - [max_active_runs](#max_active_runs)
  
<br />

# Fundamental Concepts
## DAG
instantiate a DAG object, which is a starting point of any workflow 
        
  ``` python
  # python class
  dag = DAG()
  ```

<br />

## Backfill
a process to perform history runs of a DAG for loading or analyzing past data sets
> **catch up** <br />
**True**, implies DAG will run from start_date to current datetime. <br />
**False**, implies DAG will run from current datetime.

    
  ```python
  dag = DAG(
    dag_id='backfill',
    schedule=interval='@daily',
    start_date=dt.datetime(year=2019, month=1, day=1),
    end_date=dt.datetime(year=2019, month=1, day=5),
    catchup=True,
  )
  ```

<br />

## Schedule Interval
Airflow uses schedule intervals, instead of cron-based intervals
### schedule intervals vs cron-based intervals
||schedule interval|cron-based intervals|
|:---:|:---|:---|
|Advantage|1. easy to read <br /> 2. enable to run a DAG in every specific time intervals|1. clear to know when a previous job ran|
|Disadvantage||1. difficult to read <br /> 2. hard to specify the interval of periods to run a DAG since cron define the specific time. e.g. can not run a DAG every three days|

> schedule interval is convenient if interval-based DAGS is intentionally executed on unexpected datetime and still follows the rule of a DAG executed every three days


<br />

# Airflow UI
## run_id
* scheduled__*: the DAG started to run because of its schedule
* backfill__*: the DAG run started with a backfill job
* manual__*: the DAG run started with a manual action - trigger button

## Clear
clearing tasks only clear tasks within **the same DAG**

<br />

# Arguments

## Execution date
* Definition: the start of the **corresponding interval** (since Airflow uses [Schedule Interval](#schedule-interval))
* not the moment of DAG is executed, but the mark of schedule interval
* Airflow uses **Pendulum** library for datetimes


## max_active_runs
* maximum number of active DAG runs




