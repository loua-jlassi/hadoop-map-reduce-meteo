#!/bin/bash
# Test du job MapReduce en local (sans Hadoop) avec mapper.py et reducer.py
# Usage: ./run_mapreduce_local.sh
# Ou: cat data/climate_data.csv | python mapreduce/mapper.py | sort | python mapreduce/reducer.py

set -e
cd "$(dirname "$0")"
DATA="${1:-data/climate_data.csv}"
if [[ ! -f "$DATA" ]]; then
  echo "Fichier non trouvé: $DATA"
  exit 1
fi
echo "Entrée: $DATA"
echo "--- Résultat MapReduce (température/humidité/pression moyennes par ville-mois) ---"
cat "$DATA" | python3 mapreduce/mapper.py | sort -k1,1 | python3 mapreduce/reducer.py
