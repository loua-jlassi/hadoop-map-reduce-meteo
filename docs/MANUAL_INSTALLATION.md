# Manuel d’installation – Cluster Hadoop avec Docker

## 1. Prérequis

- **Docker** et **Docker Compose** installés sur la machine
- Au moins 4 Go RAM disponibles pour les conteneurs
- Ports libres : **9870** (Web UI HDFS), **9000** (HDFS)

### Vérification

```bash
docker --version
docker-compose --version
```

## 2. Architecture du cluster

| Composant   | Rôle              | Image Docker                          |
|------------|-------------------|----------------------------------------|
| **NameNode** | Métadonnées HDFS, coordination | bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8 |
| **DataNode 1** | Stockage des blocs HDFS | bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8 |
| **DataNode 2** | Stockage des blocs HDFS | bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8 |

- **Réplication** : 2 (chaque bloc est copié sur 2 DataNodes).
- **Réseau** : tous les nœuds sont sur le réseau interne `hadoop-net`.

## 3. Installation pas à pas

### 3.1 Cloner ou copier le projet

```bash
cd /chemin/vers/bigdata
```

### 3.2 Démarrer le cluster

```bash
docker-compose up -d
```

### 3.3 Vérifier que les conteneurs tournent

```bash
docker-compose ps
```

Vous devez voir `namenode`, `datanode1`, `datanode2` en état **Up**.

### 3.4 Attendre que HDFS soit prêt

Le NameNode peut mettre 30 à 60 secondes à initialiser. Vérifier les logs :

```bash
docker-compose logs -f namenode
```

Quand vous voyez un message du type « NameNode has started », arrêtez avec `Ctrl+C`.

### 3.5 Interface Web HDFS

Ouvrir dans un navigateur : **http://localhost:9870**

- Onglet **Datanodes** : les 2 DataNodes doivent être « Live ».

## 4. Utilisation de HDFS

### 4.1 Exécuter des commandes dans le NameNode

```bash
docker exec -it namenode bash
```

### 4.2 Créer un répertoire et copier les données

Dans le shell du NameNode :

```bash
hdfs dfs -mkdir -p /user/root/input
hdfs dfs -put /data/climate_data.csv /user/root/input/
hdfs dfs -ls /user/root/input
```

Si vos données sont montées dans le conteneur sous `/data`, le fichier `climate_data.csv` doit s’y trouver.

### 4.3 Lancer un job MapReduce (depuis la machine hôte)

Les jobs MapReduce (mapper/reducer Python) peuvent être lancés avec `hadoop streaming` depuis un conteneur qui a accès au client Hadoop, ou en exécutant le job à l’intérieur du NameNode. Exemple depuis le NameNode (après avoir copié mapper/reducer et les données) :

```bash
docker exec -it namenode bash
# Dans le conteneur, après avoir mis mapper.py, reducer.py et les données dans HDFS :
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /user/root/input \
  -output /user/root/output \
  -mapper mapper.py \
  -reducer reducer.py \
  -file mapper.py \
  -file reducer.py
```

(En pratique, il faut que le répertoire de travail du conteneur contienne `mapper.py` et `reducer.py`, ou les avoir uploadés dans HDFS et référencés correctement.)

## 5. Arrêt et suppression

```bash
docker-compose down
```

Pour supprimer aussi les volumes (données HDFS) :

```bash
docker-compose down -v
```

## 6. Dépannage

- **DataNodes non « Live »** : attendre 1–2 minutes et rafraîchir la page 9870 ; vérifier `docker-compose logs datanode1 datanode2`.
- **Erreur de port déjà utilisé** : modifier dans `docker-compose.yml` les ports exposés (ex. `9871:9870`).
- **Manque de mémoire** : augmenter la mémoire allouée à Docker dans les paramètres Docker Desktop.
