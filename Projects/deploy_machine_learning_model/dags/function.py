from array import array
import gzip
import io
import pickle

import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.operators.s3_copy_object import S3CopyObjectOperator
from airflow.providers.amazon.aws.operators.sagemaker_endpoint import SageMakerEndpointOperator
from airflow.providers.amazon.aws.operators.sagemaker_endpoint import SageMakerTrainingOperator
from sagemaker.amazon.common import write_numpy_to_dense_tensor


def _extract_mnist_data():
    s3hook = S3Hook()

    mnist_buffer = io.BytesIO()
    mnist_obj = s3hook.get_key(
        bucket_name='[bucket_name]',
        key='mnist.pkl.gz'
    )

    mnist_obj.download_fileobj(mnist_buffer)

    mnist_buffer.seek(0)
    with gzip.GzipFile(fileobj=mnist_buffer, mode='rb') as f:
        train_set, _, _ = pickle.loads(f.read(), encoding='latin1')
        output_buffer = io.BytesIO()
        write_numpy_to_dense_tensor(
            file=output_buffer,
            array=train_set[0],
            labels=train_set[1],
        )

        output_buffer.seek(0)
        s3hook.load_file_obj(
            output_buffer,
            key='mnist_date',
            bucket_name='[bucket_name]',
            replace=True
        )