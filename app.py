# app.py
from analyzer import analyze_text
from exporter import export_json, export_csv_top_words, export_full_csv
from utils import clear_console, read_text_from_file
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os


def plot_top_words(top_words, title="Top palabras"):
    if not top_words:
        print("No hay palabras para graficar.")
        return
    words, counts = zip(*top_words)
    # crear un dataframe y plot simple
    df = pd.DataFrame({"word": words, "count": counts})
    df.plot.bar(x='word', y='count', legend=False)
    plt.title(title)
    plt.xlabel('')
    plt.tight_layout()
    plt.show()

def main():
    while True:
        clear_console()
        print("=== ANALIZADOR DE TEXTO (CLI) ===")
        print("1) Ingresar texto manual")
        print("2) Analizar archivo (.txt)")
        print("3) Salir")
        choice = input("Elige una opción: ").strip()

        if choice == '3':
            print("¡Adiós!")
            break

        if choice == '2':
            path = input("Ruta del archivo (.txt): ").strip()
            if not os.path.isfile(path):
                print("Archivo no encontrado.")
                input("ENTER para continuar...")
                continue
            text = read_text_from_file(path)
        else:
            print("Pega tu texto. Termina con una línea que contenga solo 'FIN' y presiona ENTER:")
            lines = []
            while True:
                line = sys.stdin.readline()
                if line.strip() == "FIN":
                    break
                lines.append(line)
            text = ''.join(lines)

        result = analyze_text(text, top_n=15, remove_stopwords=True)

        # Mostrar resumen:
        print("\n--- RESULTADO ---")
        print(f"Caracteres: {result['characters']}")
        print(f"Palabras: {result['words']}")
        print(f"Frases: {result['sentences']}")
        print("Sentiment:", result['sentiment']['label'],
              f"(polarity={result['sentiment']['polarity']}, subj={result['sentiment']['subjectivity']})")
        print("\nTop palabras:")
        for w, c in result['top_words']:
            print(f"{w}: {c}")

        # Opciones de exportación / graficar
        print("\nOpciones:")
        print("1) Exportar JSON")
        print("2) Exportar CSV (top palabras)")
        print("3) Exportar CSV (completo)")
        print("4) Graficar top palabras")
        print("5) Volver")
        opt = input("Elige una opción: ").strip()

        if opt == '1':
            fname = input("Nombre del archivo (ej. resultado.json): ").strip()
            export_json(result, fname)
            print("Exportado:", fname)
        elif opt == '2':
            fname = input("Nombre del archivo (ej. top_words.csv): ").strip()
            export_csv_top_words(result['top_words'], fname)
            print("Exportado:", fname)
        elif opt == '3':
            fname = input("Nombre del archivo (ej. full.csv): ").strip()
            export_full_csv(result, fname)
            print("Exportado:", fname)
        elif opt == '4':
            try:
                plot_top_words(result['top_words'], title="Top palabras")
            except Exception as e:
                print("Error al graficar:", e)

        input("\nPresiona ENTER para continuar...")

if __name__ == "__main__":
    main()
