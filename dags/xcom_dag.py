from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
 
from datetime import datetime
 
def _t1(ti):
    ti.xcom_push(key='my_key', value=33)
 
def _t2(ti):
    ti.xcom_pull(task_id='t1', key='my_key')

def condition_for_task(ti):
    res = ti.xcom_pull(task_id='t1', key='my_key')

    if res == 33:
        return 't2'
    else:
        return 't3'
 
with DAG("xcom_dag", start_date=datetime(2022, 1, 1), 
    schedule_interval='@daily', catchup=False) as dag:
 
    t1 = PythonOperator(
        task_id='t1',
        python_callable=_t1
    )

    branch = BranchPythonOperator(
        task_Id='branch',
        python_callable=condition_for_task
    )
 
    t2 = PythonOperator(
        task_id='t2',
        python_callable=_t2
    )
 
    t3 = BashOperator(
        task_id='t3',
        bash_command="echo ''"
    )
 
    t1 >> branch >> [t2, t3]