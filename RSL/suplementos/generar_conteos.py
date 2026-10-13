#!/usr/bin/env python3
"""Genera la matriz de extracción y todos los conteos de la RSL.

Entrada : suplementos/matriz_extraccion.json (una entrada por estudio incluido).
Salidas :
  - suplementos/matriz_extraccion.xlsx  (matriz, calidad por ítem, cruces)
  - manuscrito/generado/*.tex           (tablas y macros con cifras que usa el manuscrito)

Uso: python3 suplementos/generar_conteos.py
Cada cifra del resumen, del texto y de las tablas proviene de este script; no se
escriben conteos a mano en el .tex.
"""
import json
import statistics
from collections import Counter, OrderedDict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SUPL = RAIZ / "suplementos"
MATRIZ = SUPL / "matriz_extraccion.json"
CURACION = SUPL / "curacion.json"
FICHAS = SUPL / "extraccion_individual"
SALIDA_TEX = RAIZ / "manuscrito" / "generado"
SALIDA_XLSX = RAIZ / "suplementos" / "matriz_extraccion.xlsx"

FAMILIAS = OrderedDict([
    ("recurrente", "Recurrentes (LSTM, GRU, Bi-LSTM)"),
    ("convolucional", "Convolucionales (CNN, TCN, 3D-CNN)"),
    ("autoencoder", "Autoencoders y reconstrucci\\'{o}n"),
    ("grafos", "Grafos (GNN, GCN, GAT)"),
    ("transformer_atencion", "Transformers y atenci\\'{o}n"),
    ("generativo", "Generativos (GAN, VAE, difusi\\'{o}n)"),
])
FAM_CORTA = OrderedDict([
    ("recurrente", "Rec."), ("convolucional", "Conv."), ("autoencoder", "AE"),
    ("grafos", "Grafo"), ("transformer_atencion", "Transf."), ("generativo", "Gen."),
])
TIPOS_DATO = ["series de sensores", "movilidad OD/agregada", "trayectorias GPS",
              "video/imágenes", "multimodal", "simulado"]
CATEGORIAS = ["accidentes/incidentes", "congestión/flujo anómalo",
              "trayectorias/conducción peligrosa",
              "disrupciones/eventos extremos/infraestructura"]
ETIQUETAS = ["registros reales de incidentes", "anotación manual/experta",
             "benchmark anotado de terceros", "anomalías inyectadas/sintéticas",
             "mixto", "sin etiquetas", "no reportado"]
METRICAS = OrderedDict([
    ("accuracy", "Accuracy"), ("precision", "Precision"), ("recall", "Recall"),
    ("f1", "F1-score"), ("auc_roc", "AUC-ROC"), ("pr_auc", "PR-AUC"),
    ("dr", "Tasa de detecci\\'{o}n (DR)"), ("far_fpr", "FAR / FPR"),
    ("mttd", "Tiempo medio de detecci\\'{o}n"),
    ("error_mae_rmse_mape", "MAE / RMSE / MAPE"), ("iou_map", "IoU / mAP"),
    ("operativas_latencia_fps_energia", "Latencia / FPS / energ\\'{i}a"),
])
LIMITACIONES = OrderedDict([
    ("datos_replicabilidad", "Datos propios o de acceso limitado"),
    ("etiquetado", "Etiquetado de anomal\\'{i}as"),
    ("generalizacion", "Generalizaci\\'{o}n a otros escenarios"),
    ("metricas_no_uniformes", "M\\'{e}tricas no comparables"),
    ("costo_despliegue", "Costo computacional y despliegue"),
    ("interpretabilidad", "Interpretabilidad"),
])
QA = OrderedDict([
    ("QA1", "Procedencia y verificaci\\'{o}n de etiquetas"),
    ("QA2", "Partici\\'{o}n sin fuga (temporal o prueba independiente)"),
    ("QA3", "L\\'{i}neas base comparables"),
    ("QA4", "Reporte de variabilidad"),
    ("QA5", "C\\'{o}digo y datos disponibles"),
    ("QA6", "Validaci\\'{o}n en m\\'{a}s de un escenario"),
    ("QA7", "Protocolo de evaluaci\\'{o}n expl\\'{i}cito"),
    ("QA8", "Limitaciones declaradas"),
])
UMBRAL_ALTA = 5.0  # de 8: estudios de calidad alta para el análisis de sensibilidad


def esc(s):
    """Escapa texto plano para LaTeX."""
    rep = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
           "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\^{}",
           "\u2212": r"$-$", "\u2248": r"$\approx$", "\u00b1": r"$\pm$", "\u2265": r"$\geq$",
           "\u2264": r"$\leq$", "\u00d7": r"$\times$", "\u2013": "--", "\u2014": "---"}
    return "".join(rep.get(c, c) for c in str(s))


def pct(n, total):
    return f"{round(100 * n / total)}~\\%"


def ids(estudios, cond):
    return [e["id"] for e in estudios if cond(e)]


def lista_ids(xs):
    return ", ".join(xs) if xs else "---"


def macro(nombre, valor):
    assert nombre.isalpha(), f"nombre de macro LaTeX inválido: {nombre}"
    return f"\\newcommand{{\\{nombre}}}{{{valor}}}\n"


def cargar():
    """Une cada ficha individual con su curación y escribe la matriz consolidada."""
    cur = json.loads(CURACION.read_text(encoding="utf-8"))
    estudios = []
    for c in cur["incluidos"]:
        e = json.loads((FICHAS / f"{c['clave_extraccion']}.json").read_text(encoding="utf-8"))
        e.update(cur["overrides"].get(c["clave_extraccion"], {}))
        e.update(c)
        estudios.append(e)
    MATRIZ.write_text(json.dumps(estudios, ensure_ascii=False, indent=1), encoding="utf-8")
    for e in estudios:
        e["qa_total"] = sum(e["calidad"][q]["p"] for q in QA)
    return estudios


def tabla(cabecera, filas, formato, titulo, etiqueta, nota=None, pequena=True):
    out = ["\\begin{table}[H]", "\\centering"]
    if pequena:
        out.append("\\small")
    out.append(f"\\caption{{{titulo}}}\\label{{{etiqueta}}}")
    out.append(f"\\begin{{tabularx}}{{\\linewidth}}{{{formato}}}")
    out.append("\\toprule")
    out.append(" & ".join(f"\\textbf{{{c}}}" for c in cabecera) + " \\\\")
    out.append("\\midrule")
    for f in filas:
        if f == "MIDRULE":
            out.append("\\midrule")
        else:
            out.append(" & ".join(str(c) for c in f) + " \\\\")
    out.append("\\bottomrule")
    out.append("\\end{tabularx}")
    if nota:
        out.append(f"\\par\\vspace{{2pt}}{{\\footnotesize\\raggedright {nota}\\par}}")
    out.append("\\end{table}")
    return "\n".join(out) + "\n"


def generar(estudios):
    n = len(estudios)
    m = []  # macros
    m.append(macro("Nestudios", n))
    anios = Counter(e["anio"] for e in estudios)
    m.append(macro("AnioMin", min(anios)))
    m.append(macro("AnioMax", max(anios)))
    for a in range(2020, 2027):
        m.append(macro(f"Anio{'ABCDEFG'[a - 2020]}", anios.get(a, 0)))
    m.append(macro("NrecientesVeintidosVeintiseis", sum(v for a, v in anios.items() if a >= 2024)))

    # Calidad
    tot = [e["qa_total"] for e in estudios]
    m.append(macro("QAmedia", f"{statistics.mean(tot):.2f}"))
    m.append(macro("QAde", f"{statistics.pstdev(tot):.2f}"))
    m.append(macro("QAmin", f"{min(tot):.1f}"))
    m.append(macro("QAmax", f"{max(tot):.1f}"))
    alta = [e for e in estudios if e["qa_total"] >= UMBRAL_ALTA]
    m.append(macro("QAumbralAlta", f"{UMBRAL_ALTA:.1f}"))
    m.append(macro("NaltaCalidad", len(alta)))
    m.append(macro("IDaltaCalidad", lista_ids([e["id"] for e in alta])))
    for q in QA:
        si = sum(1 for e in estudios if e["calidad"][q]["p"] == 1)
        m.append(macro(f"QA{'Uno Dos Tres Cuatro Cinco Seis Siete Ocho'.split()[int(q[2]) - 1]}si", si))
    m.append(macro("Ncodigo", sum(1 for e in estudios if e["calidad"]["QA5"]["p"] > 0)))
    m.append(macro("NcodigoURL", sum(1 for e in estudios if e["codigo_disponible"].lower().startswith("http"))))
    m.append(macro("NetiqVerificadas", sum(1 for e in estudios if e["calidad"]["QA1"]["p"] == 1)))
    m.append(macro("NdatosSimuladosAny", sum(1 for e in estudios if any(d["tipo"] == "simulado" for d in e["datasets"]))))
    m.append(macro("NdatasetPropio", sum(1 for e in estudios if all(d["publico"] == "no" for d in e["datasets"]))))
    m.append(macro("Nvariabilidad", sum(1 for e in estudios if e["calidad"]["QA4"]["p"] == 1)))

    # Tipo de dato y entorno
    for t, nombre in zip(TIPOS_DATO, ["Sensores", "Movilidad", "Trayectorias", "Video", "Multimodal", "Simulado"]):
        m.append(macro(f"Ndato{nombre}", sum(1 for e in estudios if e["tipo_dato"] == t)))
    ent = Counter(e["entorno"] for e in estudios)
    m.append(macro("Nurbano", ent.get("urbano", 0)))
    m.append(macro("Nautopista", ent.get("autopista", 0)))
    m.append(macro("Nambos", ent.get("ambos", 0)))
    m.append(macro("NentornoNE", ent.get("no especificado", 0)))

    # Familias
    for k in FAMILIAS:
        m.append(macro(f"Nfam{FAM_CORTA[k].replace('.', '')}", sum(1 for e in estudios if e["familias"][k])))
    m.append(macro("Nhibrido", sum(1 for e in estudios if e["hibrido"])))
    m.append(macro("Nmultimodal", sum(1 for e in estudios if e["multimodal"])))

    # Etiquetas y protocolo
    et = Counter(e["origen_etiquetas"] for e in estudios)
    for t, nombre in zip(ETIQUETAS, ["Real", "Manual", "Bench", "Inyect", "Mixto", "Sin", "NR"]):
        m.append(macro(f"Netiq{nombre}", et.get(t, 0)))
    m.append(macro("Ntasa", sum(1 for e in estudios if not e["tasa_anomalias"].lower().startswith("no reportad"))))
    m.append(macro("Numbral", sum(1 for e in estudios if not e["umbral"].lower().startswith("no reportad"))))
    m.append(macro("Nparticion", sum(1 for e in estudios if not e["particion"].lower().startswith("no reportad"))))
    m.append(macro("Nunidad", sum(1 for e in estudios if not e["unidad_evaluacion"].lower().startswith("no reportad"))))
    for k in METRICAS:
        m.append(macro(f"Nmet{k.replace('_', '').replace('f1', 'Funo')}", sum(1 for e in estudios if e["metricas_flags"][k])))

    # Categorías
    for i, c in enumerate(CATEGORIAS):
        prim = sum(1 for e in estudios if e["categoria_anomalia"] == c)
        cual = sum(1 for e in estudios if c in (e["categoria_anomalia"], e["categoria_anomalia_secundaria"]))
        m.append(macro(f"Ncat{'ABCD'[i]}", prim))
        m.append(macro(f"Pcat{'ABCD'[i]}", pct(prim, n)))
        m.append(macro(f"NcatAny{'ABCD'[i]}", cual))

    # Baselines
    m.append(macro("Nbaselines", sum(1 for e in estudios if e["calidad"]["QA3"]["p"] > 0)))
    m.append(macro("NbaselineNoDL", sum(1 for e in estudios if e["baseline_no_dl"])))
    m.append(macro("NsinBaseline", sum(1 for e in estudios if e["calidad"]["QA3"]["p"] == 0)))

    # Limitaciones
    for k in LIMITACIONES:
        m.append(macro(f"Nlim{k.replace('_', '')}", sum(1 for e in estudios if e["limitaciones_flags"][k])))

    t = {}
    # Tabla de características (longtable)
    filas = []
    for e in estudios:
        ds = "; ".join(d["nombre"] for d in e["datasets"])
        filas.append(" & ".join([
            e["id"], f"\\cite{{{e['bibkey']}}}", str(e["anio"]), esc(e["tipo_dato_corto"]),
            esc(e["entorno"]), esc(e["datasets_corto"]), esc(e["etiqueta_corta"]),
            esc(e["categoria_corta"]), esc(e["modelo_corto"]), esc(e["resultado_corto"]),
        ]) + " \\\\")
    t["caracteristicas"] = "\n".join(filas) + "\n"

    # Calidad por ítem y estudio
    filas = []
    fmt = lambda p: {1: "1", 0.5: "0.5", 0: "0"}[p]
    for e in estudios:
        filas.append(" & ".join([e["id"]] + [fmt(e["calidad"][q]["p"]) for q in QA] + [f"{e['qa_total']:.1f}"]) + " \\\\")
    medias = [f"{statistics.mean(e['calidad'][q]['p'] for e in estudios):.2f}" for q in QA]
    filas.append("\\midrule")
    filas.append(" & ".join(["Media"] + medias + [f"{statistics.mean(tot):.2f}"]) + " \\\\")
    t["calidad"] = "\n".join(filas) + "\n"

    # Cruce tipo de dato x familia
    def cruce(filas_def, titulo, etiqueta, nota):
        cab = ["", *FAM_CORTA.values(), "Total"]
        filas = []
        for nombre, cond in filas_def:
            sub = [e for e in estudios if cond(e)]
            fila = [nombre] + [sum(1 for e in sub if e["familias"][k]) for k in FAMILIAS] + [len(sub)]
            filas.append(fila)
        return tabla(cab, filas, "X" + "c" * (len(FAMILIAS) + 1), titulo, etiqueta, nota)

    dato_lbl = {"series de sensores": "Series de sensores", "movilidad OD/agregada": "Movilidad agregada/OD",
                "trayectorias GPS": "Trayectorias", "video/imágenes": "Video e im\\'{a}genes",
                "multimodal": "Multimodal", "simulado": "Simulado"}
    t["cruce_dato"] = cruce(
        [(dato_lbl[d], (lambda d: lambda e: e["tipo_dato"] == d)(d)) for d in TIPOS_DATO
         if any(e["tipo_dato"] == d for e in estudios)],
        "Cruce tipo de dato $\\times$ familia de arquitectura (n.\\textsuperscript{o} de estudios).",
        "tab:cruce_dato",
        "Un estudio puede usar varias familias, por lo que las filas no suman el total.")
    cat_lbl = {"accidentes/incidentes": "Accidentes e incidentes", "congestión/flujo anómalo": "Congesti\\'{o}n o flujo an\\'{o}malo",
               "trayectorias/conducción peligrosa": "Trayectorias o conducci\\'{o}n peligrosa",
               "disrupciones/eventos extremos/infraestructura": "Disrupciones y eventos extremos"}
    t["cruce_anomalia"] = cruce(
        [(cat_lbl[c], (lambda c: lambda e: e["categoria_anomalia"] == c)(c)) for c in CATEGORIAS],
        "Cruce categor\\'{i}a principal de anomal\\'{i}a $\\times$ familia de arquitectura.",
        "tab:cruce_anomalia",
        "Clasificaci\\'{o}n por categor\\'{i}a principal (una por estudio).")
    periodos = [("2020--2021", lambda e: e["anio"] <= 2021), ("2022--2023", lambda e: 2022 <= e["anio"] <= 2023),
                ("2024--2026", lambda e: e["anio"] >= 2024)]
    t["cruce_anio"] = cruce(periodos, "Cruce periodo de publicaci\\'{o}n $\\times$ familia de arquitectura.",
                            "tab:cruce_anio", "2026 es parcial (b\\'{u}squeda cerrada en la fecha indicada en la Secci\\'{o}n~\\ref{sec:busqueda}).")

    # Macros de las celdas de los cruces (para citarlas en el texto)
    fam_m = {"recurrente": "Rec", "convolucional": "Conv", "autoencoder": "AE", "grafos": "Grafo",
             "transformer_atencion": "Transf", "generativo": "Gen"}
    dato_m = dict(zip(TIPOS_DATO, ["Sensores", "Movilidad", "Trayectorias", "Video", "Multimodal", "Simulado"]))
    cm = []
    for d, dn in dato_m.items():
        for k, kn in fam_m.items():
            cm.append(macro(f"X{dn}{kn}", sum(1 for e in estudios if e["tipo_dato"] == d and e["familias"][k])))
    for nombre, cond in [("Antes", lambda e: e["anio"] <= 2021), ("Medio", lambda e: 2022 <= e["anio"] <= 2023),
                         ("Reciente", lambda e: e["anio"] >= 2024)]:
        sub = [e for e in estudios if cond(e)]
        cm.append(macro(f"Nperiodo{nombre}", len(sub)))
        for k, kn in fam_m.items():
            cm.append(macro(f"X{nombre}{kn}", sum(1 for e in sub if e["familias"][k])))
    noVideoGrafo = sum(1 for e in estudios if e["tipo_dato"] != "video/im\u00e1genes" and e["familias"]["grafos"])
    cm.append(macro("NgrafoNoVideo", noVideoGrafo))
    par = Counter(e["paradigma"] for e in estudios)
    cm.append(macro("Nsupervisado", par.get("supervisado", 0)))
    cm.append(macro("Nnosupervisado", par.get("no supervisado", 0) + par.get("semisupervisado", 0) + par.get("autosupervisado", 0)))
    for k, kn in [("predicci\u00f3n", "Pred"), ("reconstrucci\u00f3n", "Recon"), ("clasificaci\u00f3n", "Clasif")]:
        cm.append(macro(f"Nenfoque{kn}", sum(1 for e in estudios if e["enfoque"] == k)))
    cm.append(macro("NetiqRealesTotal", sum(1 for e in estudios if e["origen_etiquetas"] in ETIQUETAS[:3])))
    cm.append(macro("NetiqNoReales", sum(1 for e in estudios if e["origen_etiquetas"] in ETIQUETAS[3:6])))
    cm.append(macro("NumbralNoAplica", sum(1 for e in estudios if e["umbral"].lower().startswith("no aplica"))))
    cm.append(macro("NumbralExplicito", sum(1 for e in estudios if not e["umbral"].lower().startswith(("no aplica", "no reportad")))))
    alta = [e for e in estudios if e["qa_total"] >= UMBRAL_ALTA]
    cm.append(macro("NaltaEtiqReal", sum(1 for e in alta if e["origen_etiquetas"] in ETIQUETAS[:3])))
    cm.append(macro("NaltaHibrido", sum(1 for e in alta if e["hibrido"])))
    m.extend(cm)

    # Etiquetas
    filas = []
    et_lbl = {"registros reales de incidentes": "Registros reales de incidentes",
              "anotación manual/experta": "Anotaci\\'{o}n manual o experta",
              "benchmark anotado de terceros": "Benchmark anotado por terceros",
              "anomalías inyectadas/sintéticas": "Anomal\\'{i}as inyectadas o sint\\'{e}ticas",
              "mixto": "Mixto o autom\\'{a}tico (pseudo-etiquetas)", "sin etiquetas": "Sin etiquetas", "no reportado": "No reportado"}
    for tlab in ETIQUETAS:
        xs = ids(estudios, lambda e, tlab=tlab: e["origen_etiquetas"] == tlab)
        if xs:
            filas.append([et_lbl[tlab], len(xs), pct(len(xs), n), lista_ids(xs)])
    t["etiquetas"] = tabla(["Origen de las etiquetas", "n", "\\%", "Estudios"], filas, "lccX",
                           "Origen de las etiquetas de anomal\\'{i}a (RQ2, protocolo).", "tab:etiquetas")

    # Métricas
    filas = []
    for k, lbl in METRICAS.items():
        xs = ids(estudios, lambda e, k=k: e["metricas_flags"][k])
        filas.append([lbl, len(xs), pct(len(xs), n), lista_ids(xs)])
    t["metricas"] = tabla(["M\\'{e}trica", "n", "\\%", "Estudios"], filas, "lccX",
                          "M\\'{e}tricas reportadas por los estudios (RQ2).", "tab:metricas",
                          "Un estudio puede reportar varias m\\'{e}tricas.")

    # Protocolo
    def rep(campo):
        return ids(estudios, lambda e: not e[campo].lower().startswith("no reportad"))
    filas = [
        ["Tasa de anomal\\'{i}as en los datos", len(rep("tasa_anomalias")), lista_ids(rep("tasa_anomalias"))],
        ["Unidad de evaluaci\\'{o}n (punto, ventana, frame, evento\\ldots)", len(rep("unidad_evaluacion")), lista_ids(rep("unidad_evaluacion"))],
        ["Criterio de umbral o decisi\\'{o}n", len(rep("umbral")), lista_ids(rep("umbral"))],
        ["Partici\\'{o}n entrenamiento/prueba", len(rep("particion")), lista_ids(rep("particion"))],
    ]
    t["protocolo"] = tabla(["Elemento del protocolo reportado", "n", "Estudios"], filas, "lcX",
                           "Elementos del protocolo de evaluaci\\'{o}n que reporta cada estudio (RQ2).", "tab:protocolo")

    # Categorías
    filas = []
    for c in CATEGORIAS:
        xs = ids(estudios, lambda e, c=c: e["categoria_anomalia"] == c)
        sec = ids(estudios, lambda e, c=c: e["categoria_anomalia_secundaria"] == c)
        filas.append([cat_lbl[c], len(xs), pct(len(xs), n), lista_ids(xs), lista_ids(sec)])
    filas.append("MIDRULE")
    filas.append(["Total", n, "100~\\%", "", ""])
    t["categorias"] = tabla(["Categor\\'{i}a", "n", "\\%", "Estudios (principal)", "Secundaria"], filas, "lccXX",
                            "Categor\\'{i}as de anomal\\'{i}a abordadas (RQ3).", "tab:categorias")

    # Familias
    filas = []
    for k, lbl in FAMILIAS.items():
        xs = ids(estudios, lambda e, k=k: e["familias"][k])
        filas.append([lbl, len(xs), pct(len(xs), n), lista_ids(xs)])
    filas.append("MIDRULE")
    xs = ids(estudios, lambda e: e["hibrido"])
    filas.append(["Combinan dos o m\\'{a}s familias (h\\'{i}bridos)", len(xs), pct(len(xs), n), lista_ids(xs)])
    xs = ids(estudios, lambda e: e["multimodal"])
    filas.append(["Integran varias modalidades de datos (multimodales)", len(xs), pct(len(xs), n), lista_ids(xs)])
    t["familias"] = tabla(["Familia", "n", "\\%", "Estudios"], filas, "lccX",
                          "Familias de arquitectura presentes en los estudios (RQ1).", "tab:familias",
                          "Un estudio puede combinar varias familias. ``H\\'{i}brido'' se refiere a la arquitectura y ``multimodal'' a los datos de entrada.")

    # Datasets / fuentes
    filas = []
    for d in TIPOS_DATO:
        xs = ids(estudios, lambda e, d=d: e["tipo_dato"] == d)
        if xs:
            ejemplos = sorted({x for e in estudios if e["tipo_dato"] == d for x in e["datasets_ejemplo"]})
            filas.append([dato_lbl[d], len(xs), lista_ids(xs), esc(", ".join(ejemplos))])
    t["datos"] = tabla(["Tipo de dato", "n", "Estudios", "Datasets"], filas, "lcXX",
                       "Tipo de dato y conjuntos de datos utilizados (RQ4).", "tab:datos")

    # Baselines
    filas = []
    for e in estudios:
        filas.append([e["id"], esc(e["baselines_corto"]), "S\\'{i}" if e["baseline_no_dl"] else "No", esc(e["ventaja_corta"])])
    t["baselines"] = "\n".join(" & ".join(map(str, f)) + " \\\\" for f in filas) + "\n"

    # Limitaciones
    filas = []
    for k, lbl in LIMITACIONES.items():
        xs = ids(estudios, lambda e, k=k: e["limitaciones_flags"][k])
        filas.append([lbl, len(xs), pct(len(xs), n), lista_ids(xs)])
    sin = ids(estudios, lambda e: not any(e["limitaciones_flags"].values()))
    filas.append(["Sin limitaciones declaradas", len(sin), pct(len(sin), n), lista_ids(sin)])
    t["limitaciones"] = tabla(["Limitaci\\'{o}n declarada por los autores", "n", "\\%", "Estudios"], filas, "lccX",
                              "Limitaciones reportadas por los estudios primarios (RQ5).", "tab:limitaciones",
                              "Un estudio puede declarar varias limitaciones.")

    (SALIDA_TEX / "macros.tex").write_text("% Generado por suplementos/generar_conteos.py. No editar a mano.\n" + "".join(m), encoding="utf-8")

    # Revisiones previas
    prev = json.loads((SUPL / "revisiones_previas.json").read_text(encoding="utf-8"))
    filas = []
    for r in sorted(prev, key=lambda r: r["anio"]):
        clave = r["bibtex"].split("{", 1)[1].split(",", 1)[0]
        aut = [a.split(",")[0].strip() for a in r["autores"].split(";")]
        nombre = f"{aut[0]} y {aut[1]}" if len(aut) == 2 else f"{aut[0]} et al."
        filas.append([f"{esc(nombre)}~\\cite{{{clave}}}", r["anio"], esc(r["tipo_corto"]),
                      esc(r["dato_corto"]), esc(r["vacio_corto"])])
    t["previas"] = tabla(["Revisi\\'{o}n", "A\\~{n}o", "Tipo", "Datos cubiertos", "Vac\\'{i}o respecto a esta RSL"], filas,
                         "lcp{2.2cm}p{2.6cm}Y", "Revisiones previas sobre detecci\\'{o}n de anomal\\'{i}as de tr\\'{a}fico y su diferencia con esta revisi\\'{o}n.",
                         "tab:previas", "Revisiones identificadas mediante b\\'{u}squeda dirigida (2018--2026). Los \\textit{preprints} se indican como tales.")

    # Casos límite (incluidos y excluidos)
    cur = json.loads(CURACION.read_text(encoding="utf-8"))
    filas = []
    for e in estudios:
        if e.get("decision_limite"):
            filas.append(f"{e['id']} \\cite{{{e['bibkey']}}} & Incluido & {esc(e['decision_limite'].split('. ', 1)[1] if e['decision_limite'].startswith('Incluido') else e['decision_limite'])} \\\\")
    for x in cur["excluidos_texto_completo"]:
        filas.append(f"--- \\cite{{{x['bibkey']}}} & Excluido ({x['criterio']}) & {esc(x['motivo'])} \\\\")
    t["limite"] = "\n".join(filas) + "\n"
    m2 = [macro("NexcluidosLimite", len(cur["excluidos_texto_completo"])),
          macro("NincluidosLimite", sum(1 for e in estudios if e.get("decision_limite")))]
    with open(SALIDA_TEX / "macros.tex", "a", encoding="utf-8") as f:
        f.write("".join(m2))

    # Lista de estudios (anexo)
    filas = []
    for e in estudios:
        filas.append(" & ".join([e["id"], e["id_version_anterior"], f"\\cite{{{e['bibkey']}}}",
                                 esc(e["primer_autor"]) + " et al.", str(e["anio"]), esc(e["editorial"]),
                                 f"\\url{{{e['doi']}}}" if e["doi"].startswith("10.") else esc("Sin DOI (actas IFAAMAS)"),
                                 f"\\BaseRecup{{{e['id']}}}"]) + " \\\\")
    t["lista_estudios"] = "\n".join(filas) + "\n"

    for nombre, contenido in t.items():
        (SALIDA_TEX / f"{nombre}.tex").write_text("% Generado por suplementos/generar_conteos.py. No editar a mano.\n" + contenido, encoding="utf-8")
    return t


def exportar_xlsx(estudios):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment
    wb = Workbook()
    ws = wb.active
    ws.title = "Matriz"
    cols = ["id", "id_version_anterior", "bibkey", "autores", "anio", "titulo", "venue", "doi", "base_recuperacion",
            "entorno", "tipo_dato", "tipo_dato_detalle", "pais_region_datos", "origen_etiquetas", "origen_etiquetas_detalle",
            "tasa_anomalias", "paradigma", "enfoque", "unidad_evaluacion", "umbral", "particion",
            "familia_principal", "hibrido", "multimodal", "arquitectura", "metricas", "resultado_principal",
            "baselines", "baseline_no_dl", "ventaja_vs_mejor_baseline", "categoria_anomalia",
            "categoria_anomalia_secundaria", "limitaciones_autores", "codigo_disponible", "caso_limite", "qa_total"]
    ws.append(cols + [f"fam_{k}" for k in FAMILIAS] + [f"met_{k}" for k in METRICAS] + [f"lim_{k}" for k in LIMITACIONES])
    for e in estudios:
        fila = []
        for c in cols:
            v = e.get(c, "")
            if isinstance(v, list):
                v = "; ".join(x if isinstance(x, str) else x.get("nombre", "") for x in v)
            fila.append(v)
        fila += [int(e["familias"][k]) for k in FAMILIAS] + [int(e["metricas_flags"][k]) for k in METRICAS] + \
                [int(e["limitaciones_flags"][k]) for k in LIMITACIONES]
        ws.append(fila)
    ws2 = wb.create_sheet("Datasets")
    ws2.append(["id", "dataset", "tipo", "publico"])
    for e in estudios:
        for d in e["datasets"]:
            ws2.append([e["id"], d["nombre"], d["tipo"], d["publico"]])
    ws3 = wb.create_sheet("Calidad")
    ws3.append(["id"] + [f"{q} puntaje" for q in QA] + ["total"] + [f"{q} evidencia" for q in QA])
    for e in estudios:
        ws3.append([e["id"]] + [e["calidad"][q]["p"] for q in QA] + [e["qa_total"]] + [e["calidad"][q]["ev"] for q in QA])
    for w in (ws, ws2, ws3):
        for c in w[1]:
            c.font = Font(bold=True)
        w.freeze_panes = "B2"
        for col in w.columns:
            for c in col[1:]:
                c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(SALIDA_XLSX)


if __name__ == "__main__":
    SALIDA_TEX.mkdir(parents=True, exist_ok=True)
    est = cargar()
    generar(est)
    exportar_xlsx(est)
    print(f"{len(est)} estudios procesados; salidas en {SALIDA_TEX} y {SALIDA_XLSX}")
