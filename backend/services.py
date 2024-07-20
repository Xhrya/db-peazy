import json
from datetime import datetime
from typing import List, Optional
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_community import BigQueryVectorStore
from google.cloud import storage, bigquery
import numpy as np
import uuid
import shutil

BUCKET = 'audio-file-dbpeazy'
PROJECT_ID = "hack-team-db-peazy"
DATASET = "memoryDataset"
TABLE = "Memories"
REGION = "us-central1"

embedding = VertexAIEmbeddings(
    model_name="textembedding-gecko@latest", project=PROJECT_ID
)

store = BigQueryVectorStore(
    project_id=PROJECT_ID,
    dataset_name=DATASET,
    table_name=TABLE,
    location=REGION,
    embedding=embedding
)


def upload_file_to_bucket(file, bucket_name, name):
    sc = storage.Client(project=PROJECT_ID)
    bucket = sc.bucket(bucket_name)
    # Create a blob object
    blob = bucket.blob(str(name) + '.wav')

    # Upload the file
    blob.upload_from_file(file)


def get_audio_file(bucket_name, id):
    sc = storage.Client(project=PROJECT_ID)
    bucket = sc.bucket(bucket_name)

    blob = bucket.get_blob(id + '.wav')
    return blob.download_to_file()


def add_memory_to_table(transcript, datetime, id):
    store.add_texts(transcript, metadatas=[{"transcript": transcript, "datetime": datetime, "id": id}])


def get_k_closest_memories(query, k):
    query_vector = embedding.embed_query(query)
    memories = store.similarity_search_by_vector(query_vector, k=k)
    return memories


def get_random_rows(num_rows=10):
    bq = bigquery.Client(project=PROJECT_ID)

    query = f"""
    SELECT datetime, id, transcript
    FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
    ORDER BY RAND()
    LIMIT {num_rows}
    """

    query_job = bq.query(query)

    results = query_job.result()  # Wait for the job to complete.

    # Convert the result to a list of dictionaries for easier handling
    rows = [dict(row) for row in results]

    return rows


def get_memory(id):
    bq = bigquery.Client(project=PROJECT_ID)

    query = f"""
    SELECT datetime, id, transcript
    FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
    WHERE id = {str(id)}
    """

    query_job = bq.query(query)

    results = query_job.result()  # Wait for the job to complete.

    # Convert the result to a list of dictionaries for easier handling
    rows = [dict(row) for row in results]

    return rows


def save_wav_file(file_obj, destination):
    with open(destination, 'wb') as destination_file:
        shutil.copyfileobj(file_obj, destination_file)

def get_audio_file(id):
    sc = storage.Client(project=PROJECT_ID)
    bucket = sc.bucket(BUCKET)
    # Create a blob object
    blob = bucket.get_blob(str(id) + '.wav')
    blob.download_to_filename('temp_files/temp_download.wav')


if __name__ == "__main__":
    print(get_audio_file(45393717))
