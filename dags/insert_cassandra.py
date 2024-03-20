from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.apache.cassandra.hooks.cassandra import CassandraHook
from datetime import datetime
from uuid import uuid4
import requests
import json

dag = DAG("Airflow_and_Cassandra",
    description="A simple DAG that helps to insert dummy data into Cassandra Database",
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["ETL_jobs"])

def get_rest_api_data(**context):
    task_instance = context["ti"]

    url = "https://api.data.gov.my/data-catalogue?id=hies_state" 
    response_json = requests.get(url=url).json()

    task_instance.xcom_push("json_data", response_json)

def insert_dummy_data_into_cassandra_db(**context):
    task_instance = context["ti"]

    Live_data = task_instance.xcom_pull(task_ids='get_rest_api_data',
                                            key='json_data'
                                            )

    hook = CassandraHook(cassandra_conn_id='cassandra_default')
    session = hook.get_conn()

    for data in Live_data:
        query = """
            INSERT INTO hies.data_state (uuiid, date, state, gini, poverty, income_mean, income_median, expenditure_mean)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        session.execute(query, (uuid4(), data["date"], data["state"], str(data["gini"]), str(data["poverty"]), str(data["income_mean"]), str(data["income_median"]), str(data["expenditure_mean"])))

get_data_from_api = PythonOperator( 
    task_id="get_rest_api_data", 
    python_callable=get_rest_api_data, 
    dag=dag
)

insert_dummy_data = PythonOperator(
    task_id="insert_dummy_data",
    python_callable=insert_dummy_data_into_cassandra_db,
    dag=dag,
)

get_data_from_api >> insert_dummy_data