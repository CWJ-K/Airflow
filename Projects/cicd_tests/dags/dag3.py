import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash import BashOperator

dag = DAG(
    dag_id="dag3",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval=None,
)

BashOperator(task_id="without_bash_comment", dag=dag)