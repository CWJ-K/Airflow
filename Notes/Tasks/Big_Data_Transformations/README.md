<!-- omit in toc -->
# Introduction

When facing big data, data transformation may impact the resources of Airflow machine. So, how to avoid running out the resources of Airflow machine?

<br />

<!-- omit in toc -->
# Table of Contents

<br />

# Methods
Use a cluster of machines instead a single machine
## Spark
* SparkSubmitOperator
* SSHOperator

## Containerized Systems
### Kubernetes
* KubernetesPodOperator

### AWS ECS
* ECSOperator
