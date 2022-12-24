
# Airflow

Airflow est un outil de planification de tâches et de flux de travail qui vous permet de planifier, 
de suivre et de surveiller l'exécution de tâches de manière automatisée. 
Il est conçu pour être facile à utiliser, scalable et fiable.

Framework orienté batch qui nous permet de construire facilement des pipelines de données planifiés en Python.
Imaginer un "*workflow as code*" capable d'exécuter toute opération que nous pouvons mettre en oeuvre en Python.

Airflow n'est pas un outil de traitement des données en soi. C'est un *orchestration software*. Nous pouvons imaginer Airflow 
comme une sorte d'araignée dans une toile. Assis au milieu, tirant toutes les ficelles et coordonnant la charge de travail 
de nos pipelines de données.

Un pipeline de données se compose généralement de plusieurs tâches ou actions qui doivent être exécutées dans un ordre spécifique. 
Apache Airflow modélise un piple comme un *DAG* (directec acyclic graph). 

Cette approche nous permet d'exécuter des tâches indépendantes en parallèle, ce qui permet de gagner du temps et de l'argent.
En outre, nous pouvons diviser un pipeline de données en plusieurs tâches plus petites. Si une tâche échoue, nous pouvons 
seulement réexécuter la tâche qui a échoué et les tâches en aval, au lieu de réexécuter le flux de travail complet.

## Les composantes principales

Airflow __scheduler__ - le "coeur" d'Airflow, qui analyse les DAGs, vérifie les intervalles programmés et transmet les tâches aux travailleurs

Airflow __worker__ - reprend les tâches et effectue réellement le travail.

Airflow __webserver__ - fournit l'interface utilisateur principale pour visualiser et surveiller les DAGs et leurs résultats.


![Logo](https://miro.medium.com/max/4800/1*z3MNHDV9eTTLGikvucGEKw.webp)


## Demarrer Airflow

Pour démarrer les services d'Airflow, il faut se placer dans le repertoir du docker-compose puis : 

/airflow
```bash
  docker-compose up -d 
```

