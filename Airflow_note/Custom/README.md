https://airflow.apache.org/docs/apache-airflow/stable/howto/custom-operator.html

<!-- omit in toc -->
# Introduction
Take notes of how to customize components in Airflow

<br />

<!-- omit in toc -->
# Table of Contents
- [Custom Hook](#custom-hook)
  - [Goal](#goal)
  - [Methods](#methods)
  - [Concepts](#concepts)
  - [Steps](#steps)
- [Custom Operator](#custom-operator)
  - [Goal](#goal-1)
  - [Concepts](#concepts-1)
  - [Steps](#steps-1)
    - [before __init__](#before-init)
    - [__init__](#init)
    - [execute()](#execute)
- [Custom Sensor](#custom-sensor)
  - [Goal](#goal-2)
  - [Concepts](#concepts-2)
  - [Steps](#steps-2)

# Custom Hook
## Goal
* simplifies the complexity of interaction with APIs
* keep the API-specific code in one place to be easily reused

<br />

## Methods
* encapsulate codes into a reusable Airflow hook
  > not directly using get_conn() outside the hook is good for
    * not breaking encapsulation - hide the internal details - which can change the internal details without affecting outside implementation

<br />

## Concepts
* all hooks are subclasses of BaseHook class

<br />

## Steps
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
## Goal
* avoid considerable code duplication and extra effort when reusing functions in multiple DAGs

## Concepts
* all hooks are subclasses of BaseOperator class

## Steps
### before __init__
6. instead to hardcode date parameters, using `templates_fields`
   > tell Airflow to template these instance variables on operators

### __init__
1. make sure default DAG arguments `@apply_defaults` are passed to the __init__ method of the custom operators

2. use **kwargs to forward the generic arguments to the __init__ of the BaseOperator class in order to avoid listing all arguments explicitly
   > BaseOperator takes a large number of generic arguments to define the basic behavior of operators.
    
3. filter required parameters in __init__


### execute()
4. follow the expected structure of operators
    * e.g. `def execute(self, context)`
      * main method called when executing the operator
      * context: a dict including all the Airflow context variables

5. use logger provided from the BaseOperator class, available in the self.log property

<br />

# Custom Sensor
## Goal
* make a custom sensor for our systems

## Concepts
* all sensors are subclasses of BaseSensorOperator class

## Steps
1. implement a `poke` method instead of `execute` method
   * `poke` is expected to return a **Boolean** value 
     * Process:
       * if the sensor condition is true, allow downstream tasks to start execution
       * if false, the sensor sleeps for seconds and check the conditions again until the condition becomes true
2. check condition
   * to check at least only one record, instead of all records 