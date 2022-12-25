from airflow.decorators import dag, task
import pendulum
import requests
import xmltodict
@dag(
    dag_id='podcast_summary2',
    schedule_interval='@daily',
    start_date=pendulum.datetime(2022,12,25),
    catchup=False
)

def podcast_summary2():
    """
    1ère tache : Get episodes
    """
    @task()
    def get_episodes():
        data = requests.get("https://www.marketplace.org/feed/podcast/marketplace/")
        feed = xmltodict.parse(data.text)
        episodes = feed["rss"]["channel"]["item"]
        print(f"Found{len(episodes)} episodes.")
        return episodes

    podcast_episodes = get_episodes()
summary = podcast_summary2()