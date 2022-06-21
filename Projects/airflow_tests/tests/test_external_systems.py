import os
import pytest
from airflow.models import Connection
from pytest_docker_tools import fetch, container

from dags.custom.movielens_operator import MovielensToPostgresOperator
from dags.custom.hook import MovielensHook
from airflow.providers.postgres.hooks.postgres import PostgresHook


postgres_image = fetch(repository='postgres:11.1-alpine')

postgres_container = container(
    image='{postgres_image.id}',
    environments={
        'POSTGRES_USER': 'testuser',
        'POSTGRES_PASSWROD': 'testpass',
    },
    ports={'5432/tcp': None},
    volumes={
        os.path.join(os.path.dirname(__file__), 'postgres-init.sql'):{
            'bind': '/docker-entrypoint-initdb.d/postgres-init.sql'
        }
    }
)


@pytest.fixture
def test_dag():
    return DAG(
        "test_dag",
        default_args={"owner": "airflow", "start_date": datetime.datetime(2015, 1, 1)},
        schedule_interval="@daily",
    )


def test_movielens_to_postgres_operator(mocker, test_dag, postgres):
    mocker.patch.object(
        MovielensHook,
        'get_connection',
        return _value=Connection(
            conn_id='test',
            login='airflow',
            password='airflow',
        ),
    )

    mocker.patch.object(
        PostgresHook,
        'get_connection',
        return _value=Connection(
            conn_id='postgres',
            conn_type='postgres',
            host='localhost',
            login='testuser',
            password='testpass',
            port=postgres.ports['5432/tcp'][0],
        ),
    )

task = MovielensToPostgresOperator(
    task_id='test',
    movielens_conn_id='movielens_id',
    start_date='{{ prev_ds }}',
    end_date='{{ ds }}',
    postgres_conn_id='postgres_id',
    insert_query=(
        '''INSERT INTO movielens
        (movieId,rating,ratingTimestamp,userId,scrapeTime)
        VALUES ({0}, "{{ macros.datetime.now() }}")
        '''
    ),
    dag=test_dag,
)

pg_hook = PostgresHook()

row_count = pg_hook.get_first('SELECT COUNT(*) FROM movielens')[0]
assert row_count == 0

pytest.helpers.run_airflow_task(task, test_dag)

row_count = pg_hook.get_first('SELECT COUNT(*) FROM movielens')[0]
assert row_count > 0


def test_call_fixture(postgres_image):
    print(postgres_image)


def test_call_fixture(postgres_container):
    print(
        f'''
        Running Postgres container named {postgres_container.name}
        on port {postgres_container.ports["5432/tcp"][0]}
        '''
    )


