"""
## Print the number of people currently in space

This DAG pulls the number of people currently in space. The number is pulled
from XCom and was pushed by the `get_astronauts` task in the `example_astronauts` DAG.
"""
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow import Dataset
from airflow.models.baseoperator import chain
from pendulum import datetime

@dag(
    dag_id="my_astronauts_dag",
    start_date=datetime(2025, 1, 1),
    schedule=[Dataset("current_astronauts")],
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "Astro", "retries": 3},
    tags=["My First DAG!"],
)
def my_astronauts_dag():
    @task
    def print_num_people_in_space(**context) -> None:
        """
        This task pulls the number of people currently in space from XCom. The number is
        pushed by the `get_astronauts` task in the `example_astronauts` DAG.
        """

        num_people_in_space = context["ti"].xcom_pull(
            dag_id="example_astronauts",
            task_ids="get_astronauts",
            key="number_of_people_in_space",
            include_prior_dates=True,
        )

        print(f"There are currently {num_people_in_space} people in space.")
        return 0
    
    print_reaction = BashOperator(
      task_id="print_reaction",
      bash_command="echo This is awesome!",
    )
    
    chain(print_num_people_in_space(), print_reaction)

my_astronauts_dag()