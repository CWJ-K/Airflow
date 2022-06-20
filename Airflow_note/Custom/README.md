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
