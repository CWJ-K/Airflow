<!-- omit in toc -->
# Introduction
Dynamic references are important concepts in Airflow. It looks like Python string format, however, the string arguments are limited in Airflow.

<br />

<!-- omit in toc -->
# Table of Contents
- [Fundamental Concepts](#fundamental-concepts)
  - [1. Airflow template](#1-airflow-template)
- [Dynamic References](#dynamic-references)
  - [1. BashOperator](#1-bashoperator)
  - [2. PythonOperator](#2-pythonoperator)
    - [2.1. context[key]](#21-contextkey)
    - [2.2. key](#22-key)
    - [2.3. op_kwargs:](#23-op_kwargs)
    - [2.4. op_args](#24-op_args)
  - [3. Example](#3-example)

<br />

# Fundamental Concepts

<br />

## 1. Airflow template
* define code between **double curly braces** is to be evaluated at runtime

<br />

# Dynamic References
* Use Airflow's **Jinja** based template syntax to reference parameters.

* Not all operator arguments can be templates
  * Available parameters can be found in [Templates reference](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html).
  
* Each operators has their different templating formats

<br />

## 1. BashOperator
* only one way: using Jinja

<br />

## 2. PythonOperator
* PythonOperator uses a function instead of string arguments, which can not use Jinja-templated. Instead, PythonOperator uses function arguments
* Airflow will pass a dictionary of arguments to the function In PythonOperator

    ```python
    # print a dictionary of arguments passed by Airflow

    def _print_context(**context):
    print(context)

    print_context = PythonOperator(
        task_id="print_context", python_callable=_print_context, dag=dag
    )
    ```

* There are multiple methods to call parameters


### 2.1. context[key]

```python
def _print_context(**context):
    start = context["execution_date"]
    end = context["next_execution_date"]
    print(f"Start: {start}, end: {end}")
```

<br />

### 2.2. key
* will pass a dictionary of arguments, but check whether arguments are in the function's expected arguments. If not, the arguments are put into context. If yes, the arguments are passed to the function
  * it is optional to put **context in the function

    ```python
    def _print_context(execution_date, **context):
        start = execution_date
        print(start)
    ```
    
<br />    

### 2.3. op_kwargs: 
*  can custom parameters
*  pass a dictionary of arguments
    
    ```python
    def _get_data(year, month, day, hour, output_path, **_):
        url = (
            "https://dumps.wikimedia.org/other/pageviews/"
            f"{year}/{year}-{month:0>2}/pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
        )
        request.urlretrieve(url, output_path)


    get_data = PythonOperator(
        task_id="get_data",
        python_callable=_get_data,
        op_kwargs={
            "year": "{{ execution_date.year }}",
            "month": "{{ execution_date.month }}",
            "day": "{{ execution_date.day }}",
            "hour": "{{ execution_date.hour }}",
            "output_path": "/tmp/wikipageviews.gz",
        },
        dag=dag,
    )
    ```

* the value of key can use brackets
  
   ```python
    def _fetch_pageviews(pagenames):
        result = dict.fromkeys(pagenames, 0)
        with open("/tmp/wikipageviews", "r") as f:
            for line in f:
                domain_code, page_title, view_counts, _ = line.split(" ")
                if domain_code == "en" and page_title in pagenames:
                    result[page_title] = view_counts

    print(result)
    # Prints e.g. "{'Facebook': '778', 'Apple': '20', 'Google': '451', 'Amazon': '9', 'Microsoft': '119'}"


    fetch_pageviews = PythonOperator(
        task_id="fetch_pageviews",
        python_callable=_fetch_pageviews,
        op_kwargs={"pagenames": {"Google", "Amazon", "Apple", "Microsoft", "Facebook"}},
        dag=dag,
    )
    ```

<br />

### 2.4. op_args
*  can custom parameters
*  pass a list

    ```python
    get_data = PythonOperator(
        task_id="get_data",
        python_callable=_get_data,
        op_args=["/tmp/wikipageviews.gz"],
        dag=dag,
    )
    ```

<br />

## 3. Example
* Execution Date of Airflow is not actually date, but datetime type

    ```python
    # assign dynamic parameters - execution date, next execution date - into tasks

    fetch_objects = BashOperator(
        task_id = 'fetch_objects',
        bash_command = (
            "mkdir -p /data/events && "
            "curl -o /data/events.json "
            "http://events_api:5000/events? "
            "start_date={{execution_date.strftime('%Y-%m-%d')}}&"
            "end_date={{next_execution_date.strftime('%Y-%m-%d')}}"
        ),
        dag=dag,
    )
    ```

