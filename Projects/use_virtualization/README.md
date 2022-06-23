<!-- omit in toc -->
# Introduction
Instead to use different Airflow operators, only implement docker operators to run tasks.

<br />

<!-- omit in toc -->
# Table of Contents
- [Why needs container-based operators?](#why-needs-container-based-operators)
- [Container-based Operators](#container-based-operators)
  - [DockerOperator](#dockeroperator)
    - [Steps](#steps)
  - [KubernetesPodOperator](#kubernetespodoperator)

<br />

# Why needs container-based operators?
* using different operators has drawbacks:
  1. takes time to fix bugs:<br />
        need to familiarize ourselves with the interface of multiple types of operators and the inner workings of each operator  
  2. complex and conflicting dependencies:<br />
        * different tasks require their corresponding dependencies to be installed 
          * leads to conflicts and complexity in environment maintenance 
          * may cause security risks with installing so many different software packages together 
* Advantages of docker operators:
  1. using a single operator for Airflow tasks:<br />
    * easy to understand the interface
    * mitigate bugs occurring 
  2. separate dependencies of each task
    * easy to manage dependencies in different images
  3. tasks no longer run directly on the workers
    * task dependencies are not installed in the worker environment
  4. improve testability
    * each image have its development cycle
    > think about how to cicd image ?
    * if testing on PythonOperator, it tightly couples to the DAG

<br />

# Container-based Operators
* The operators start running a container after they are executed 
* similar to `docker run`
* after finishing running, the container will be terminated

<br />

## DockerOperator
* after finishing tasks, the container is terminated
* run in Airflow worker machine
* images are cached locally when fetched

<br />

### Steps
1. build images via Dockerfile
   * include task scripts
     * with **shebang** to tell Linux to execute the script using Python
     * with `click` to convert `main` function to a click CLI command 
     * with `main` function and `if __name__ == "__main__":`
   * Dockerfile
     * `ENV`: ensure the script is on the PATH to directly run the script without specifying the full path to the script


<br />

## KubernetesPodOperator
* not run in Airflow worker machine, but in Kubernetes