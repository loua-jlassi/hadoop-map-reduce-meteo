#!/usr/bin/env python3
"""
Reducer pour l'analyse des données climatiques.
Reçoit des paires (clé, valeur) du mapper et calcule la moyenne par clé.
"""
import sys
from collections import defaultdict


def reducer():
    current_key = None
    values = []

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            key, value = line.split('\t', 1)
            value = float(value)
        except (ValueError, IndexError):
            continue

        if key != current_key:
            if current_key is not None and values:
                avg = sum(values) / len(values)
                print(f"{current_key}\t{avg:.2f}")
            current_key = key
            values = [value]
        else:
            values.append(value)

    if current_key is not None and values:
        avg = sum(values) / len(values)
        print(f"{current_key}\t{avg:.2f}")


if __name__ == '__main__':
    reducer()
