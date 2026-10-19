#!/usr/bin/env python3
"""PASO 4b. Fiabilidad intra-revisor (test-retest), porque el cribado lo hace una sola persona.

Al no haber un segundo revisor, la consistencia se mide re-cribando, al menos 7 días después,
una muestra aleatoria SIN ver las decisiones anteriores. El kappa entre ambas pasadas es el
kappa intra-revisor que se reporta en el artículo.

Uso (desde la carpeta RSL):
  python cribado/scripts/04b_recribado.py --etapa TA --preparar      # crea revision/recribado_TA.xlsx
  python cribado/scripts/04b_recribado.py --etapa TA --calcular      # compara y calcula el kappa
(igual con --etapa TC)

Tamaño de la muestra: 10 % de los registros, con un mínimo de 30 (o todos si hay menos) y un
máximo de 100.
"""
import argparse
import json
import random
import sys

from comun import REVISION, SALIDA, asegurar_utf8_consola, cargar_json, guardar_json, interpretar_kappa, kappa_cohen, leer_csv
from hojas import crear_hoja, leer_hoja

COLS_TA = [("ID", 8, "id"), ("Título", 45, "titulo"), ("Resumen", 80, "resumen"),
           ("Palabras clave", 22, "palabras_clave"), ("Año", 6, "anio"), ("Fuente", 20, "fuente"),
           ("Tipo doc.", 12, "tipo_doc")]
COLS_TC = [("ID", 8, "id"), ("Título", 45, "titulo"), ("Año", 6, "anio"), ("DOI", 26, "doi")]


def main():
    asegurar_utf8_consola()
    ap = argparse.ArgumentParser()
    ap.add_argument("--etapa", required=True, choices=["TA", "TC"])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--preparar", action="store_true")
    g.add_argument("--calcular", action="store_true")
    ap.add_argument("--semilla", type=int, default=2026)
    ap.add_argument("--forzar", action="store_true")
    a = ap.parse_args()
    decision = cargar_json(SALIDA / f"decision_{a.etapa}.json")
    if not decision:
        sys.exit(f"Primero cierra la etapa: 04_cerrar_etapa.py --etapa {a.etapa}")
    ruta = REVISION / f"recribado_{a.etapa}.xlsx"

    if a.preparar:
        if ruta.exists() and not a.forzar:
            sys.exit(f"Ya existe {ruta} (usa --forzar si estás seguro).")
        ids = sorted(i for i, v in decision.items() if v["decision"] != "No recuperado")
        n = len(ids) if len(ids) <= 30 else min(100, max(30, round(len(ids) * 0.10)))
        random.seed(a.semilla)
        muestra = set(random.sample(ids, n))
        registros = [r for r in leer_csv(SALIDA / "02_registros_unicos.csv") if r["id"] in muestra]
        random.shuffle(registros)                       # otro orden, para no recordar la secuencia
        crear_hoja(ruta, "TC" if a.etapa == "TC" else "TA", registros, COLS_TC if a.etapa == "TC" else COLS_TA)
        print(f"Creado {ruta} con {n} registros. Hazlo dentro de 7 días o más, SIN mirar TA.xlsx/TC.xlsx.")
        return

    nuevo = leer_hoja(ruta)
    faltan = [i for i, v in nuevo.items() if not v["decision"]]
    if faltan:
        sys.exit(f"Faltan decisiones en {len(faltan)} registros del re-cribado (p. ej., {', '.join(faltan[:5])}).")
    paso = lambda d: "No pasa" if d == "Excluir" else "Pasa"
    pares = [(paso(decision[i]["decision_original"]), paso(v["decision"])) for i, v in nuevo.items() if i in decision]
    k, n, po = kappa_cohen(pares)
    distintos = [i for i, v in nuevo.items() if i in decision and paso(decision[i]["decision_original"]) != paso(v["decision"])]
    info = cargar_json(SALIDA / "fiabilidad.json", {})
    info[f"recribado_{a.etapa}"] = {"kappa": round(k, 2), "n": n, "acuerdo": round(po, 3), "discrepancias": distintos}
    guardar_json(SALIDA / "fiabilidad.json", info)
    print(f"Kappa intra-revisor ({a.etapa}): {k:.2f} ({interpretar_kappa(k)}), n = {n}, acuerdo = {po:.1%}")
    if distintos:
        print("Registros con decisión distinta (revísalos; si la primera decisión estaba mal, corrígela en "
              f"{a.etapa}.xlsx y vuelve a cerrar la etapa): " + ", ".join(distintos))


if __name__ == "__main__":
    main()
