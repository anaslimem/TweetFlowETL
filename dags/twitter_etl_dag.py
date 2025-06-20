from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import tweepy
import json
import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import logging

load_dotenv()

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "tweets"
BLOB_NAME = "elonmusk_tweets.json"
LOCAL_FILE = "/opt/airflow/elonmusk_tweets.json"

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 6, 1),
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='twitter_etl_dag',
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    description='Extract tweets, transform and load to Azure Blob Storage.',
) as dag:

    def extract_tweets(ti, **kwargs):
        client = tweepy.Client(bearer_token=BEARER_TOKEN)
        user = client.get_user(username='elonmusk')
        user_id = user.data.id
        response = client.get_users_tweets(
            id=user_id,
            max_results=10,
            tweet_fields=["created_at", "lang", "source", "public_metrics"]
        )
        tweets_data = response.data or []
        ti.xcom_push(key='raw_response', value=[tweet.data for tweet in tweets_data])

    def transform_tweets(ti, **kwargs):
        tweets = ti.xcom_pull(key='raw_response', task_ids='extract_tweets') or []
        transformed = []
        for tweet in tweets:
            transformed.append({
                'id': tweet['id'],
                'text': tweet['text'],
                'created_at': tweet['created_at'],
                'author_id': tweet.get('author_id'),
                'lang': tweet.get('lang'),
                'source': tweet.get('source'),
                'public_metrics': tweet.get('public_metrics')
            })
        with open(LOCAL_FILE, 'w') as f:
            json.dump(transformed, f, indent=4)
        logging.info(f"Transformed {len(transformed)} tweets and saved to {LOCAL_FILE}")

    def load_to_azure(**kwargs):
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        try:
            blob_service_client.create_container(CONTAINER_NAME)
        except Exception as e:
            logging.info(f"Container '{CONTAINER_NAME}' exists or error: {e}")

        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)
        with open(LOCAL_FILE, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        logging.info("✅ Uploaded to Azure Blob Storage.")

    extract_task = PythonOperator(
        task_id='extract_tweets',
        python_callable=extract_tweets,
    )

    transform_task = PythonOperator(
        task_id='transform_tweets',
        python_callable=transform_tweets,
    )

    load_task = PythonOperator(
        task_id='load_to_azure',
        python_callable=load_to_azure,
    )

    extract_task >> transform_task >> load_task
