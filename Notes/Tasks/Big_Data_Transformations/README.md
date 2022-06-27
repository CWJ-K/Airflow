<!-- omit in toc -->
# Introduction

When facing big data, data transformation may impact the resources of the Airflow machine. So, how to avoid running out the resources of the Airflow machine?

<br />

<!-- omit in toc -->
# Table of Contents
- [Methods](#methods)
  - [1. Spark](#1-spark)
  - [2. Containerized Systems](#2-containerized-systems)
    - [2.1. Kubernetes](#21-kubernetes)
    - [2.2. AWS ECS](#22-aws-ecs)
<br />

# Methods
Use a cluster of machines instead of a single machine
<br />

## 1. Spark
* SparkSubmitOperator
* SSHOperator

<br />

## 2. Containerized Systems

<br />

### 2.1. Kubernetes
* KubernetesPodOperator

<br />

### 2.2. AWS ECS
* ECSOperator
