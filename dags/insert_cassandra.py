from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.apache.cassandra.hooks.cassandra import CassandraHook
import uuid
from datetime import datetime
from uuid import uuid4

dag = DAG("Airflow_and_Cassandra",
    description="A simple DAG that helps to insert dummy data into Cassandra Database",
    schedule_interval=timedelta(minutes=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["ETL_jobs"])

def insert_dummy_data_into_cassandra_db():
    hook = CassandraHook(cassandra_conn_id='cassandra_default')
    session = hook.get_conn()

    # Generate some dummy data
    dummy_data = [
        {
            "uuiid": uuid4(),
            "source": "Dummy Source",
            "author": "Dummy Author",
            "category": "Dummy Category",
            "country": "Dummy Country",
            "description": "Dummy Description",
            "image": "Dummy Image URL",
            "language": "Dummy Language",
            "published_at": datetime.now().isoformat(),  # Convert datetime to string
            "title": "Dummy Title",
            "url": "Dummy URL"
        }
    ]


    # Insert dummy data
    for data in dummy_data:
        query = """
            INSERT INTO news.news_table (uuiid, source, author, category, country, description, image, language, published_at, title, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        session.execute(query, (data["uuiid"], data["source"], data["author"], data["category"], data["country"], data["description"], data["image"], data["language"], data["published_at"], data["title"], data["url"]))

insert_dummy_data = PythonOperator(
    task_id="insert_dummy_data",
    python_callable=insert_dummy_data_into_cassandra_db,
    dag=dag,
)

insert_dummy_data