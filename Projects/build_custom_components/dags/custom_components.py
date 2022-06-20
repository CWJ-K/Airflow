import datetime as dt

from airflow import DAG

from custom.operator import MovielensFetchRatingsOperator
from custom.sensor import MovielensRatingsSensor


with DAG(
    dag_id="custom_components",
    description="Fetches ratings from the Movielens API using custom components.",
    start_date=dt.datetime(2019, 1, 1),
    end_date=dt.datetime(2019, 1, 10),
    schedule_interval="@daily",
) as dag:

    wait_for_ratings = MovielensRatingsSensor(
        task_id="wait_for_ratings",
        conn_id="movielens",
        start_date="{{ds}}",
        end_date="{{next_ds}}",
    )

    fetch_ratings = MovielensFetchRatingsOperator(
        task_id="fetch_ratings",
        conn_id="movielens",
        start_date="{{ds}}",
        end_date="{{next_ds}}",
        output_path="/data/custom_sensor/{{ds}}.json",
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



    wait_for_ratings >> fetch_ratings >> rank_movies