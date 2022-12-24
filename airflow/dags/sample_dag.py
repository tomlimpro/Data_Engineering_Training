"""
DAG est la classe de base utilisée pour définir un workflow Airflow

EmptyOperator est une classe de base pour définir une tache vide 
BashOperator est utilisée pour exécuter une commande Bash

"""
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator

from datetime import datetime

"""
Nouvelle instance de 'DAG' en utilisant le contexte de gestion de ressources 'with'. 
Cette instance de 'DAG' définie avec l'identifiant 'dag_id'; la date de démarrage 'start_date' et la fréquence de planification 'schedule_interval'

"""
with DAG(
    dag_id = 'first_sample_dag',
    start_date=datetime(2022,12,24),
    schedule_interval = None
) as dag:

    # Les instances EmptyOperator sont utilisés pour définir les tâches de début et de fin du workflow
    start_task = EmptyOperator(
        task_id = 'start'
    )

    # l'instance de BashOperator est utilisée pour exécuter la commande 'echo "HelloWorld!"' lors de l'exécution du workflow. 
    print_hello_world = BashOperator(
        task_id = 'print_hello_world',
        bash_command='echo "HelloWorld!"'
    )

    end_task = EmptyOperator(
        task_id = 'end'
    )

"""
Les opérateurs de chaînage '>>' pour définir l'ordre de dépendance entre les tâches. 
La tâche de début dépend de la tâche d'impression "HelloWorld!" qui à son tour dépend de la tâche de fin.
Cela signifie que la tâche de début sera exécutée en premier, suivie de la tâche d'impression "HelloWorld!"

"""
start_task >> print_hello_world
print_hello_world >> end_task
