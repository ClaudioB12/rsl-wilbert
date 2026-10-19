#!/usr/bin/env python3
"""PASO 1. Une todas las exportaciones de las bases en una sola tabla y verifica los conteos.

Antes de ejecutarlo:
  - Guardar los archivos exportados en cribado/exportaciones/<Base>/ (Scopus, WoS, IEEE,
    ScienceDirect, ACM). Formatos aceptados: .ris, .bib, .csv (Scopus/IEEE) y .txt
    (Web of Science «Tab delimited» o RIS).
  - Completar cribado/exportaciones/fechas_busqueda.csv con la fecha y el número de
    resultados que mostró cada base en pantalla.

Uso (desde la carpeta RSL):   python cribado/scripts/01_unificar_exportaciones.py
Salida:  cribado/salida/01_registros_todos.csv  y un resumen por base en pantalla.
"""
import sys
from collections import Counter

from comun import (BASES, EXPORTACIONES, NOMBRE_BASE, SALIDA, asegurar_utf8_consola, escribir_csv,
                   leer_csv, leer_exportacion)

CAMPOS = ["base", "archivo", "titulo", "autores", "anio", "fuente", "doi", "resumen",
          "palabras_clave", "tipo_doc", "idioma", "url"]


def main():
    asegurar_utf8_consola()
    todos = []
    for base in BASES:
        carpeta = EXPORTACIONES / base
        archivos = sorted(p for p in carpeta.glob("*") if p.is_file() and not p.name.startswith(("LEEME", ".")))
        for a in archivos:
            regs = leer_exportacion(a, base)
            print(f"  {base:<14} {a.name:<45} {len(regs):>5} registros")
            todos.extend(regs)
    if not todos:
        sys.exit("No se encontraron exportaciones en cribado/exportaciones/<Base>/. Revisa la guía (Parte 2).")

    sin_titulo = [r for r in todos if not r["titulo"]]
    todos = [r for r in todos if r["titulo"]]
    conteo = Counter(r["base"] for r in todos)

    fechas = {f["base"]: f for f in leer_csv(EXPORTACIONES / "fechas_busqueda.csv")} if (EXPORTACIONES / "fechas_busqueda.csv").exists() else {}
    print("\nResumen por base (registros leídos vs. resultados en pantalla):")
    problemas = 0
    for base in BASES:
        f = fechas.get(base, {})
        pantalla = (f.get("resultados_en_pantalla") or "").strip()
        aviso = ""
        if pantalla and pantalla.isdigit() and int(pantalla) != conteo.get(base, 0):
            aviso = "  <-- NO COINCIDE: falta exportar algún lote o hay registros sin título"
            problemas += 1
        if not f.get("fecha"):
            aviso += "  <-- falta la fecha en fechas_busqueda.csv"
        print(f"  {NOMBRE_BASE[base]:<22} leídos={conteo.get(base, 0):>5}  pantalla={pantalla or '?':>5}{aviso}")
    print(f"  {'TOTAL':<22} leídos={len(todos):>5}")
    if sin_titulo:
        print(f"\nAviso: se descartaron {len(sin_titulo)} registros sin título (revisar el archivo de origen).")
    sin_resumen = sum(1 for r in todos if not r["resumen"])
    if sin_resumen:
        print(f"Aviso: {sin_resumen} registros sin resumen. Para el cribado conviene exportar «con resumen» (abstract).")

    escribir_csv(SALIDA / "01_registros_todos.csv", todos, CAMPOS)
    print(f"\nListo: {SALIDA / '01_registros_todos.csv'}")
    if problemas:
        print("Corrige las diferencias de conteo antes de seguir (PRISMA exige el número exacto por base).")


if __name__ == "__main__":
    main()
