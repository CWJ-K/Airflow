import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator 

from get_pictures import _get_pictures

dag = DAG(
    dag_id='download_rocket_launches',
    description='Download rocket pictures of recently launched rockets',
    start_date=airflow.utils.dates.days_ago(14),
    schedule_interval='@daily' 
)

download_launches = BashOperator(
    task_id='download_launches',
    bash_command='''
        curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'
    ''',
    dag=dag
)


get_pictures = PythonOperator(
    task_id='get_pictures',
    python_callable=_get_pictures,
    dag=dag
)


notify = BashOperator(
    task_id='notify',
    bash_command='echo "There are now $(ls /tmp/images/ | wc -l) images"',
    dag=dag
)



download_launches >> get_pictures >> notify

