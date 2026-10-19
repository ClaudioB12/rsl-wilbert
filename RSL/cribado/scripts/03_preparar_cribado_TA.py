#!/usr/bin/env python3
"""PASO 3. Crea las hojas de cribado por título y resumen (una por revisor).

Uso (desde la carpeta RSL):
  python cribado/scripts/03_preparar_cribado_TA.py --piloto 50   # 1.º: muestra de calibración
  python cribado/scripts/03_preparar_cribado_TA.py               # 2.º: todos los registros

Salidas en cribado/revision/:
  piloto_R1.xlsx / piloto_R2.xlsx     (con --piloto)
  TA_R1.xlsx / TA_R2.xlsx             (sin --piloto). Si el piloto ya se cerró (paso 4 --cerrar),
                                      sus registros vienen prellenados con la decisión de consenso
                                      para no cribarlos dos veces; esos registros no cuentan para el
                                      kappa de la etapa TA (su acuerdo se reporta como kappa del piloto).
Por seguridad, NO sobrescribe hojas existentes salvo con --forzar.
"""
import argparse
import random
import sys

from comun import REVISION, SALIDA, asegurar_utf8_consola, cargar_json, leer_csv
from hojas import crear_hoja_revisor


def main():
    asegurar_utf8_consola()
    ap = argparse.ArgumentParser()
    ap.add_argument("--piloto", type=int, default=0, help="tamaño de la muestra de calibración (p. ej., 50)")
    ap.add_argument("--semilla", type=int, default=2026)
    ap.add_argument("--forzar", action="store_true", help="sobrescribir hojas existentes (¡se pierde lo llenado!)")
    args = ap.parse_args()

    registros = leer_csv(SALIDA / "02_registros_unicos.csv")
    etapa = "piloto" if args.piloto else "TA"
    previas = {}
    if args.piloto:
        random.seed(args.semilla)
        registros = sorted(random.sample(registros, min(args.piloto, len(registros))), key=lambda r: r["id"])
    else:
        consenso = cargar_json(SALIDA / "consenso_piloto.json", {})
        previas = {i: (v["decision"], v["criterio"], "Decidido en el piloto (consenso)") for i, v in consenso.items()}

    for rev in ("R1", "R2"):
        ruta = REVISION / f"{etapa}_{rev}.xlsx"
        if ruta.exists() and not args.forzar:
            sys.exit(f"Ya existe {ruta}. No se sobrescribe para no perder trabajo (usa --forzar si estás seguro).")
        crear_hoja_revisor(ruta, rev, "TA" if etapa == "TA" else "piloto", registros, previas)
        print(f"Creado {ruta}  ({len(registros)} registros{', ' + str(len(previas)) + ' prellenados del piloto' if previas else ''})")
    print("Entreguen cada archivo a su revisor. Cada uno trabaja por separado y devuelve SU archivo a la carpeta cribado/revision/.")


if __name__ == "__main__":
    main()
