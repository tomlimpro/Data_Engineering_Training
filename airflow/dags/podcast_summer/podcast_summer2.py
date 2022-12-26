from airflow.decorators import dag, task
import pendulum
import requests
import xmltodict

# Interaction avec la database postgresql
from airflow.providers.postgres.operators.postgres import PostgresOperator

@dag(
    dag_id='podcast_summary2',
    schedule_interval='@daily',
    start_date=pendulum.datetime(2022,12,25),
    catchup=False
)

def podcast_summary2():
    # Créer la table "episodes"
    create_database = PostgresOperator(
        task_id="create_table_postgres",
        postgres_conn_id='postgres_localhost',
        sql="""
            CREATE TABLE IF NOT EXISTS episodes(
                link TEXT PRIMARY KEY,
                title TEXT,
                filename TEXT,
                published TEXT,
                description TEXT
            )
        """,
    )
    """
    1ère tache : Get episodes
    """
    @task()
    def get_episodes():
        data = requests.get("https://www.marketplace.org/feed/podcast/marketplace/")
        feed = xmltodict.parse(data.text)
        episodes = feed["rss"]["channel"]["item"]
        print(f"Found {len(episodes)} episodes.")
        return episodes

    podcast_episodes = get_episodes()
    # ici on run create_database() avant de get_episodes()
    create_database.set_downstream(podcast_episodes)
summary = podcast_summary2()