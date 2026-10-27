#!/usr/bin/env python3
"""PASO 16. Evaluación de calidad (QA1-QA8) de los estudios incluidos: resumen y carga en Parsif.al.

Toma los puntajes de la hoja «3_Calidad» de REVISION_TEXTO_COMPLETO.xlsx, ya pasados por
15_aplicar_texto_completo.py (cribado/salida/15_extraccion_TC.json), y:
  1. muestra el resumen (media, rango y cumplimiento por ítem) y lo guarda en
     cribado/salida/16_calidad_resumen.csv (una fila por estudio, con el total);
  2. genera cribado/salida/parsifal/cargar_calidad_en_parsifal.js, que se pega en la consola del
     navegador (F12) en Parsif.al > Conducting > Quality Assessment y marca la respuesta de cada
     pregunta de cada estudio aceptado (Sí = 1, Parcial = 0.5, No = 0).

Requisitos en Parsif.al (Planning > Quality Assessment Checklist, ver PARSIFAL_COPIAR_PEGAR.md 2.8):
  - las respuestas «Sí», «Parcial» y «No»;
  - las preguntas QA1 … QA8, cada una empezando por su código («QA1. …»).

Uso (desde la carpeta RSL):   python cribado/scripts/16_calidad_parsifal.py
"""
import importlib.util
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

from comun import SALIDA, asegurar_utf8_consola, cargar_json, escribir_csv

ITEMS = [f"QA{i}" for i in range(1, 9)]
RESPUESTA = {1.0: "si", 0.5: "parcial", 0.0: "no"}  # como norm() del JS

PLANTILLA = r"""// Script generado por cribado/scripts/16_calidad_parsifal.py. No editar a mano.
// Pegar en la consola del navegador (F12 > Console) estando en tu revisión de parsif.al
// (Conducting > Quality Assessment).
(async () => {
  const DATOS = __DATOS__;
  const rid = (document.querySelector("#review-id") || {}).value;
  if (!rid) { alert("Abre primero tu revisión en Parsif.al (Conducting > Quality Assessment) y vuelve a pegar el script."); return; }
  const r0 = await fetch(`/reviews/conducting/quality_assessment_detailed/?review-id=${rid}`, { credentials: "same-origin" });
  if (!r0.ok) { alert("No se pudo leer la página de Quality Assessment (HTTP " + r0.status + ")."); return; }
  const doc = new DOMParser().parseFromString(await r0.text(), "text/html");
  const norm = (t) => (t || "").normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]/g, "");
  const tablas = [...doc.querySelectorAll("table[article-id]")];
  if (!tablas.length) { alert("No hay estudios en Quality Assessment. ¿Están creadas las preguntas y respuestas del checklist y hay estudios Accepted?"); return; }

  // Preguntas (QA1…QA8) y respuestas (Sí/Parcial/No) según la primera tabla.
  const pregunta = {}, respuesta = {};
  tablas[0].querySelectorAll("tr[question-id]").forEach((tr) => {
    const m = tr.children[0].textContent.trim().match(/^QA\s*(\d)/i);
    if (m) pregunta["QA" + m[1]] = tr.getAttribute("question-id");
    tr.querySelectorAll("td[answer-id]").forEach((td) => { respuesta[norm(td.textContent)] = td.getAttribute("answer-id"); });
  });
  const faltanQ = Object.keys(DATOS[Object.keys(DATOS)[0]][1]).filter((q) => !pregunta[q]);
  const faltanR = ["si", "parcial", "no"].filter((r) => !respuesta[r]);
  if (faltanQ.length || faltanR.length) {
    alert("Falta en el checklist de Parsif.al: " + [...faltanQ, ...faltanR.map((r) => "respuesta " + r)].join(", ") +
          ". Revisa Planning > Quality Assessment Checklist (cada pregunta debe empezar por QA1., QA2., …).");
    return;
  }

  // Estudios: por título (como en Study Selection).
  const porTitulo = {};
  tablas.forEach((t) => {
    const h = t.closest(".panel").querySelector(".panel-title");
    const titulo = h.childNodes[0].textContent;
    porTitulo[norm(titulo)] = { aid: t.getAttribute("article-id"), csrf: t.getAttribute("csrf-token") };
  });
  const claves = Object.keys(DATOS).filter((k) => porTitulo[DATOS[k][0]]);
  const faltan = Object.keys(DATOS).filter((k) => !porTitulo[DATOS[k][0]]);
  console.log(`Estudios en Quality Assessment: ${tablas.length}. Coinciden: ${claves.length}. Sin coincidencia: ${faltan.length}.`);
  if (!confirm(`Se van a marcar ${claves.length * 8} respuestas (${claves.length} estudios × 8 preguntas). ¿Continuar?`)) return;

  const cola = [];
  claves.forEach((k) => Object.entries(DATOS[k][1]).forEach(([q, r]) => cola.push([k, q, r])));
  let ok = 0, err = [];
  const trabajador = async () => {
    while (cola.length) {
      const [k, q, r] = cola.shift();
      const { aid, csrf } = porTitulo[DATOS[k][0]];
      const datos = new URLSearchParams({ "review-id": rid, "article-id": aid, "question-id": pregunta[q],
                                          "answer-id": respuesta[r], "csrfmiddlewaretoken": csrf });
      try {
        const resp = await fetch("/reviews/conducting/save_quality_assessment/", {
          method: "POST", credentials: "same-origin", body: datos,
          headers: { "X-CSRFToken": csrf, "X-Requested-With": "XMLHttpRequest" },
        });
        if (!resp.ok) throw new Error("HTTP " + resp.status);
        ok++;
      } catch (e) { err.push(`${k} ${q} (${e.message})`); }
      if ((ok + err.length) % 100 === 0) console.log(`… ${ok + err.length} respuestas`);
    }
  };
  await Promise.all([1, 2, 3, 4].map(trabajador));
  console.log(`LISTO: ${ok} respuestas guardadas, ${err.length} con error.`);
  if (err.length) console.warn("Con error (vuelve a pegar el script para reintentar): " + err.join(", "));
  if (faltan.length) console.warn("Estudios que no están en Quality Assessment (¿no están Accepted?): " + faltan.join(", "));
  alert(`Listo: ${ok} respuestas guardadas${err.length ? ", " + err.length + " con error (ver consola)" : ""}. Recarga la página para verlas.`);
})();
"""


def main():
    asegurar_utf8_consola()
    estudios = cargar_json(SALIDA / "15_extraccion_TC.json")
    if not estudios:
        sys.exit("Falta cribado/salida/15_extraccion_TC.json: ejecuta antes 15_aplicar_texto_completo.py")
    spec = importlib.util.spec_from_file_location("gen09", Path(__file__).with_name("09_generar_script_parsifal.py"))
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)

    filas, datos = [], {}
    for i, e in sorted(estudios.items()):
        p = {q: e["calidad"][q]["p"] for q in ITEMS}
        filas.append({"id": i, "titulo": e["titulo"], "anio": e["anio"], **p, "total": sum(p.values())})
        datos[i] = [gen.norm(e["titulo"]), {q: RESPUESTA[float(v)] for q, v in p.items()}]
    totales = [f["total"] for f in filas]
    print(f"Calidad de {len(filas)} estudios: media {statistics.mean(totales):.2f} / 8 "
          f"(DE {statistics.stdev(totales):.2f}; rango {min(totales):g}-{max(totales):g}).")
    print("Ítem   Sí  Parcial  No")
    for q in ITEMS:
        c = Counter(f[q] for f in filas)
        print(f"{q}  {c[1]:>4} {c[0.5]:>6} {c[0]:>5}")
    altos = [f["id"] for f in filas if f["total"] >= 6]
    print(f"Calidad alta (≥ 6): {len(altos)} estudios.")
    escribir_csv(SALIDA / "16_calidad_resumen.csv", filas, ["id", "titulo", "anio", *ITEMS, "total"])
    salida = SALIDA / "parsifal" / "cargar_calidad_en_parsifal.js"
    salida.write_text(PLANTILLA.replace("__DATOS__", json.dumps(datos, ensure_ascii=False)), encoding="utf-8")
    print(f"Creado {salida.name}: pégalo en Parsif.al > Conducting > Quality Assessment (F12 > Console).")


if __name__ == "__main__":
    main()
