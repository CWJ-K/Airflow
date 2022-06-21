from email.policy import default
import json
import os
from collections import defaultdict, Counter

from airflow.models import BaseOperator

from dags.custom.hook import MovielensHook


class MovielensPopularityOperator(BaseOperator):
    '''
    TODO
    '''
    def __init__(
        self,
        conn_id,
        start_date,
        end_date,
        min_ratings=4,
        top_n=5
    ) -> None:
        super().__init__(**kwargs)
        self._conn_id = conn_id
        self._start_date = start_date
        self._end_date = end_date
        self._min_ratings = min_ratings
        self._top_n = top_n

    
    def execute(self, context):
        with MovielensHook(self._conn_id) as hook:
            ratings = hook.get_ratings(
                start_date=self._start_date,
                end_date=self._end_date,
            )

            rating_counter = defaultdict(Counter)
            for rating in ratings:
                rating_counter[rating['movieId']].update(count=1, rating=rating['rating'])
            
            averages = {
                movie_id: (
                    rating_counter['rating'] / rating_counter['count'], rating_counter['count']
                )

                for movie_id, rating_counter['count'] in rating_counter.items()
                if rating_counter['count'] >= self._min_ratings
            }

            return sorted(averages.items(), key=lambda x: x[1], reverse=True)[: self._top_n]