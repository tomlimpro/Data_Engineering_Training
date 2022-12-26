from airflow.decorators import dag, task
import pendulum
import requests 
import xmltodict
import os

# Interaction avec la database postgresql
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
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

    # Import de postgres.hook
    @task()
    def load_episodes(episodes):
        hook = PostgresHook(postgres_conn_id='postgres_localhost')
        stored = hook.get_pandas_df("SELECT * from episodes;")
        new_episodes = []
        for episode in episodes:
            if episode["link"] not in stored["link"].values:
                filename = f"{episode['link'].split('/')[-1]}.mp3"
                new_episodes.append([episode["link"],episode["title"],episode["pubDate"], episode["description"], filename])
        hook.insert_rows(table="episodes", rows=new_episodes, target_fields=["link", "title","published","description","filename"])
    
    load_episodes(podcast_episodes)

    @task()
    def download_episodes(episodes):
        for episode in episodes:
            filename = f"{episode['link'].split('/')[-1]}.mp3"
            audio_path = os.path.join("episodes",filename)
            if not os.path.exists(audio_path):
                print(f"Downloading {filename}")
                audio = requests.get(episode["enclosure"]["@url"])
                with open(audio_path, "wb+") as f:
                    f.write(audio.content)
    
    download_episodes(podcast_episodes)
summary = podcast_summary2()