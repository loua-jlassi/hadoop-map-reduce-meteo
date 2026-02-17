# Partie II – Analyse des données et streaming

## Partie A – MapReduce (données climatiques)

### i. Description du dataset

- **Source** : jeu de données climatiques (type Kaggle / open data). Exemple fourni : `data/climate_data.csv`.
- **Colonnes** : `Date` (YYYY-MM-DD), `City`, `Temperature` (°C), `Humidity` (%), `Pressure` (hPa).
- **Objectif** : analyse descriptive par ville et par mois (température, humidité, pression).

### ii. Objectifs d’analyse

- Température moyenne par ville et par mois.
- Humidité moyenne par ville et par mois.
- Pression moyenne par ville et par mois.

(Équivalent à des agrégations par continent/pays/année si le dataset est étendu avec ces champs.)

### iii. Procédures Map et Reduce

- **Mapper** (`mapreduce/mapper.py`) : lit chaque ligne CSV, extrait (ville, année-mois), émet pour chaque enregistrement trois paires :
  - `(ville_année-mois, température)`
  - `(ville_année-mois_humidity, humidité)`
  - `(ville_année-mois_pressure, pression)`
- **Reducer** (`mapreduce/reducer.py`) : pour chaque clé, regroupe toutes les valeurs et calcule la **moyenne**, puis écrit `clé\tmoyenne`.

---

## Partie B – Twitter Streaming (Spark / PySpark)

### i. Datasource : Twitter Streaming API

- **API** : [Twitter API v2](https://developer.twitter.com/en/docs/twitter-api) (ou API v1.1 streams). Accès aux tweets en temps réel via un stream.
- **Accès** : création d’un projet et d’une app sur [Twitter Developer Portal](https://developer.twitter.com/), récupération des clés :
  - `API Key`, `API Secret`, `Bearer Token`
  - `Access Token`, `Access Token Secret` (pour l’authentification utilisateur / streaming).
- **Colonnes / champs utiles du dataset** : `id`, `text`, `created_at`, `author_id`, `lang`, `public_metrics` (retweet_count, like_count, reply_count), `entities` (hashtags, mentions).

### ii. Fonctions d’analyse (streaming + ML)

- **Streaming** : réception du flux Twitter avec PySpark Streaming (ou Kafka + Spark Streaming), parsing des tweets (texte, date, langue, hashtags).
- **Analyse prédictive / ML** : exemples possibles :
  - Classification de sentiment (positif / négatif / neutre) avec un modèle entraîné (ex. pipeline scikit-learn ou modèle chargé).
  - Détection de langue, comptage de hashtags par fenêtre temporelle.
- Le code correspondant est dans `spark_streaming/` (voir README dans ce dossier).

### iii. Visualisation graphique des résultats

- Graphiques générés à partir des résultats du streaming et/ou du ML (ex. matplotlib, sauvegardés en PNG).
- Exemples : évolution du nombre de tweets par fenêtre, distribution des sentiments, top hashtags.
- Scripts de visualisation dans `spark_streaming/visualization.py` (ou équivalent).
