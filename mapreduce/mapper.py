#!/usr/bin/env python3
"""
Mapper pour l'analyse des données climatiques.
Lit des lignes CSV (Date, City, Temperature, Humidity, Pressure) et émet
(clé, valeur) pour température, humidité et pression par ville et mois.
"""
import sys
from datetime import datetime


def mapper():
    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith('#') or line.lower().startswith('date'):
            continue
        try:
            fields = line.split(',')
            if len(fields) < 5:
                continue
            date_str = fields[0].strip()
            location = fields[1].strip()
            temperature = float(fields[2].strip())
            humidity = float(fields[3].strip())
            pressure = float(fields[4].strip())

            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                month_key = f"{date_obj.year}-{date_obj.month:02d}"
            except ValueError:
                continue

            location_month_key = f"{location}_{month_key}"
            print(f"{location_month_key}\t{temperature}")
            print(f"{location_month_key}_humidity\t{humidity}")
            print(f"{location_month_key}_pressure\t{pressure}")
        except (ValueError, IndexError):
            continue


if __name__ == '__main__':
    mapper()
