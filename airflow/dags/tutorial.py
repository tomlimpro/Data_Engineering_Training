"""
Exemple d'un simple pipeline
vu ici : https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html

"""

from datetime import datetime, timedelta
from textwrap import dedent

# DAG object 
from airflow import DAG

# import Operator
from airflow.operators.bash import BashOperator

with DAG(
    "tutorial",
    default_args={
        "depends_on_past" : False,
        "email" : ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries" : 1,
        "retry_delay" : timedelta(minutes=5),
    },
    description="tutorial DAG",
    start_date=datetime(2022, 12, 24),
    catchup=False,
    tags=["example"],
) as dag:
    # t1, t2 et t3 sont des exemples de tâches créées par instances
    """
    Pour utiliser un opérateur dans un DAG, on doit l'instancier comme une tâche. Les tâches déterminent comment exécuter le travail de l'opérateur dans le contexte d'un DAG.
    Nous instancions l'opérateur BashOperator en deux tâches distinctes afin d'exécuter deux scripts bash distincts. 
    Le premier argument de chaque instanciation, task_id, sert d'identifiant unique pour la tâche. 

    """
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )
    t2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
        retries=3,
    )
    t1.doc_md = dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
    **Image Credit:** Randall Munroe, [XKCD](https://xkcd.com/license.html)
    """
    )
    dag.doc_md = __doc__ # à condition qu'on a un docstring au début du DAG
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
    {% endfor %}
    """
    )
    t3 = BashOperator(
        task_id = "templated",
        depends_on_past=False,
        bash_command=templated_command,
    )

    """
    Lorsque la tâche t1 est suive de [t2,t3], cela signique que les tâches t2,t3 dépendent de la tâche t1. 
    Cela signifie que la tâche t1 doit être exécutée avant que les tâches t2 et t3 ne soient exécutées. 
    
    """
    t1 >> [t2,t3]