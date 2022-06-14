<!-- omit in toc -->
# Introduction
Take notes of the main components involved in Airflow.

<br />

<!-- omit in toc -->
# Table of Contents
- [Main components](#main-components)
  - [Dag files](#dag-files)
  - [Scheduler](#scheduler)

<br />

## Main components

### Dag files
users write pipelines as DAGs, stored in the Dag folder

### Scheduler
* scheduler reads Dag folder to extract corresponding **tasks, dependents** and **schedule interval** of each Dag
* scheduler checks if the schedule interval for the DAG had passed since the last time it was read. If passed, the tasks are added to the execution queue
* scheduler checks if the dependencies of tasks have been completed 
* scheduler wait until the new loop
