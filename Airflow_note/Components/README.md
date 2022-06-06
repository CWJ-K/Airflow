<!-- omit in toc -->
# Introduction
Take notes of main components involved in Airflow.

<br />

<!-- omit in toc -->
# Table of Contents

<br />

# Fundamental Concepts

## Overview of main components

### Dag files
users write pipelines as DAGs, stored in Dag folder

### Scheduler
* scheduler read Dag folder to extract corresponding **tasks, dependents** and **schedule interval** of each Dag
* scheduler check if the schedule interval for the DAG had passed since the last time it was read. If passed, the tasks is added to the execution queue
* scheduler check if the dependencies of tasks have been completed 
* scheduler wait until the new loop
