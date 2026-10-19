#!/usr/bin/env python3
"""PASO 7. Verificación de la evaluación de calidad (QA1-QA8) de los estudios incluidos.

Cada estudio ya tiene un puntaje PROPUESTO por ítem, con la evidencia tomada del PDF (en
suplementos/extraccion_individual/*.json). Tú lo verificas leyendo el artículo: confirmas o
cambias cada puntaje. El acuerdo entre tu puntaje y el propuesto se reporta en el artículo.

Uso (desde la carpeta RSL):
  A) python cribado/scripts/07_calidad.py --preparar   → crea cribado/revision/calidad.xlsx
  B) llenas la columna «TU PUNTAJE» (y la justificación cuando cambias el propuesto)
  C) python cribado/scripts/07_calidad.py --aplicar    → calcula el acuerdo y guarda tus puntajes
     Luego:  python suplementos/generar_conteos.py
"""
import argparse
import json
import sys

from openpyxl import Workbook, load_workbook

from comun import REVISION, SALIDA, SUPLEMENTOS, asegurar_utf8_consola, cargar_json, guardar_json, interpretar_kappa, kappa_cohen
from hojas import AJUSTE, AMARILLO, AZUL, BLANCO_NEGRITA, VERDE_OSC, _lista

ITEMS = {
    "QA1": ("Procedencia de etiquetas", "1: registros reales o anotación verificada; 0.5: mixtas, automáticas o verificación parcial; 0: solo inyectadas o no reportado"),
    "QA2": ("Partición sin fuga", "1: partición temporal o prueba independiente descrita; 0.5: partición aleatoria o descripción incompleta; 0: no reportada"),
    "QA3": ("Líneas base comparables", "1: dos o más líneas base con el mismo protocolo, incluida una del estado del arte o no DL; 0.5: una sola o solo ablación; 0: ninguna"),
    "QA4": ("Variabilidad", "1: varias ejecuciones con dispersión, intervalos o pruebas de significancia; 0.5: parcial; 0: una sola ejecución"),
    "QA5": ("Código y datos", "1: ambos públicos; 0.5: uno de los dos; 0: ninguno"),
    "QA6": ("Más de un escenario", "1: dos o más datasets, ciudades o vías independientes; 0.5: varios subconjuntos de un dataset; 0: un único escenario"),
    "QA7": ("Protocolo explícito", "1: reporta unidad de evaluación y criterio de umbral o decisión; 0.5: solo uno; 0: ninguno"),
    "QA8": ("Limitaciones", "1: sección o párrafo explícito; 0.5: mención breve; 0: ninguna"),
}
CAB = ["ID", "Estudio", "Ítem", "Criterio y escala", "Puntaje propuesto", "Evidencia del puntaje propuesto",
       "TU PUNTAJE", "Justificación (obligatoria si cambias el propuesto)"]


def fmt(p):
    return {1.0: "1", 0.5: "0.5", 0.0: "0"}[float(p)]


def cargar():
    cur = json.loads((SUPLEMENTOS / "curacion.json").read_text(encoding="utf-8"))
    out = []
    for c in cur["incluidos"]:
        ruta = SUPLEMENTOS / "extraccion_individual" / f"{c['clave_extraccion']}.json"
        out.append((c["id"], ruta, json.loads(ruta.read_text(encoding="utf-8"))))
    return out


def preparar(forzar):
    ruta = REVISION / "calidad.xlsx"
    if ruta.exists() and not forzar:
        sys.exit(f"Ya existe {ruta} (usa --forzar si estás seguro).")
    wb = Workbook()
    ws = wb.active
    ws.title = "Calidad"
    ws.append(CAB)
    anchos = [7, 34, 7, 40, 10, 60, 10, 40]
    for c, w in zip(ws[1], anchos):
        c.fill = VERDE_OSC if c.value.startswith(("TU", "Justif")) else AZUL
        c.font, c.alignment = BLANCO_NEGRITA, AJUSTE
        ws.column_dimensions[c.column_letter].width = w
    for sid, _, e in cargar():
        for q, (nombre, escala) in ITEMS.items():
            ws.append([sid, f"{e['primer_autor']} et al. ({e['anio']}). {e['titulo']}", q, f"{nombre}. {escala}",
                       fmt(e["calidad"][q]["p"]), e["calidad"][q]["ev"], None, None])
            for c in ws[ws.max_row]:
                c.alignment = AJUSTE
            ws.cell(row=ws.max_row, column=7).fill = AMARILLO
    _lista(ws, f"G2:G{ws.max_row}", ["1", "0.5", "0"])
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:H{ws.max_row}"
    wb.save(ruta)
    print(f"Creado {ruta}: {ws.max_row - 1} filas (21 estudios × 8 ítems). Llena «TU PUNTAJE» leyendo cada PDF.")


def aplicar():
    ws = load_workbook(REVISION / "calidad.xlsx", data_only=True)["Calidad"]
    tuyo, faltan, sin_just = {}, [], []
    for f in ws.iter_rows(min_row=2, values_only=True):
        if not f[0]:
            continue
        if f[6] in (None, ""):
            faltan.append(f"{f[0]}-{f[2]}")
            continue
        try:
            v, prop = fmt(float(str(f[6]).replace(",", "."))), fmt(float(str(f[4]).replace(",", ".")))
        except (ValueError, KeyError):
            faltan.append(f"{f[0]}-{f[2]} (valor no válido: {f[6]})")
            continue
        if v != prop and not (f[7] or "").strip():
            sin_just.append(f"{f[0]}-{f[2]}")
        tuyo[(f[0], f[2])] = (v, prop, f[7] or "")
    if faltan or sin_just:
        if faltan:
            print(f"Faltan puntajes ({len(faltan)}): {', '.join(faltan[:15])}")
        if sin_just:
            print(f"Cambiaste el propuesto sin justificar ({len(sin_just)}): {', '.join(sin_just[:15])}")
        sys.exit(1)
    k, n, po = kappa_cohen([(a, b) for a, b, _ in tuyo.values()])
    cambios = 0
    for sid, ruta, e in cargar():
        for q in ITEMS:
            v, prop, just = tuyo[(sid, q)]
            if v != prop:
                e["calidad"][q]["ev"] += f" [Verificado por el autor: {v} (propuesto {prop}). {just}]"
                e["calidad"][q]["p"] = float(v)
                cambios += 1
        ruta.write_text(json.dumps(e, ensure_ascii=False, indent=1), encoding="utf-8")
    info = cargar_json(SALIDA / "fiabilidad.json", {})
    info["calidad"] = {"kappa": round(k, 2), "n": n, "acuerdo": round(po, 3), "cambios": cambios}
    guardar_json(SALIDA / "fiabilidad.json", info)
    print(f"Acuerdo con el puntaje propuesto: {po:.1%} (kappa {k:.2f}, {interpretar_kappa(k)}); {cambios} puntajes cambiados.")
    print("Ahora ejecuta:  python suplementos/generar_conteos.py   y luego   python cribado/scripts/06_resultados_prisma.py")


def main():
    asegurar_utf8_consola()
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--preparar", action="store_true")
    g.add_argument("--aplicar", action="store_true")
    ap.add_argument("--forzar", action="store_true")
    a = ap.parse_args()
    preparar(a.forzar) if a.preparar else aplicar()


if __name__ == "__main__":
    main()
