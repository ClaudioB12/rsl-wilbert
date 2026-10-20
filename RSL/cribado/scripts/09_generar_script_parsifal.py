#!/usr/bin/env python3
"""PASO 9. Genera un script para la consola del navegador que coloca en Parsif.al las decisiones
de TA.xlsx: estado (Accepted / Rejected), criterio de selección y comentario de cada estudio.

Parsif.al no tiene una API pública ni importa el estado desde BibTeX. El script generado se pega
en la consola del navegador (F12) estando dentro de tu revisión en parsif.al: usa tu propia sesión
y hace lo mismo que harías tú abriendo cada estudio, eligiendo el estado y pulsando «Save».

Requisitos en Parsif.al:
  - Los estudios importados desde cribado/salida/parsifal/<Base>.bib. Parsif.al deja vacía la
    «Bibtex Key» al importar, así que cada estudio se busca por su título y se confirma con el ID
    que va en el campo «note» («ID cribado R0001»).
  - Los criterios de selección creados como en PARSIFAL_COPIAR_PEGAR.md (cada uno empieza por su
    código: «CE-2: …»).

Uso (desde la carpeta RSL):   python cribado/scripts/09_generar_script_parsifal.py
Salida: cribado/salida/parsifal/cargar_en_parsifal.js

Correspondencia: Incluir → Accepted; Duda → Accepted con «[Duda]» al inicio del comentario
(pasa a texto completo); Excluir → Rejected con su criterio. Filas sin decisión no se tocan.
"""
import json
import re
import unicodedata

from comun import REVISION, SALIDA, asegurar_utf8_consola
from hojas import leer_hoja

PLANTILLA = r"""// Script generado por cribado/scripts/09_generar_script_parsifal.py. No editar a mano.
// Pegar en la consola del navegador (F12 > Console) estando en tu revisión de parsif.al
// (Conducting > Study Selection). Ver cribado/PARSIFAL_CARGAR_DECISIONES.md.
(async () => {
  const DATOS = __DATOS__;
  const rid = (document.querySelector("#review-id") || {}).value;
  if (!rid) { alert("Abre primero tu revisión en Parsif.al (Conducting > Study Selection) y vuelve a pegar el script."); return; }
  const texto = async (url) => { const r = await fetch(url, { credentials: "same-origin" }); if (!r.ok) throw new Error(url + " → " + r.status); return r.text(); };
  const html = (t) => new DOMParser().parseFromString(t, "text/html");

  console.log("Leyendo los estudios de la revisión…");
  const lista = html(await texto(`/reviews/conducting/source_articles/?review-id=${rid}&source-id=None`));
  const norm = (t) => (t || "").normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]/g, "");
  const oid = {}, repetidos = new Set();
  lista.querySelectorAll("tr[oid]").forEach((tr) => {
    const t = norm(tr.children[2].textContent);
    if (oid[t]) repetidos.add(t); else oid[t] = tr.getAttribute("oid");
  });
  const id2oid = {};
  for (const [k, d] of Object.entries(DATOS)) if (oid[d[3]]) id2oid[k] = oid[d[3]];
  const claves = Object.keys(id2oid);
  const faltan = Object.keys(DATOS).filter((k) => !id2oid[k]);
  console.log(`Estudios en Parsif.al: ${lista.querySelectorAll("tr[oid]").length}. Coinciden con TA.xlsx: ${claves.length}. De TA.xlsx sin coincidencia: ${faltan.length}.`);
  if (!claves.length) { alert("Ningún estudio coincide por título. ¿Importaste los archivos de cribado/salida/parsifal/?"); return; }

  const form0 = html(await texto(`/reviews/conducting/article_details/?review-id=${rid}&article-id=${id2oid[claves[0]]}`)).querySelector("#article-details");
  const criterio = {};
  form0.querySelectorAll("select[name=selection_criteria] option").forEach((o) => {
    const m = o.textContent.trim().match(/^(C[IE]-\d+)/); if (m) criterio[m[1]] = o.value;
  });
  const usados = [...new Set(claves.map((k) => DATOS[k][1]).filter(Boolean))];
  const sinCriterio = usados.filter((c) => !criterio[c]);
  if (sinCriterio.length) console.warn("Criterios que no existen en Parsif.al (se guardan solo en el comentario): " + sinCriterio.join(", "));
  if (!confirm(`Se van a actualizar ${claves.length} estudios en Parsif.al (estado, criterio y comentario). ¿Continuar?`)) return;

  let ok = 0, err = [];
  const guardar = async (k) => {
    const [estado, crit, comentario] = DATOS[k];
    const f = html(await texto(`/reviews/conducting/article_details/?review-id=${rid}&article-id=${id2oid[k]}`)).querySelector("#article-details");
    const nota = (f.querySelector("[name=note]") || {}).value || "";
    const m = nota.match(/ID cribado (R\d+)/);
    if (m && m[1] !== k) throw new Error("el título coincide con " + m[1] + ", no se toca");
    const datos = new URLSearchParams();
    // Parsif.al muestra «None» en los campos vacíos sin valor; se envían vacíos para no guardarlo como texto.
    f.querySelectorAll("input[name], textarea[name], select[name]").forEach((e) => datos.set(e.name, e.value === "None" ? "" : e.value));
    datos.set("status", estado);
    datos.set("selection_criteria", crit && criterio[crit] ? criterio[crit] : "");
    datos.set("comments", comentario);
    if (!datos.get("bibtex-key")) datos.set("bibtex-key", k);
    const r = await fetch("/reviews/conducting/save_article_details/", {
      method: "POST", credentials: "same-origin", body: datos,
      headers: { "X-CSRFToken": datos.get("csrfmiddlewaretoken") || "", "X-Requested-With": "XMLHttpRequest" },
    });
    if (!r.ok) throw new Error("HTTP " + r.status);
  };
  const cola = [...claves];
  const trabajador = async () => {
    while (cola.length) {
      const k = cola.shift();
      try { await guardar(k); ok++; } catch (e) { err.push(k + " (" + e.message + ")"); }
      if ((ok + err.length) % 50 === 0) console.log(`… ${ok + err.length} de ${claves.length}`);
    }
  };
  await Promise.all([1, 2, 3, 4].map(trabajador));
  console.log(`LISTO: ${ok} estudios actualizados, ${err.length} con error.`);
  if (err.length) console.warn("Con error (vuelve a pegar el script para reintentar): " + err.join(", "));
  if (faltan.length) console.warn("IDs de TA.xlsx que no están en Parsif.al: " + faltan.slice(0, 50).join(", ") + (faltan.length > 50 ? " …" : ""));
  alert(`Listo: ${ok} estudios actualizados${err.length ? ", " + err.length + " con error (ver consola)" : ""}. Recarga la página para verlos.`);
})();
"""


def norm(t):
    """Igual que norm() del script JS: sin tildes, minúsculas, solo letras y números."""
    t = unicodedata.normalize("NFKD", t or "")
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in t if not unicodedata.combining(c)).lower())


def main():
    asegurar_utf8_consola()
    hoja = leer_hoja(REVISION / "TA.xlsx")
    datos = {}
    for i, v in hoja.items():
        d = v["decision"]
        if d not in ("Incluir", "Duda", "Excluir"):
            continue
        crit = v["criterio"] if d == "Excluir" else ""
        # La confianza de la IA solo se muestra mientras el autor no ha verificado la fila.
        conf = v.get("Confianza IA", "") if v["comentario"].startswith("IA (verificar)") else ""
        etiqueta = "Duda" if d == "Duda" else f"Excluir {crit}" if d == "Excluir" else "Incluir"
        etiqueta = f"[{etiqueta}{' · confianza IA ' + conf if conf else ''}]"
        datos[i] = ["R" if d == "Excluir" else "A", crit, f"{etiqueta} {v['comentario']}"[:4000], norm(v["Título"])]
    salida = SALIDA / "parsifal" / "cargar_en_parsifal.js"
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(PLANTILLA.replace("__DATOS__", json.dumps(datos, ensure_ascii=False)), encoding="utf-8")
    n = {x: sum(1 for d in datos.values() if d[0] == x) for x in "AR"}
    print(f"Creado {salida}: {len(datos)} estudios (Accepted {n['A']}, Rejected {n['R']}).")
    print("Pégalo en la consola del navegador (F12) dentro de tu revisión en parsif.al. Ver cribado/PARSIFAL_CARGAR_DECISIONES.md.")


if __name__ == "__main__":
    main()
