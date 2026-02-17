# Explication du projet – En termes simples

## De quoi il s’agit exactement ?

Le projet porte sur **l’analyse de grandes quantités de données** avec des outils utilisés en entreprise pour le **Big Data** :

1. **Hadoop** : pour stocker et traiter des données réparties sur plusieurs machines (un « cluster »).
2. **MapReduce** : une façon de calculer des statistiques (moyennes, totaux, etc.) en découpant le travail sur ces machines.
3. **Spark / Twitter** : pour traiter des données **en continu** (streaming), par exemple des tweets, et faire un peu de **machine learning** (ex. sentiment) et des **graphiques**.

En résumé : **on simule un petit « cluster Big Data » avec Docker, on analyse des données météo avec MapReduce, et on montre du traitement en temps réel sur des tweets avec Spark.**

---

## Les outils utilisés et leur rôle

### 1. Docker

- **C’est quoi ?** Un outil qui crée des **conteneurs** : des mini-machines virtuelles légères qui tournent sur ton Mac.
- **Rôle dans le projet :** Au lieu d’installer Hadoop directement sur ton ordinateur (compliqué), on lance **3 conteneurs** :
  - 1 **NameNode** (le « chef » qui sait où sont les données)
  - 2 **DataNodes** (les « ouvriers » qui stockent vraiment les données)
- **Importance :** Ça permet d’avoir un **vrai petit cluster Hadoop** (1 chef + 2 nœuds) comme en entreprise, sans acheter plusieurs ordinateurs.

### 2. Hadoop (HDFS)

- **C’est quoi ?** Un système de **fichiers distribué** : les fichiers sont coupés en blocs et répartis sur plusieurs machines (les DataNodes). Le NameNode garde la « carte » (où est chaque bloc).
- **Rôle dans le projet :** On utilise HDFS comme **stockage** pour les données du cluster. Les données météo (ou autres) pourraient être mises dans HDFS pour être lues par des jobs MapReduce.
- **Importance :** C’est la base du Big Data « classique » : stocker beaucoup de données sur plusieurs machines et les traiter en parallèle.

### 3. MapReduce (mapper + reducer en Python)

- **C’est quoi ?** Un **modèle de calcul** en deux étapes :
  - **Map** : chaque ligne de données est lue et transformée en paires (clé, valeur). Ex. (Paris_2026-01, 5.2), (Paris_2026-01, 6.1)…
  - **Reduce** : pour une même clé, on regroupe toutes les valeurs et on calcule un résultat (moyenne, somme, etc.). Ex. Paris_2026-01 → 5.65.
- **Rôle dans le projet :**
  - **mapper.py** : lit le CSV météo (date, ville, température, humidité, pression) et émet des paires (ville_mois, valeur).
  - **reducer.py** : pour chaque clé (ex. Paris_2026-01), calcule la **moyenne** des valeurs.
- **Importance :** C’est l’analyse **descriptive** demandée : moyennes par ville et par mois. En vrai cluster, Hadoop répartit le Map et le Reduce sur les DataNodes pour traiter des gros volumes.

### 4. Dataset (climate_data.csv)

- **C’est quoi ?** Un fichier CSV avec des **données climatiques** : date, ville (Paris, London, Berlin), température, humidité, pression.
- **Rôle :** C’est la **source de données** sur laquelle on applique MapReduce. On pourrait le remplacer par un gros dataset Kaggle (même format ou proche).
- **Importance :** Sans données, pas d’analyse. Ce fichier représente le type de données « météo / climat » demandé dans le sujet.

### 5. Spark / PySpark (Streaming)

- **C’est quoi ?** Un moteur de calcul qui traite des données **par flux** (streaming) : au lieu de lire un fichier une fois, on lit des données qui arrivent en continu (ex. tweets).
- **Rôle dans le projet :**
  - **twitter_stream.py** : récupère des tweets (via l’API Twitter ou des tweets simulés) et les écrit dans des fichiers JSON.
  - **streaming_analysis.py** : PySpark lit ces fichiers au fur et à mesure et calcule des stats (ex. nombre de tweets par langue).
- **Importance :** C’est la partie **traitement en temps réel** du sujet : on montre qu’on sait traiter un flux de données (Twitter) avec Spark.

### 6. Twitter API

- **C’est quoi ?** L’interface fournie par Twitter pour récupérer des tweets (recherche, stream, etc.) de façon officielle.
- **Rôle :** Donner une **vraie source de données en continu**. Sans clé API, on utilise des tweets **simulés** pour faire tourner le code.
- **Importance :** Montre qu’on sait se connecter à une source de streaming réelle (comme demandé dans le sujet).

### 7. Machine Learning (ml_sentiment.py)

- **C’est quoi ?** Un petit modèle qui prédit le **sentiment** (positif / négatif) d’un texte à partir de mots (TF-IDF + régression logistique).
- **Rôle :** On l’applique aux tweets collectés pour illustrer une **analyse prédictive** avec du ML.
- **Importance :** Répond à la demande « analyse prédictive avec un algorithme de ML » sur les données Twitter.

### 8. Visualisation (visualization.py)

- **C’est quoi ?** Des **graphiques** (camembert, barres) générés avec matplotlib à partir des résultats (tweets par langue, répartition du sentiment).
- **Rôle :** Produire des images (PNG) pour le rapport ou la présentation.
- **Importance :** Répond à la demande « visualisation graphique des résultats ».

---

## Résumé des étapes du projet

| Étape | Outil / Fichier | Ce qu’on fait | Importance |
|-------|------------------|----------------|------------|
| 1 | Docker | On lance 1 NameNode + 2 DataNodes | Avoir un cluster Hadoop sans vrais serveurs |
| 2 | HDFS (interface 9870) | On voit que le cluster tourne, on peut y mettre des fichiers | Montrer le stockage distribué |
| 3 | mapper.py + reducer.py | On lit le CSV météo et on calcule des moyennes par ville/mois | Analyse descriptive MapReduce |
| 4 | climate_data.csv | Données d’entrée pour MapReduce | Source de données du projet |
| 5 | twitter_stream.py | On récupère (ou simule) des tweets et on les écrit en JSON | Source de données streaming (Twitter) |
| 6 | streaming_analysis.py | Spark lit le flux et compte par langue | Traitement temps réel avec Spark |
| 7 | ml_sentiment.py | On prédit le sentiment des tweets | Analyse prédictive avec du ML |
| 8 | visualization.py | On génère des graphiques | Visualisation des résultats |

---

## En une phrase

**On a mis en place un mini-cluster Hadoop avec Docker, on a analysé des données météo avec MapReduce (moyennes par ville et par mois), et on a montré du traitement en temps réel sur des tweets avec Spark, du ML (sentiment) et des graphiques.**

Si tu veux, on peut détailler une partie précise (par exemple uniquement MapReduce, ou uniquement Spark/Twitter).
