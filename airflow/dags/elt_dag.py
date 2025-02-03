from datetime import datetime, timedelta
import subprocess

from docker.types import Mount

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

def run_elt_script():
    script_path = "/opt/airflow/elt/elt.py"
    result = subprocess.run(["python", script_path], 
                             capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)

dag = DAG(
    'elt_and_dbt', # name of DAG
    default_args=default_args,
    description='An ELT workflow with dbt',
    start_date=datetime(2023, 10, 28),
    catchup=False
)

# Task 1 - run the ELT script
t1 = PythonOperator(
    task_id="run_elt_script",
    python_callable=run_elt_script,
    dag=dag
)

# Task 2 - run the DBT transformations
# this is basically what's in the docker compose dbt service but in Airflow
t2 = DockerOperator(
    task_id="run_dbt",
    image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    command=[
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/opt/dbt",
        "--full-refresh"
    ],
    auto_remove=True,
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    mounts=[
        Mount(source="/home/coco/git/data-engineering-basics/custom_postgres",
              target='/opt/dbt',
              type='bind'),
        Mount(source="/home/coco/.dbt",
              target='/root', 
              type='bind')
    ],
    dag=dag
)

# make sure t1 runs before t2
t1 >> t2
