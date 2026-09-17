# exporter.py
import json
import csv
from typing import Dict, Any, List

def export_json(result: Dict[str, Any], filename: str):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def export_csv_top_words(top_words: List[tuple], filename: str):
    """Guarda top words como CSV (palabra, frecuencia)."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['word', 'count'])
        for word, count in top_words:
            writer.writerow([word, count])

def export_full_csv(result: Dict[str, Any], filename: str):
    """Guarda un CSV simple con métricas básicas y top words en columnas separadas."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Encabezados
        writer.writerow(['metric', 'value'])
        writer.writerow(['characters', result.get('characters')])
        writer.writerow(['words', result.get('words')])
        writer.writerow(['sentences', result.get('sentences')])
        sentiment = result.get('sentiment', {})
        writer.writerow(['sentiment_polarity', sentiment.get('polarity')])
        writer.writerow(['sentiment_subjectivity', sentiment.get('subjectivity')])
        writer.writerow(['sentiment_label', sentiment.get('label')])
        writer.writerow([])
        writer.writerow(['top_word', 'count'])
        for w, c in result.get('top_words', []):
            writer.writerow([w, c])
