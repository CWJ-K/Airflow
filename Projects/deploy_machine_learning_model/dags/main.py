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

from function import _extract_mnist_data

dag = DAG(
    dag_id='aws_classifier_for_handwritten_digits',
    schedule_interval=None,
    start_date=airflow.utils.dates.days_ago(3)
)

download_mnist_data = S3CopyObjectOperator(
    task_id='download_mnist_data',
    source_bucket_name='sagemaker-sample-data-eu-west-1',
    source_bucket_key='algorithms/kmeans/mnist/mnist.pkl.gz',
    dest_bucket_name='[bucket-name]',
    dest_bucket_key='mnist.pkl.gz',
    dag=dag
)

extract_mnist_date = PythonOperator(
    task_id='extract_mnist_data',
    python_callable=_extract_mnist_data,
    dag=dag
)

sagemaker_train_model = SageMakerTrainingOperator(
    task_id='sagemaker_train_model',
    config={
        'TrainingJobName': '''mnistclassifier-{{
            execution_date.strftime('%Y-%m-%d-%H-%M-%S') 
        }}''',
        'AlgorithmSpecification': {
            'TrainingImage': '43834646658.dkr.ecr.eu-west-1.amazonaws.com/kmeans:1',
            'TrainingInputMode': 'File',
        },
        'HyperParameters': {'k': '10', 'feature_dim': '784'},
        'InputDataConfig': [
            {
                'ChannelName': 'train',
                'DataSource': {
                    'S3DataSource': 'S3Prefix',
                    'S3Uri': 's3://[bucket_name]/mnist-data',
                    'S3DataDistributionType': 'FullyReplicated'
                }
            }
        ],
        'OutputDataConfig': {
            'S3OutputPath': 's3://[bucket_name]/mnistclassifier-output'
        },
        'ResourceConfig': {
            'InstanceType': 'ml.c4.xlarge',
            'InstanceCount': 1,
            'VolumeSizeInGB': 10,
        },
        'RoleArn': 'arn:aws:iam::297623009465:role/service-role/AmazonSageMaker-ExecutionRole-20180905T153196',
        'StoppingCondition': {'MaxRuntimeInSeconds': 24*60*60}
    },
    wait_for_completion=True,
    print_log=True,
    check_interval=10,
    dag=dag
)

sagemaker_deploy_model = SageMakerEndpointOperator(
    task_id='sagemaker_deploy_model',
    wait_for_completion=True,
    config={
        'Model': {
            'ModelName': '''mnistclassifier-{{ execution_date.strftime('%Y-%m-%d-%H-%M-%S') }}''',
            'PrimaryContainer': {
                'Image': '438346466558.dkr.ecr.eu-west-1.amazonaws.com/kmeans:1',
                'ModelDataUrl': (
                    's3://[bucket_name]/mnistclassifier-output/'
                    'mnistclassifier-{{execution_date.strftime("%Y-%m-%d-%H-%M-%S")'
                    'output/model.tar.gz'
                )
            },
            'ExecutionRoleArn': 'arn:aws:iam::297623009465:role/service-role/AmazonSageMaker-ExecutionRole-20180905T153196',
        },
        'EndpointConfig': {
            'EndpointConfigName': 'mnistclassifier-{{ execution_date.strftime("%Y-%m-%d-%H-%M-%S") }}',
            'ProductionVariants': [
                {
                    'InitialInstanceCount': 1,
                    'InstanceType': 'ml.t2.medium',
                    'ModelName': 'mnistclassifier',
                    'VariantName': 'AllTraffic'
                }
            ]
        },
        "Endpoint": {
            "EndpointConfigName": "mnistclassifier-{{ execution_date.strftime('%Y-%m-%d-%H-%M-%S') }}",
            "EndpointName": "mnistclassifier",
        },
    },
    dag=dag
)


download_mnist_data >> extract_mnist_date >> sagemaker_train_model >> sagemaker_deploy_model