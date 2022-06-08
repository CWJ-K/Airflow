import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator
from urllib import request

def _get_data(year, month, day, hour, output_path):
    url = (
        "https://dumps.wikimedia.org/other/pageviews/"
        f"{year}/{year}-{month:0>2}/pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    )
    request.urlretrieve(url, output_path)


def _fetch_pageviews(pagenames, execution_date):
    result = dict.fromkeys(pagenames, 0)
    with open('/tmp/wikipageviews', 'r') as f:
        for line in f:
            domain_code, page_title, view_counts, _ = line.split(" ")
            if domain_code == 'en' and page_title in pagenames:
                result[page_title] = view_counts
    
    with open('/tmp/postgres_query.sql', 'w') as f:
        for pagename, pageviewcount in result.items():
            f.write(
                'INSERT INTO pageview_counts VALUES ('
                f'"{pagename}", {pageviewcount}, "{execution_date}"'
                ');\n'
            )




