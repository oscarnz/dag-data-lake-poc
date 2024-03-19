FROM apache/airflow:latest
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
RUN pip install --no-cache-dir apache-airflow-providers-docker==2.1.0
RUN pip install --no-cache-dir apache-airflow-providers-apache-cassandra==2.1.3