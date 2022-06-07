<!-- omit in toc -->
# Introduction
Take notes of main object involved in Airflow.

<br />

<!-- omit in toc -->
# Table of Contents
- [Fundamental Concepts](#fundamental-concepts)
  - [DAG](#dag)
  - [Schedule Interval](#schedule-interval)
    - [schedule intervals vs cron-based intervals](#schedule-intervals-vs-cron-based-intervals)
    - [Execution date](#execution-date)
  - [Backfill](#backfill)
  
<br />

# Fundamental Concepts
## DAG
instantiate a DAG object, which is a starting point of any workflow 
        
        # python class
        dag = DAG()


## Schedule Interval
Airflow uses schedule intervals, instead of cron-based intervals
### schedule intervals vs cron-based intervals
||schedule interval|cron-based intervals|
|:---:|:---|:---|
|Advantage|1. easy to read <br /> 2. enable to run a DAG in every specific time intervals|1. clear to know when a previous job ran|
|Disadvantage||1. difficult to read <br /> 2. hard to specify the interval of periods to run a DAG since cron define the specific time. e.g. can not run a DAG every three days|

> schedule interval is convenient if interval-based DAGS is intentionally executed on unexpected datetime and still follows the rule of a DAG executed every three days


### Execution date
* Definition: the start of the **corresponding interval** (since Airflow uses schedule intervals)
* not the moment of DAG is executed, but the mark of schedule interval


## Backfill
a process to perform history runs of a DAG for loading or analyzing past data sets

    # catch up is True, implying DAG will run from start_date to current datetime
    # catch up is False, implying DAG will run from current datetime

    dag = DAG(
      dag_id='backfill',
      schedule=interval='@daily',
      start_date=dt.datetime(year=2019, month=1, day=1),
      end_date=dt.datetime(year=2019, month=1, day=5),
      catchup=True,
    )