#!/usr/bin/env python3
"""PASO 6. Calcula las cifras del diagrama PRISMA y actualiza los datos del manuscrito.

Requisitos: etapas TA y TC cerradas (04_cerrar_etapa.py) y
            cribado/exportaciones/fechas_busqueda.csv completo.
Uso (desde la carpeta RSL):   python cribado/scripts/06_resultados_prisma.py

Hace lo siguiente:
  1. Calcula identificados por base, duplicados, cribados, excluidos y motivos.
  2. Reemplaza los valores en manuscrito/datos_busqueda.tex (fechas, conteos, kappa).
  3. Escribe manuscrito/generado/base_recuperacion.tex (base de cada estudio, Anexo B).
  4. Compara los incluidos con el corpus actual (S01-S21) y avisa de diferencias.
  5. Escribe en cribado/salida/:
       06_resumen_prisma.txt               resumen legible de todo el proceso
       06_excluidos_texto_completo.csv     estudios excluidos a texto completo con motivo (PRISMA 16b)
       06_estado_para_parsifal.csv         decisión final de cada registro para marcarla en Parsif.al
"""
import json
import re
from collections import Counter
from datetime import datetime

from comun import (BASES, DESCRIPCION_CRITERIO, EXPORTACIONES, MANUSCRITO, NOMBRE_BASE, SALIDA, SUPLEMENTOS,
                   asegurar_utf8_consola, cargar_json, escribir_csv, leer_csv, normalizar_doi, normalizar_titulo)

MESES_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
            "October", "November", "December"]
MACRO_CRITERIO = {"CE-2": "PexclCEdos", "CE-3": "PexclCEtres", "CE-4": "PexclCEcuatro", "CE-5": "PexclCEcinco",
                  "CI-6": "PexclCIseis", "CE-6": "PexclCEseis"}


def fecha(texto):
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(texto.strip(), fmt)
        except ValueError:
            pass
    return None


def coma(x):
    return f"{float(x):.2f}".replace(".", ",")


def reemplazar_macros(valores):
    ruta = MANUSCRITO / "datos_busqueda.tex"
    lineas, hechos = ruta.read_text(encoding="utf-8").splitlines(), []
    for i, l in enumerate(lineas):
        m = re.match(r"^\\newcommand\{\\(\w+)\}\{.*\}(\s*%.*)?$", l)
        if m and m.group(1) in valores:
            lineas[i] = f"\\newcommand{{\\{m.group(1)}}}{{{valores[m.group(1)]}}}" + (m.group(2) or "")
            hechos.append(m.group(1))
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return hechos


def main():
    asegurar_utf8_consola()
    todos = leer_csv(SALIDA / "01_registros_todos.csv")
    unicos = leer_csv(SALIDA / "02_registros_unicos.csv")
    ta, tc = cargar_json(SALIDA / "decision_TA.json"), cargar_json(SALIDA / "decision_TC.json")
    if not ta or not tc:
        raise SystemExit("Faltan etapas cerradas: ejecuta 04_cerrar_etapa.py --etapa TA y --etapa TC.")
    fiab = cargar_json(SALIDA / "fiabilidad.json", {})
    fechas = {f["base"]: f for f in leer_csv(EXPORTACIONES / "fechas_busqueda.csv")}

    por_base = Counter(r["base"] for r in todos)
    v = {}
    for b in BASES:
        v[f"N{b}"] = str(por_base.get(b, 0))
        f = fecha(fechas.get(b, {}).get("fecha", ""))
        if f:
            v[f"F{b}"] = f.strftime("%d/%m/%Y")
    ultimas = [fecha(f["fecha"]) for f in fechas.values() if fecha(f.get("fecha", ""))]
    if ultimas:
        u = max(ultimas)
        v["FechaBusqueda"], v["FechaBusquedaEN"] = u.strftime("%d/%m/%Y"), f"{u.day} {MESES_EN[u.month - 1]} {u.year}"

    c_ta = Counter(x["decision"] for x in ta.values())
    c_tc = Counter(x["decision"] for x in tc.values())
    excl_tc = {i: x for i, x in tc.items() if x["decision"] == "Excluir"}
    crit = Counter(x["criterio"] for x in excl_tc.values())
    v.update({"Pidentificados": str(len(todos)), "Pduplicados": str(len(todos) - len(unicos)),
              "Pcribados": str(len(unicos)), "PexclTA": str(c_ta["Excluir"]), "Pbuscados": str(c_ta["Incluir"]),
              "PnoRecuperados": str(c_tc["No recuperado"]), "Pevaluados": str(c_ta["Incluir"] - c_tc["No recuperado"]),
              "PexclTC": str(len(excl_tc))})
    for c, macro in MACRO_CRITERIO.items():
        v[macro] = str(crit.get(c, 0))
    v["PexclOtros"] = str(sum(n for c, n in crit.items() if c not in MACRO_CRITERIO))
    for clave, macro in (("recribado_TA", "KappaRecribadoTA"), ("recribado_TC", "KappaRecribadoTC"),
                         ("asistente_TA", "KappaAsistenteTA")):
        k = fiab.get(clave, {}).get("kappa")
        if k is not None:
            v[macro] = coma(k)
    for clave, macro in (("recribado_TA", "NRecribadoTA"), ("recribado_TC", "NRecribadoTC")):
        if clave in fiab:
            v[macro] = str(fiab[clave]["n"])
    if "asistente_TA" in fiab:
        a = fiab["asistente_TA"]
        v["AcuerdoAsistenteTA"] = f"{round(100 * a['acuerdo'])}~\\%"
        v["NExclRegla"] = str(a["exclusiones_regla"])
        v["NExclReglaConfirmadas"] = str(a["exclusiones_regla_confirmadas"])
    if "IA_TA" in fiab:
        a = fiab["IA_TA"]
        v["AcuerdoIATA"] = f"{round(100 * a['acuerdo'])}~\\%"
        v["KappaIATA"] = coma(a["kappa"]) if a["kappa"] is not None else "---"
        v["NCambiosIATA"] = str(a["decisiones_cambiadas"])
    v["NexclOA"] = str(sum(1 for x in ta.values() if x["decision"] == "Excluir" and x["criterio"] == "CI-2"))
    if (SALIDA / "11_openalex_cache.json").exists():
        fechas_oa = [x.get("fecha") for x in cargar_json(SALIDA / "11_openalex_cache.json", {}).values() if x.get("fecha")]
        if fechas_oa:
            f = fecha(max(fechas_oa))
            v["FechaOA"] = f.strftime("%d/%m/%Y") if f else max(fechas_oa)
    if (SALIDA / "01_fuera_de_filtros.csv").exists():
        v["NFueraFiltros"] = str(len(leer_csv(SALIDA / "01_fuera_de_filtros.csv")))
    if "calidad" in fiab:
        v["AcuerdoCalidad"] = f"{round(100 * fiab['calidad']['acuerdo'])}~\\%"

    # Incluidos frente al corpus actual
    incluidos = {i for i, x in tc.items() if x["decision"] == "Incluir"}
    reg = {r["id"]: r for r in unicos}
    corpus = json.loads((SUPLEMENTOS / "matriz_extraccion.json").read_text(encoding="utf-8"))
    base_recup, avisos, otros = {}, [], []
    ids_corpus_encontrados = set()
    for e in corpus:
        doi, tit = normalizar_doi(e.get("doi", "")), normalizar_titulo(e["titulo"])
        r = next((r for r in unicos if (doi and normalizar_doi(r["doi"]) == doi) or normalizar_titulo(r["titulo"]) == tit), None)
        if r is None:
            otros.append(e["id"])
            base_recup[e["id"]] = "Otros métodos (búsqueda v1, ACM texto completo)"
            continue
        ids_corpus_encontrados.add(r["id"])
        base_recup[e["id"]] = r["bases"]
        if r["id"] not in incluidos:
            estado = tc.get(r["id"], ta.get(r["id"], {}))
            avisos.append(f"{e['id']} ({e['primer_autor']} {e['anio']}) está en el corpus pero el cribado lo dejó como "
                          f"«{estado.get('decision')}» {estado.get('criterio', '')}. Revisen la decisión o avisen para actualizar el corpus.")
    nuevos = sorted(incluidos - ids_corpus_encontrados)
    for i in nuevos:
        avisos.append(f"NUEVO estudio incluido {i}: «{reg[i]['titulo'][:80]}». Hay que extraer sus datos y evaluar su calidad.")
    v["POtrosIdentificados"] = str(len(otros))
    v["POtrosIncluidos"] = str(len(otros))
    hechos = reemplazar_macros(v)

    lineas = ["% Generado por cribado/scripts/06_resultados_prisma.py. No editar a mano."]
    for sid, bases in sorted(base_recup.items()):
        lineas.append(f"\\expandafter\\def\\csname baserecup{sid}\\endcsname{{{bases}}}")
    (MANUSCRITO / "generado" / "base_recuperacion.tex").write_text("\n".join(lineas) + "\n", encoding="utf-8")

    escribir_csv(SALIDA / "06_excluidos_texto_completo.csv",
                 [{"id": i, "titulo": reg[i]["titulo"], "anio": reg[i]["anio"], "doi": reg[i]["doi"],
                   "criterio": x["criterio"], "descripcion": DESCRIPCION_CRITERIO.get(x["criterio"], ""),
                   "evidencia": x["evidencia"], "nota": x["nota"]} for i, x in sorted(excl_tc.items())],
                 ["id", "titulo", "anio", "doi", "criterio", "descripcion", "evidencia", "nota"])
    estado = []
    for r in unicos:
        t = tc.get(r["id"])
        d = t or ta.get(r["id"], {})
        etapa = "Texto completo" if t else "Título y resumen"
        parsifal = {"Incluir": "Accepted", "Excluir": "Rejected", "No recuperado": "Rejected"}.get(d.get("decision"), "")
        estado.append({"id": r["id"], "base_atribuida": NOMBRE_BASE.get(r["base_atribuida"], r["base_atribuida"]),
                       "titulo": r["titulo"], "estado_parsifal": parsifal, "decision": d.get("decision"),
                       "criterio": d.get("criterio") or ("No recuperado" if d.get("decision") == "No recuperado" else ""),
                       "etapa": etapa})
    escribir_csv(SALIDA / "06_estado_para_parsifal.csv", estado,
                 ["id", "base_atribuida", "titulo", "estado_parsifal", "decision", "criterio", "etapa"])

    res = ["RESUMEN PRISMA 2020", "=" * 40]
    for b in BASES:
        res.append(f"{NOMBRE_BASE[b]:<22} {v[f'N{b}']:>6}   fecha {v.get(f'F{b}', '¿?')}")
    res += [f"{'Identificados':<22} {v['Pidentificados']:>6}", f"{'Duplicados':<22} {v['Pduplicados']:>6}",
            f"{'Cribados (TA)':<22} {v['Pcribados']:>6}", f"{'Excluidos TA':<22} {v['PexclTA']:>6}",
            f"{'Buscados a TC':<22} {v['Pbuscados']:>6}", f"{'No recuperados':<22} {v['PnoRecuperados']:>6}",
            f"{'Evaluados TC':<22} {v['Pevaluados']:>6}", f"{'Excluidos TC':<22} {v['PexclTC']:>6}"]
    for c in sorted(crit):
        res.append(f"   {c} {DESCRIPCION_CRITERIO.get(c, '')[:55]:<55} {crit[c]:>4}")
    res += [f"{'Incluidos desde bases':<22} {len(incluidos):>6}", f"{'Otros métodos':<22} {len(otros):>6}  ({', '.join(otros)})",
            f"{'TOTAL INCLUIDOS':<22} {len(incluidos) + len(otros):>6}", ""]
    for clave, valor in fiab.items():
        res.append(f"{clave:<16} {valor}")
    res += ["", f"Macros actualizadas en datos_busqueda.tex: {len(hechos)}"]
    if avisos:
        res += ["", "AVISOS (resolver antes de enviar):"] + ["  - " + a for a in avisos]
    texto = "\n".join(res)
    (SALIDA / "06_resumen_prisma.txt").write_text(texto + "\n", encoding="utf-8")
    print(texto)
    print("\nSuban a Overleaf: manuscrito/datos_busqueda.tex y manuscrito/generado/base_recuperacion.tex "
          "(o usen 08_paquete_overleaf.py).")


if __name__ == "__main__":
    main()
