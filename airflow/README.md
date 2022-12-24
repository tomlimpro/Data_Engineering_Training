
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

Airflow __webserver__ - fournit l'interface utilisateur principale pour visualiser et surveiller les DAGs et leurs résultats. Il affiche l'état des travaux et 
permet d'interagir avec les bdd et de lire les fichiers journaux à partir des remote file stores comme S3, GCS, etc...

Airflow __database__ : L'état des DAG et des tâches sont sauvegardés dans la bdd afin que le planning se souvienne des informations relatives aux métadonnées. 
Airflow utilise SQLAlchemy et Object Relation Mapping (ORM) pour se connecter à la BDD et stocke les informations pertinentes comme les intervalles de planification, les stats et instances de tâches.

Airflow __executor__ : Décide de la manière dont le travail est effectué.

Exemple Executors : 
* `SequentialExecutor` : peut exécuter une seule tâche à un moment donné. Il ne peut pas exécuter des tâches en parallèle. Il est utile dans les situations de test ou de débogage.
* `LocalExecutor` : permet le parallélisme et l'hyperthreading. Il est idéal pour exécuter Airflow sur une machine locale ou un seul nœud.
* `CeleryExecutor` : Cet exécuteur est le moyen privilégié d'exécuter un cluster Airflow distribué.
* `KubernetesExecutor` : appelle l'API Kubernetes pour créer des pods temporaires pour chacune des instances de tâches à exécuter.

Voir le lien pour les executors : https://airflow.apache.org/docs/apache-airflow/stable/executor/index.html#executor-types



![Logo](https://miro.medium.com/max/4800/1*z3MNHDV9eTTLGikvucGEKw.webp)

----
![Logo](https://miro.medium.com/max/4800/1*nGt96_U37FzJdW8tCqBw0Q.webp)


## __Les Avantages__
* __Open-source__ : Facile à installer et utilisation rapide
* __Scalable__ : Scalable up and down. Peut être déployé sur un seul serveur ou mis à l'échelle pour de grands déploiements avec de nombre noeuds.
* __Flexible__ : Airflow a été conçu pour fonctionner avec l'architecture standard de la plupart des environnements de développement logiciels mais sa flexibilité permet de nombreuses possibilités de personnalisation.
* __Monitoring abilities__ : Permet de diversifier les méthodes de surveillance. Par exemple, pour visualiser l'état des tâches à partir de l'UI.
* __Code-first platform__ : Cette dépendance au code donne la liberté d'écrire le code qu'on souhaite exécuter à chaque étape du pipeline.

## __Directed Acyclic Graph__
Les workflows sont définits à l'aide DAG, qui sont composés de tâches à exécuter ainsi que de leurs dépendances connectées. Chaque DAG représente un groupe de tâches qu'on souhaite exécuter, et ils montrent les relations entre les tâches dans l'UI d'Airflow.

* Directed : Si on a plusieurs tâches avec des dépendances, chacune à besoin d'au moins une tâche en amont ou aval spécifiée.
* Acyclic : Les tâches ne sont pas autorisées à produire des données qui s'autoréférencent. Cela permet d'éviter la possibilité de produire une boucle infinie.
* Graph : Les tâches sont dans une structure logique avec des processus clairement définis et des relations avec d'autres tâches. 

### DAG run
Lorsqu'un DAG est exécuté, on parle de DAG run. 
Exemple : un DAG est programmée toutes les heures. Chaque instanciation de ce DAG crée un DAG run. Il peut y avoir plusieurs DAG run connectées à un DAG fonctionnant en même temps.

### Operators
Pendant que les DAGs définissent le workflow, les opérateurs définissent le travail. Un opérateur est comme un modèle ou une classe pour exécuter une tâche particulière. 
Tous les opérateurs proviennent de *BaseOperator*. Il existe des opérateurs pour de nombreuses tâches générales : 
* `PythonOperator`
* `MySqlOperator`
* `EmailOperator`
* `BashOperator`

Voir lien : https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/index.html

Il existe __trois types d'operators :__

* Les opérateurs qui exécutent une action ou demandent à un autre système d'exécuter une action.
* Les opérateurs qui déplacent les données d'un système à un autre.
* Les opérateurs qui s'exécutent jusqu'à ce que certaines conditions soient remplies. 

## Demarrer Airflow

Pour démarrer les services d'Airflow, il faut se placer dans le repertoir du docker-compose puis : 

/airflow
```bash
  docker-compose up -d 
```

## Accéder au conteneur PostgreSQL 
```bash
  docker-compose exec postgres psql -U airflow -d airflow
```

