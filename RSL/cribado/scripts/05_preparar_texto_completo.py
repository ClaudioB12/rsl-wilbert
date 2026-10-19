#!/usr/bin/env python3
"""PASO 5. Crea las hojas de cribado a texto completo con los registros que pasaron el título y resumen.

Requisito: haber cerrado la etapa TA (04_consolidar.py --etapa TA --cerrar).
Uso (desde la carpeta RSL):   python cribado/scripts/05_preparar_texto_completo.py
Salidas:  cribado/revision/TC_R1.xlsx y TC_R2.xlsx
          cribado/salida/05_lista_pdf_a_conseguir.csv   (para repartir la descarga de PDF)
"""
import argparse
import sys

from comun import REVISION, SALIDA, asegurar_utf8_consola, cargar_json, escribir_csv, leer_csv
from hojas import crear_hoja_revisor


def main():
    asegurar_utf8_consola()
    ap = argparse.ArgumentParser()
    ap.add_argument("--forzar", action="store_true")
    args = ap.parse_args()
    consenso = cargar_json(SALIDA / "consenso_TA.json")
    if not consenso:
        sys.exit("Primero cierra la etapa de título y resumen: 04_consolidar.py --etapa TA --cerrar")
    registros = [r for r in leer_csv(SALIDA / "02_registros_unicos.csv")
                 if consenso.get(r["id"], {}).get("decision") == "Incluir"]
    for rev in ("R1", "R2"):
        ruta = REVISION / f"TC_{rev}.xlsx"
        if ruta.exists() and not args.forzar:
            sys.exit(f"Ya existe {ruta}. No se sobrescribe (usa --forzar si estás seguro).")
        crear_hoja_revisor(ruta, rev, "TC", registros)
        print(f"Creado {ruta}  ({len(registros)} registros)")
    escribir_csv(SALIDA / "05_lista_pdf_a_conseguir.csv",
                 [{**r, "enlace": f"https://doi.org/{r['doi']}" if r["doi"] else r["url"], "responsable": "", "conseguido": ""}
                  for r in registros],
                 ["id", "titulo", "anio", "fuente", "doi", "enlace", "responsable", "conseguido"])
    print("Guarden los PDF como cribado/pdf/<ID>.pdf (p. ej., R0123.pdf). Esa carpeta NO se sube a GitHub.")


if __name__ == "__main__":
    main()
