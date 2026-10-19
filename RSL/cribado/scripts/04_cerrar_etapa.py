#!/usr/bin/env python3
"""PASO 4. Cierra una etapa del cribado (TA o TC) cuando terminaste de decidir.

Uso (desde la carpeta RSL):
  python cribado/scripts/04_cerrar_etapa.py --etapa TA
  python cribado/scripts/04_cerrar_etapa.py --etapa TC

Hace lo siguiente:
  - Verifica que TODOS los registros tengan decisión, que cada «Excluir» tenga criterio y, en
    texto completo, evidencia. Si falta algo, te dice qué registros y no cierra.
  - Convierte «Duda» en «Incluir» (en título y resumen la duda pasa a texto completo).
  - Calcula el acuerdo entre tu decisión y la sugerencia del asistente (se reporta en el artículo).
  - Guarda el resultado en cribado/salida/decision_<etapa>.json.
"""
import argparse
import sys
from collections import Counter

from comun import REVISION, SALIDA, asegurar_utf8_consola, cargar_json, guardar_json, interpretar_kappa, kappa_cohen
from hojas import leer_hoja


def pasa_humano(d):
    return "No pasa" if d == "Excluir" else "Pasa"


def pasa_asistente(s, etapa):
    """TA: el asistente «excluye» solo con sus reglas. TC: «Revisar» significa que marcó un posible problema."""
    if etapa == "TC":
        return "No pasa" if s.startswith("Revisar") else "Pasa"
    return "No pasa" if s.startswith("Excluir") else "Pasa"


def main():
    asegurar_utf8_consola()
    ap = argparse.ArgumentParser()
    ap.add_argument("--etapa", required=True, choices=["TA", "TC"])
    a = ap.parse_args()
    hoja = leer_hoja(REVISION / f"{a.etapa}.xlsx")
    errores, decision = [], {}
    for i, v in hoja.items():
        d = v["decision"]
        if a.etapa == "TC" and v["texto_completo"] == "No recuperado":
            d = "No recuperado"
        if not d:
            errores.append(f"{i}: falta DECISIÓN")
            continue
        if d == "Excluir" and not v["criterio"]:
            errores.append(f"{i}: «Excluir» sin CRITERIO")
        if a.etapa == "TC" and d == "Excluir" and not v["evidencia"]:
            errores.append(f"{i}: «Excluir» sin EVIDENCIA (cita del artículo)")
        if a.etapa == "TC" and d != "No recuperado" and v["texto_completo"] != "Sí":
            errores.append(f"{i}: indica en «Texto completo» si lo conseguiste (Sí / No recuperado)")
        decision[i] = {"decision": "Incluir" if d == "Duda" else d, "decision_original": d,
                       "criterio": v["criterio"] if d == "Excluir" else "", "evidencia": v["evidencia"],
                       "nota": v["comentario"], "sugerencia": v["sugerencia"],
                       "propuesta_IA": v.get("Propuesta IA", "")}
    if errores:
        print(f"No se puede cerrar la etapa {a.etapa}: {len(errores)} pendientes. Primeros:")
        for e in errores[:20]:
            print("   " + e)
        sys.exit(1)

    guardar_json(SALIDA / f"decision_{a.etapa}.json", decision)
    c = Counter(v["decision_original"] for v in decision.values())
    print(f"Etapa {a.etapa} cerrada: " + ", ".join(f"{k}: {n}" for k, n in sorted(c.items())))
    if a.etapa == "TC":
        crit = Counter(v["criterio"] for v in decision.values() if v["decision"] == "Excluir")
        print("Exclusiones por criterio: " + ", ".join(f"{k}: {n}" for k, n in sorted(crit.items())))

    con_sug = [(pasa_humano(v["decision_original"]), pasa_asistente(v["sugerencia"], a.etapa))
               for v in decision.values() if v["sugerencia"] and v["decision"] != "No recuperado"]
    if con_sug:
        k, n, po = kappa_cohen(con_sug)
        reglas = [v for v in decision.values() if pasa_asistente(v["sugerencia"], a.etapa) == "No pasa"]
        confirmadas = sum(1 for v in reglas if v["decision_original"] == "Excluir")
        info = cargar_json(SALIDA / "fiabilidad.json", {})
        info[f"asistente_{a.etapa}"] = {"kappa": round(k, 2) if k is not None else None, "n": n,
                                        "acuerdo": round(po, 3) if po is not None else None,
                                        "exclusiones_regla": len(reglas), "exclusiones_regla_confirmadas": confirmadas}
        guardar_json(SALIDA / "fiabilidad.json", info)
        detalle = (f"exclusiones por regla confirmadas: {confirmadas} de {len(reglas)}." if a.etapa == "TA" else
                   f"de los {len(reglas)} artículos que el asistente marcó para revisar, excluiste {confirmadas}.")
        print(f"Acuerdo autor-asistente: {po:.1%} (kappa {k:.2f}, {interpretar_kappa(k)}); {detalle}")

    con_ia = [(v["decision_original"], v["propuesta_IA"]) for v in decision.values()
              if v["propuesta_IA"] and v["decision"] != "No recuperado"]
    if con_ia:
        k, n, po = kappa_cohen([(pasa_humano(h), pasa_humano(ia)) for h, ia in con_ia])
        cambios = sum(1 for h, ia in con_ia if h != ia)
        info = cargar_json(SALIDA / "fiabilidad.json", {})
        info[f"IA_{a.etapa}"] = {"kappa": round(k, 2) if k is not None else None, "n": n,
                                 "acuerdo": round(po, 3) if po is not None else None, "decisiones_cambiadas": cambios}
        guardar_json(SALIDA / "fiabilidad.json", info)
        print(f"Acuerdo autor-IA (pasa / no pasa): {po:.1%} (kappa {k:.2f}, {interpretar_kappa(k)}); "
              f"decisiones que cambiaste respecto de la propuesta de la IA: {cambios} de {n}.")


if __name__ == "__main__":
    main()
