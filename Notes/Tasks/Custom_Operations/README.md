<!-- omit in toc -->
# Introduction
Default Airflow operators may not be applied to any cases. It may be required to build [custom operators](https://airflow.apache.org/docs/apache-airflow/stable/howto/custom-operator.html) to add more features. Therefore, it is important to learn how to customize your own operators.

<br />

<!-- omit in toc -->
# Table of Contents
- [Custom Hook](#custom-hook)
  - [1. Goal](#1-goal)
  - [2. Methods](#2-methods)
  - [3. Concepts](#3-concepts)
  - [4. Steps](#4-steps)
- [Custom Operator](#custom-operator)
  - [1. Goal](#1-goal-1)
  - [2. Concepts](#2-concepts)
  - [3. Steps](#3-steps)
    - [3.1. before __init__](#31-before-init)
    - [3.2. __init__](#32-init)
    - [3.3. execute()](#33-execute)
- [Custom Sensor](#custom-sensor)
  - [1. Goal](#1-goal-2)
  - [2. Concepts](#2-concepts-1)
  - [3. Steps](#3-steps-1)

<br />

# Custom Hook

## 1. Goal
* simplifies the complexity of interaction with APIs
* keep the API-specific code in one place to be easily reused

<br />

## 2. Methods
* encapsulate codes into a reusable Airflow hook
  > not directly using get_conn() outside the hook is good for
    * not breaking encapsulation - hide the internal details - which can change the internal details without affecting outside implementation

<br />

## 3. Concepts
* all hooks are subclasses of BaseHook class

<br />

## 4. Steps
1. define an **init** method that includes only required arguments since there are many arguments in BaseHook class
2. follow the expected structure of other similar Airflow Hook
   * e.g. get_conn(): responsible for setting up a connection to an external system
3. add connection credentials in Airflow
    * Airflow UI: Admin > Connections

4. make get_conn() fetch the **connection details** (connection credentials) from the **metastore** via a given **connection ID**
5. (optional) require the connection is specified through raising error instead of supplying defaults

    ```python
    if config.login:
        session.auth = (config.login, config.password)
    ```
6. Avoid fetching the connection credentials from the metastore when calling to get_conn() every time. Caching session and base_url as protected variables in the class

    ```python
    def get_conn():
        self.session = None
        self._base_url = None
        if self.session is None:
            ...
        return self._session, self._base_url
    ``` 

<br />

# Custom Operator

## 1. Goal
* avoid considerable code duplication and extra effort when reusing functions in multiple DAGs
* when operators are more often with different parameters to be set, it is appropriate to use custom operator

## 2. Concepts
* all hooks are subclasses of BaseOperator class

## 3. Steps

### 3.1. before __init__
6. instead to hardcode date parameters, using `templates_fields`
   > tell Airflow to template these instance variables on operators

### 3.2. __init__
1. make sure default DAG arguments `@apply_defaults` are passed to the __init__ method of the custom operators

2. use **kwargs to forward the generic arguments to the __init__ of the BaseOperator class in order to avoid listing all arguments explicitly
   > BaseOperator takes a large number of generic arguments to define the basic behavior of operators.
    
3. filter required parameters in __init__


### 3.3. execute()
4. follow the expected structure of operators
    * e.g. `def execute(self, context)`
      * main method called when executing the operator
      * context: a dict including all the Airflow context variables
        * When Airflow runs a task, it collects several variables and passes these to the context argument on the execute() method. These variables hold information about the current task
        * context is null: make Airflow not render any arguments except for self-defined arguments in functions

5. use logger provided from the BaseOperator class, available in the self.log property

<br />

# Custom Sensor

## 1. Goal
* make a custom sensor for our systems

## 2. Concepts
* all sensors are subclasses of BaseSensorOperator class

## 3. Steps
1. implement a `poke` method instead of `execute` method
   * `poke` is expected to return a **Boolean** value 
     * Process:
       * if the sensor condition is true, allow downstream tasks to start execution
       * if false, the sensor sleeps for seconds and check the conditions again until the condition becomes true
2. check condition
   * to check at least only one record, instead of all records 