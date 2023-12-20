from airflow import DAG
from airflow.operators.bash import BashOperator
from groups.group_downloads import download_task

 
from datetime import datetime
 
with DAG('group_dag', start_date=datetime(2022, 1, 1), 
    schedule_interval='@daily', catchup=False) as dag:

    # args = {'start_date': dag.start_date, 'schedule_interval':dag.schedule_int}
    downloads = download_task()

    check_files = BashOperator(
        task_id='check_files',
        bash_command='sleep 6'
    )

    downloads >> check_files