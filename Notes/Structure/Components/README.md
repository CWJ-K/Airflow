<!-- omit in toc -->
# Introduction
Understand the structure of Airflow to deploy Airflow. 

<br />

<!-- omit in toc -->
# Table of Contents
- [Main components](#main-components)
  - [1. Dag Files](#1-dag-files)
  - [2. Scheduler](#2-scheduler)
  - [3. Workers](#3-workers)
  - [4. Database](#4-database)

<br />

# Main components

## 1. Dag Files
users write pipelines as DAGs, stored in the Dag folder

<br />

## 2. Scheduler
* scheduler reads Dag folder to extract corresponding **tasks, dependents** and **schedule interval** of each Dag
* scheduler checks if the schedule interval for the DAG had passed since the last time it was read. If passed, the tasks are added to the execution queue
* scheduler checks if the dependencies of tasks have been completed 
* scheduler wait until the new loop
> If local executor, scheduler will be as a worker to execute tasks and store results.

<br />

## 3. Workers

<br />

## 4. Database

