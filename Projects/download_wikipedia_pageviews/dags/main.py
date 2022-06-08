from ast import operator
from urllib import request

import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from functions import _get_data, _fetch_pageviews

dag = DAG(
    dag_id='wiki_pageviews',
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval='@hourly',
    template_searchpath='/tmp',
    max_active_runs=1
)


get_data = PythonOperator(
    task_id='get_wiki_pageviews_data',
    python_callable=_get_data,
    op_kwargs={
        'year': '{{ execution_date.year }}',
        'month': '{{ execution_date.month }}',
        'day': '{{ execution_date.day }}',
        'hour': '{{ execution_date.hour }}',
        'output_path': '/tmp/wikipageviews.gz'
    },
    dag=dag,
)

extract_gz = BashOperator(
    task_id='extract_gz',
    bash_command='gunzip --force /tmp/wikipageviews.gz', 
    dag=dag
)


fetch_pageviews = PythonOperator(
    task_id="fetch_pageviews",
    python_callable=_fetch_pageviews,
    op_kwargs={"pagenames": {"Google", "Amazon", "Apple", "Microsoft", "Facebook"}},
    dag=dag,
)

write_to_postgres = PostgresOperator(
    task_id="write_to_postgres",
    postgres_conn_id="my_postgres",
    sql="postgres_query.sql",
    dag=dag,
)

get_data >> extract_gz >> fetch_pageviews >> write_to_postgres

