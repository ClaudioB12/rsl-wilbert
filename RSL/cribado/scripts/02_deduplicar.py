#!/usr/bin/env python3
"""PASO 2. Elimina duplicados, verifica el conjunto de control y prepara la importación a Parsif.al.

Criterio de duplicado (CE-1): mismo DOI, o mismo título normalizado (sin mayúsculas,
tildes ni signos) con año igual o con un año de diferencia. Se conserva el registro
más completo (con resumen y palabras clave) y se anotan todas las bases donde apareció.

Uso (desde la carpeta RSL):   python cribado/scripts/02_deduplicar.py
Salidas en cribado/salida/:
  02_registros_unicos.csv     registros únicos con ID (R0001...) y señales de apoyo
  02_duplicados.csv           cada duplicado eliminado y con qué registro coincidió
  02_conjunto_control.csv     dónde apareció cada uno de los estudios ya incluidos (S01-S21)
  parsifal/<Base>.bib         un archivo por base para importar en Parsif.al (sin duplicados)
"""
import json
from collections import defaultdict

from comun import (BASES, NOMBRE_BASE, SALIDA, SUPLEMENTOS, asegurar_utf8_consola, escribir_csv, leer_csv,
                   normalizar_doi, normalizar_titulo, senales)


def completitud(r):
    return (bool(r["resumen"]), len(r["resumen"]), bool(r["palabras_clave"]), bool(r["doi"]))


def bib_escape(s):
    return (s or "").replace("{", "").replace("}", "").replace("\\", "")


def escribir_bib(ruta, regs):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        for r in regs:
            conf = any(x in (r["tipo_doc"] or "").lower() for x in ("conference", "proceeding", "inproceedings"))
            tipo = "inproceedings" if conf else "article"
            campo_fuente = "booktitle" if conf else "journal"
            autores = " and ".join(a.strip() for a in r["autores"].split(";") if a.strip())
            f.write(f"@{tipo}{{{r['id']},\n")
            for k, v in [("title", r["titulo"]), ("author", autores), ("year", r["anio"]),
                         (campo_fuente, r["fuente"]), ("doi", r["doi"]), ("abstract", r["resumen"]),
                         ("keywords", r["palabras_clave"]), ("note", f"ID cribado {r['id']}; bases: {r['bases']}")]:
                if v:
                    f.write(f"  {k} = {{{bib_escape(str(v))}}},\n")
            f.write("}\n\n")


def main():
    asegurar_utf8_consola()
    todos = leer_csv(SALIDA / "01_registros_todos.csv")
    for r in todos:
        r["anio"] = int(r["anio"]) if r["anio"] else None
    orden = {b: i for i, b in enumerate(BASES)}
    todos.sort(key=lambda r: orden[r["base"]])          # la base prioritaria «gana» el registro

    unicos, por_doi, por_titulo, duplicados = [], {}, defaultdict(list), []
    for r in todos:
        doi, tit = normalizar_doi(r["doi"]), normalizar_titulo(r["titulo"])
        previo = por_doi.get(doi) if doi else None
        if previo is None and tit:
            for c in por_titulo.get(tit, []):
                if not r["anio"] or not c["anio"] or abs(r["anio"] - c["anio"]) <= 1:
                    previo = c
                    break
        if previo is not None:
            motivo = "DOI" if doi and normalizar_doi(previo["doi"]) == doi else "título"
            duplicados.append({"base": r["base"], "titulo": r["titulo"], "anio": r["anio"], "doi": r["doi"],
                               "coincide_con_base": previo["base"], "motivo": motivo, "_ref": previo})
            previo["_bases"].add(r["base"])
            if completitud(r) > completitud(previo):              # conservar los datos más completos
                for k in ("resumen", "palabras_clave", "doi", "tipo_doc", "idioma", "url"):
                    if r[k] and not previo[k]:
                        previo[k] = r[k]
                if len(r["resumen"]) > len(previo["resumen"]):
                    previo["resumen"] = r["resumen"]
            continue
        r["_bases"] = {r["base"]}
        unicos.append(r)
        if doi:
            por_doi[doi] = r
        if tit:
            por_titulo[tit].append(r)

    unicos.sort(key=lambda r: normalizar_titulo(r["titulo"]))
    for i, r in enumerate(unicos, 1):
        r["id"] = f"R{i:04d}"
        r["bases"] = ", ".join(NOMBRE_BASE[b] for b in BASES if b in r["_bases"])
        r["base_atribuida"] = r["base"]
        r["senales"] = senales(r)
    for d in duplicados:
        d["id_conservado"] = d.pop("_ref")["id"]

    campos = ["id", "titulo", "autores", "anio", "fuente", "doi", "tipo_doc", "idioma", "resumen",
              "palabras_clave", "base_atribuida", "bases", "senales", "url"]
    escribir_csv(SALIDA / "02_registros_unicos.csv", unicos, campos)
    escribir_csv(SALIDA / "02_duplicados.csv", duplicados,
                 ["base", "titulo", "anio", "doi", "coincide_con_base", "id_conservado", "motivo"])
    for b in BASES:
        escribir_bib(SALIDA / "parsifal" / f"{b}.bib", [r for r in unicos if r["base_atribuida"] == b])

    # Conjunto de control: los estudios ya incluidos en la v2 deben aparecer en la búsqueda.
    control = json.loads((SUPLEMENTOS / "matriz_extraccion.json").read_text(encoding="utf-8"))
    filas_c = []
    for e in control:
        doi, tit = normalizar_doi(e.get("doi", "")), normalizar_titulo(e["titulo"])
        hallado = next((r for r in unicos if (doi and normalizar_doi(r["doi"]) == doi) or normalizar_titulo(r["titulo"]) == tit), None)
        filas_c.append({"id_estudio": e["id"], "titulo": e["titulo"], "anio": e["anio"],
                        "encontrado": "Sí" if hallado else "No", "id_registro": hallado["id"] if hallado else "",
                        "bases": hallado["bases"] if hallado else ""})
    escribir_csv(SALIDA / "02_conjunto_control.csv", filas_c,
                 ["id_estudio", "titulo", "anio", "encontrado", "id_registro", "bases"])

    print(f"Registros leídos:      {len(todos)}")
    print(f"Duplicados eliminados: {len(duplicados)}  (por DOI: {sum(d['motivo'] == 'DOI' for d in duplicados)}, por título: {sum(d['motivo'] == 'título' for d in duplicados)})")
    print(f"Registros únicos:      {len(unicos)}")
    print("Registros únicos atribuidos a cada base (archivos para Parsif.al):")
    for b in BASES:
        print(f"  {NOMBRE_BASE[b]:<22} {sum(r['base_atribuida'] == b for r in unicos):>5}  -> salida/parsifal/{b}.bib")
    no = [f for f in filas_c if f["encontrado"] == "No"]
    print(f"\nConjunto de control: {len(filas_c) - len(no)} de {len(filas_c)} estudios incluidos aparecen en la búsqueda.")
    for f in no:
        print(f"  NO encontrado: {f['id_estudio']} {f['titulo'][:70]}")
    print("  (Se esperaba que S03 y S14 no aparezcan: se declaran en «otros métodos». Si falta otro, revisen la cadena o la exportación.)")


if __name__ == "__main__":
    main()
