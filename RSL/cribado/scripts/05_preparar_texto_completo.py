#!/usr/bin/env python3
"""PASO 5. Crea la hoja de cribado a texto completo con los registros que pasaron el título y resumen.

Requisito: haber cerrado la etapa TA (04_cerrar_etapa.py --etapa TA).
Uso (desde la carpeta RSL):   python cribado/scripts/05_preparar_texto_completo.py
Salidas:  cribado/revision/TC.xlsx
          cribado/salida/05_lista_pdf_a_conseguir.csv  (enlaces DOI para descargar los PDF)
Después de descargar los PDF en cribado/pdf/<ID>.pdf, ejecuta 05b_leer_pdfs.py para que el
asistente lea cada artículo y te proponga la decisión con la evidencia.
"""
import argparse
import sys

from comun import REVISION, SALIDA, asegurar_utf8_consola, cargar_json, escribir_csv, leer_csv
from hojas import crear_hoja

COLUMNAS = [("ID", 8, "id"), ("Título", 45, "titulo"), ("Autores", 22, "autores"), ("Año", 6, "anio"),
            ("Fuente", 22, "fuente"), ("DOI / enlace", 26, "enlace"),
            ("SUGERENCIA", 16, None), ("Motivo de la sugerencia", 30, None),
            ("Evidencia sugerida: métricas de detección", 40, None),
            ("Evidencia sugerida: qué proponen", 40, None),
            ("Evidencia sugerida: Deep Learning", 32, None),
            ("Evidencia sugerida: anomalía / tráfico", 32, None)]


def main():
    asegurar_utf8_consola()
    ap = argparse.ArgumentParser()
    ap.add_argument("--forzar", action="store_true")
    a = ap.parse_args()
    decision = cargar_json(SALIDA / "decision_TA.json")
    if not decision:
        sys.exit("Primero cierra la etapa de título y resumen: 04_cerrar_etapa.py --etapa TA")
    ruta = REVISION / "TC.xlsx"
    if ruta.exists() and not a.forzar:
        sys.exit(f"Ya existe {ruta}. No se sobrescribe (usa --forzar si estás seguro).")
    registros = [r for r in leer_csv(SALIDA / "02_registros_unicos.csv") if decision.get(r["id"], {}).get("decision") == "Incluir"]
    for r in registros:
        r["enlace"] = f"https://doi.org/{r['doi']}" if r["doi"] else (r["url"] or f"https://scholar.google.com/scholar?q={r['titulo']}")
    crear_hoja(ruta, "TC", registros, COLUMNAS)
    escribir_csv(SALIDA / "05_lista_pdf_a_conseguir.csv",
                 [{**r, "guardar_como": f"cribado/pdf/{r['id']}.pdf"} for r in registros],
                 ["id", "titulo", "anio", "fuente", "doi", "enlace", "guardar_como"])
    print(f"Creado {ruta}  ({len(registros)} artículos a leer a texto completo)")
    print("1) Descarga cada PDF y guárdalo como cribado/pdf/<ID>.pdf (lista: salida/05_lista_pdf_a_conseguir.csv)")
    print("2) Ejecuta: python cribado/scripts/05b_leer_pdfs.py")


if __name__ == "__main__":
    main()
