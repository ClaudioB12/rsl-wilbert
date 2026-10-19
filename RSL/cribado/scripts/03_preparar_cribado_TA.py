#!/usr/bin/env python3
"""PASO 3. Crea la hoja de cribado por título y resumen, con la pre-clasificación del asistente.

Uso (desde la carpeta RSL):   python cribado/scripts/03_preparar_cribado_TA.py

Salida: cribado/revision/TA.xlsx
  - SUGERENCIA del asistente por reglas (ver comun.sugerencia_TA):
      «Excluir (regla)»   → la DECISIÓN viene prellenada como Excluir + criterio. Verifícala.
      «Probable incluir»  → menciona anomalía + Deep Learning + tráfico vial.
      «Revisar»           → decides tú leyendo el título y el resumen.
  - Las filas vienen ordenadas: primero «Excluir (regla)», luego «Probable incluir» y al final
    «Revisar» (de mayor a menor puntaje), para que avances rápido.
Por seguridad, NO sobrescribe la hoja si ya existe (usa --forzar si estás seguro).
"""
import argparse
import sys

from comun import REVISION, SALIDA, asegurar_utf8_consola, escribir_csv, leer_csv, sugerencia_TA
from hojas import COL_CRITERIO, COL_DECISION, crear_hoja

COLUMNAS = [("ID", 8, "id"), ("Título", 45, "titulo"), ("Resumen", 80, "resumen"),
            ("Palabras clave", 22, "palabras_clave"), ("Año", 6, "anio"), ("Fuente", 20, "fuente"),
            ("Tipo doc.", 12, "tipo_doc"), ("SUGERENCIA", 14, "sugerencia"),
            ("Motivo de la sugerencia", 32, "motivo"), ("Puntaje", 8, "puntaje")]
ORDEN = {"Excluir (regla)": 0, "Probable incluir": 1, "Revisar": 2}


def main():
    asegurar_utf8_consola()
    ap = argparse.ArgumentParser()
    ap.add_argument("--forzar", action="store_true", help="sobrescribir la hoja existente (¡se pierde lo llenado!)")
    args = ap.parse_args()
    ruta = REVISION / "TA.xlsx"
    if ruta.exists() and not args.forzar:
        sys.exit(f"Ya existe {ruta}. No se sobrescribe para no perder tu trabajo (usa --forzar si estás seguro).")

    registros = leer_csv(SALIDA / "02_registros_unicos.csv")
    prefill = {}
    for r in registros:
        r["sugerencia"], r["criterio_sug"], r["motivo"], r["puntaje"] = sugerencia_TA(r)
        if r["sugerencia"] == "Excluir (regla)":
            prefill[r["id"]] = {COL_DECISION: "Excluir", COL_CRITERIO: r["criterio_sug"],
                                "Comentario": "Regla automática: VERIFICAR"}
    registros.sort(key=lambda r: (ORDEN[r["sugerencia"]], -int(r["puntaje"]), r["id"]))
    crear_hoja(ruta, "TA", registros, COLUMNAS, prefill)
    escribir_csv(SALIDA / "03_sugerencias_TA.csv", registros,
                 ["id", "titulo", "anio", "sugerencia", "criterio_sug", "motivo", "puntaje"])

    from collections import Counter
    c = Counter(r["sugerencia"] for r in registros)
    print(f"Creado {ruta}  ({len(registros)} registros)")
    for k in ORDEN:
        print(f"  {k:<18} {c.get(k, 0):>5}")
    print("Abre TA.xlsx, filtra SUGERENCIA y decide. Lo prellenado («Excluir (regla)») también se verifica.")


if __name__ == "__main__":
    main()
