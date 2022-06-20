import datetime as dt
import logging
import json
import os

from airflow import DAG
from airflow.operators.python import PythonOperator

from custom.hooks import MovielensHook


with DAG(
    dag_id='use_hook',
    description='Fetches ratings from the Movielens API using a custom hook.',
    start_date=dt.datetime(2019, 1, 1),
    end_date=dt.datetime(2019, 1, 10),
    schedule_interval='@daily'
) as dag:


    def _fetch_ratings(conn_id, templates_dict, batch_size=1000, **_):
        logger = logging.getLogger(__name__)

        start_date = templates_dict['start_date']
        end_date = templates_dict['end_date']
        output_path = templates_dict['output_path']

        logger.info(f'Fetching ratings for {start_date} to {end_date}')
        hook = MovielensHook(conn_id=conn_id)
        ratings = list(
            hook.get_ratings(
                start_date=start_date, end_date=end_date, batch_size=batch_size
            )
        )
        logger.info(f"Fetched {len(ratings)} ratings")

        logger.info(f"Writing ratings to {output_path}")

        output_dir = os.path.dirname(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        with open(output_dir, 'w') as file_:
            json.dump(ratings, fp=file_)
    
    fetch_ratings = PythonOperator(
        task_id='fetch_ratings',
        python_callable=_fetch_ratings,
        op_kwargs={'conn_id': 'movielens'},
        templates_dict={
            'start_date': '{{ds}}',
            'end_date': '{{next_ds}}',
            'output_path': '/data/custom_hook/{{ds}}.json',
        },
    )


    def _rank_movies(templates_dict, min_ratings=2, **_):
        input_path = templates_dict['input_path']
        output_path = templates_dict['output_path']

        ratings = pd.read_json(input_path)
        ranking = rank_movies_by_rating(ratings, min_ratings=min_ratings)

        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)

        ranking.to_csv(output_path, index=True)


    rank_movies = PythonOperator(
        task_id='rank_movies',
        python_callable=_rank_movies,
        templates_dict={
            'input_path': '/data/python/ratings/{{ds}}.json',
            'output_path': '/data/python/rankings/{{ds}}.csv',
        }
    )



    fetch_ratings >> rank_movies