FROM apache/airflow:2.10.5
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
COPY . /opt/airflow