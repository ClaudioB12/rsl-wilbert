#!/usr/bin/env python3
"""Construye el corpus final de la revisión (suplementos/corpus.json) a partir de la lectura a texto
completo del autor (cribado/salida/15_extraccion_TC.json, que viene de REVISION_TEXTO_COMPLETO.xlsx).

Cada estudio incluido recibe:
  - un ID definitivo S01…Snn (ordenado por año y primer autor) y su ID de cribado (Rxxxx);
  - una clave BibTeX (se reutiliza la de referencias.bib si el estudio ya estaba citado) y su entrada
    BibTeX, tomada de la exportación de la base (manuscrito/estudios.bib);
  - los campos que usa generar_conteos.py (familias, métricas, limitaciones, etiquetas…), derivados de
    la hoja de extracción; los textos originales del autor se conservan en los campos *_detalle.

Uso (desde la carpeta RSL):   python suplementos/construir_corpus.py
Luego:  python suplementos/generar_conteos.py  y  python cribado/scripts/06_resultados_prisma.py
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "cribado" / "scripts"))
from comun import _campos_bibtex, leer_csv, normalizar_doi, normalizar_titulo  # noqa: E402

SALIDA = RAIZ / "cribado" / "salida"
SUPL = RAIZ / "suplementos"
MANUS = RAIZ / "manuscrito"


def s(t):
    t = unicodedata.normalize("NFKD", str(t or ""))
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


# Metadatos que faltan en la transcripción del listado de ACM (pendiente la exportación oficial): tomados del PDF.
METADATOS = {
    "R1010": {"tipo": "inproceedings", "author": "Nallapula and others", "fuente": "Proceedings of the 2025 14th International "
              "Conference on Software and Computer Applications (ICSCA 2025)", "pages": "67--71", "publisher": "ACM"},
    "R0360": {"tipo": "article", "fuente": "ACM Transactions on Spatial Algorithms and Systems", "publisher": "ACM"},
    "R0025": {"tipo": "inproceedings", "fuente": "ACM conference proceedings (verificar en el PDF)", "publisher": "ACM"},
}


def apellido(nombre):
    """«Shen, Guojiang» → Shen; «Guojiang Shen» → Shen."""
    nombre = nombre.strip()
    return nombre.split(",")[0].strip() if "," in nombre else (nombre.split()[-1] if nombre.split() else nombre)


def corto(t, n=60):
    t = re.sub(r"\s+", " ", str(t or "")).strip()
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip(",;:") + "…"


TIPO = {"Sensores/detectores": "series de sensores", "Movilidad agregada": "movilidad OD/agregada",
        "Trayectorias GPS": "trayectorias GPS", "Video": "video/imágenes", "Multimodal": "multimodal"}
TIPO_CORTO = {"Sensores/detectores": "Sensores", "Movilidad agregada": "Movilidad agregada",
              "Trayectorias GPS": "Trayectorias", "Video": "Video/imágenes", "Multimodal": "Multimodal"}
ENTORNO = {"Urbano": "urbano", "Autopista": "autopista", "Ambos": "ambos", "No reportado": "no especificado"}
CATEGORIA = {"Accidentes/incidentes": "accidentes/incidentes", "Congestión atípica": "congestión/flujo anómalo",
             "Trayectoria anómala": "trayectorias/conducción peligrosa",
             "Comportamiento de conducción": "trayectorias/conducción peligrosa",
             "Fallo de sensor/datos": "disrupciones/eventos extremos/infraestructura",
             "Evento/otro": "disrupciones/eventos extremos/infraestructura"}
CATEGORIA_CORTA = {"Accidentes/incidentes": "Accidentes e incidentes", "Congestión atípica": "Congestión atípica",
                   "Trayectoria anómala": "Trayectoria anómala", "Comportamiento de conducción": "Conducción peligrosa",
                   "Fallo de sensor/datos": "Fallo de sensor", "Evento/otro": "Evento u otro"}
PARADIGMA = {"Supervisado": "supervisado", "Semi-supervisado": "semisupervisado",
             "No supervisado": "no supervisado", "Auto-supervisado": "autosupervisado"}
FAM_PRINCIPAL = {"Recurrente (RNN/LSTM/GRU)": "recurrente", "Convolucional (CNN)": "convolucional",
                 "Grafos (GNN)": "grafos", "Atención/Transformer": "transformer_atencion",
                 "Autoencoder/VAE": "autoencoder", "Generativo (GAN/difusión)": "generativo", "Otra": "otra"}
# Benchmarks públicos anotados por terceros (videos de accidentes, trayectorias y sensores de referencia).
BENCHMARKS = r"ccd|car ?crash|dota|dada|ucf-?crime|cadp|ai ?city|uit-?adrone|xd-?violence|shanghaitech|street ?scene|" \
             r"traffic-?net|a3d|\bdad\b|tads|drone-?anomaly|ft-?aed|maad|vtad|4m-?tad|hwid"
PUBLICOS = BENCHMARKS + r"|pems|metr-?la|ngsim|highd|porto|nyc|new york|argoverse|comma\.?ai|i-?880|uah|geolife|didi|" \
                        r"chengdu|xi.?an|kaggle|github|i-?24|trafficam|rad\b"


def etiquetas(x):
    o = x["Origen de etiquetas"]
    if o == "Anotación manual" and re.search(BENCHMARKS, s(x["Datasets (nombre, país)"])):
        return "benchmark anotado de terceros", "Benchmark anotado"
    return {"Reales/registros": ("registros reales de incidentes", "Registros reales"),
            "Anotación manual": ("anotación manual/experta", "Anotación manual"),
            "Inyectadas/sintéticas": ("anomalías inyectadas/sintéticas", "Inyectadas o sintéticas"),
            "Pseudo-etiquetas": ("mixto", "Pseudo-etiquetas"),
            "Sin etiquetas": ("sin etiquetas", "Sin etiquetas"),
            "No reportado": ("no reportado", "No reportado")}[o]


def familias(x, original=""):
    """Familias presentes, según el texto original del autor (columna «Familia DL principal») y la arquitectura.
    Se descartan las frases negativas («No integra CNN…»)."""
    t = s(original + ". " + x["Familia DL principal"] + ". " + x["Arquitectura (nombre)"])
    t = t.replace("autoencoder/vae", "autoencoder")  # nombre de la opción de la lista, no implica VAE
    t = " ".join(f for f in re.split(r"[.;]\s+", t) if not re.search(r"\b(no|ni|sin|aunque|prescinde)\b", f))
    f = {"recurrente": bool(re.search(r"\blstm|\bbi-?lstm|\bgru\b|\brnn\b|recurrent|seq2seq|sequence-to-sequence|convlstm", t)),
         "convolucional": bool(re.search(r"\bcnn|-cnn|convolu|\byolo|resnet|vgg|efficientnet|mobilenet|\btcn\b|\bi3d|\bc3d|"
                                         r"\br3d|densenet|\bfcos|faster r-cnn|u-?net|inception|darknet", t)),
         "autoencoder": bool(re.search(r"autoencoder|auto-encoder|\bvae\b|\bae\b", t)),
         "grafos": bool(re.search(r"\bgnn|\bgcn|\bgat\b|\bgraph|\bgrafo|hgnn|mgtgcn|\bgae\b", t)),
         "transformer_atencion": bool(re.search(r"transformer|\batencion|attention|\bvit\b|\bswin|\bclip\b|long-clip|llama|"
                                                r"informer|multi-?head|multicabez|q-former", t)),
         "generativo": bool(re.search(r"\bgan\b|\bgans\b|bigan|adversari|difusion|diffusion|\bvae\b|variational|variacional", t))}
    p = FAM_PRINCIPAL[x["Familia DL principal"]]
    if p in f:
        f[p] = True
    return f, p


def textos_originales():
    """Texto original de la columna «Familia DL principal» (guardado como comentario al normalizar el Excel)."""
    from openpyxl import load_workbook
    ruta = RAIZ / "cribado" / "revision" / "REVISION_TEXTO_COMPLETO.xlsx"
    ws = load_workbook(ruta)["2_Extraccion"]
    j = [c.value for c in ws[1]].index("Familia DL principal") + 1
    out = {}
    for r in range(3, ws.max_row + 1):
        c = ws.cell(row=r, column=j)
        out[ws.cell(row=r, column=1).value] = c.comment.text.replace("Texto original:\n", "") if c.comment else ""
    return out


def metricas(x):
    t = s(x["Métricas de detección"] + " " + x["Resultado principal"])
    f = {"accuracy": "accuracy" in t or "exactitud" in t,
         "precision": bool(re.search(r"precision(?!-recall)|precisio", t)) and "average precision" not in t,
         "recall": bool(re.search(r"recall|sensibilidad|sensitivity", t)),
         "f1": bool(re.search(r"\bf1|f-?score|f-?measure", t)),
         "auc_roc": bool(re.search(r"auc|roc", t)) and not re.search(r"pr-?auc|auprc", t.replace("auc-roc", "")),
         "pr_auc": bool(re.search(r"pr-?auc|auprc|average precision|\bap\b|precision-recall", t)),
         "dr": bool(re.search(r"\bdr\b|detection rate|tasa de deteccion", t)),
         "far_fpr": bool(re.search(r"\bfar\b|\bfpr\b|false alarm|falsas alarmas|false positive rate", t)),
         "mttd": bool(re.search(r"mttd|time to detect|tiempo (medio )?de deteccion|mtta|time-to-accident", t)),
         "error_mae_rmse_mape": bool(re.search(r"\bmae\b|rmse|mape|\bmse\b", t)),
         "iou_map": bool(re.search(r"\biou\b|\bmap\b|map50|map@", t)),
         "operativas_latencia_fps_energia": bool(re.search(r"latencia|latency|fps|inferencia|energ|ms\b", t))}
    if re.search(r"auc-roc|roc-auc|auroc", t):
        f["auc_roc"] = True
    lista = [m.strip() for m in re.split(r"[;,]", x["Métricas de detección"]) if m.strip()][:10]
    return f, lista


def limitaciones(x):
    t = s(x["Limitaciones que reportan"])
    if re.match(r"\s*no report", t):
        return {k: False for k in ("datos_replicabilidad", "etiquetado", "generalizacion", "metricas_no_uniformes",
                                   "costo_despliegue", "interpretabilidad")}
    return {"datos_replicabilidad": bool(re.search(r"datos? propios|privad|no (son )?public|acceso|tamano|pocos datos|"
                                                   r"escasez|insuficien|muestra|dataset limitado|cantidad de datos", t)),
            "etiquetado": bool(re.search(r"etiquet|anotac|label|ground truth", t)),
            "generalizacion": bool(re.search(r"generaliz|otros escenarios|otras ciudades|un solo|unico|transfer|dominio|"
                                             r"diversidad|escenarios reales|simulad|condiciones", t)),
            "metricas_no_uniformes": bool(re.search(r"metric", t)),
            "costo_despliegue": bool(re.search(r"costo|coste|computacion|computacional|tiempo real|latencia|hardware|"
                                               r"despliegue|recursos|eficiencia|memoria", t)),
            "interpretabilidad": bool(re.search(r"interpret|explicab", t))}


def umbral(x):
    t = s(x["Criterio de umbral"])
    if re.match(r"\s*no report", t):
        return "No reportado"
    explicito = re.search(r"percentil|umbral fijo|umbral (adaptativ|dinamic|aprendid)|μ|sigma|\bk ?=|supera|>|≥|"
                          r"carta de control|threshold|τ|0[.,]\d", t)
    if not explicito and re.search(r"softmax|clasificador|argmax|sin umbral|no se especifica|clasificacion", t):
        return "No aplica (decisión del clasificador): " + x["Criterio de umbral"]
    return x["Criterio de umbral"]


def enfoque(x):
    t = s(x["Criterio de umbral"] + " " + x["Arquitectura (nombre)"] + " " + x["Paradigma"])
    if re.search(r"reconstru", t):
        return "reconstrucción"
    if re.search(r"predic|pronost|forecast", t) and x["Paradigma"] != "Supervisado":
        return "predicción"
    return "clasificación"


def datasets(x):
    out = []
    for parte in re.split(r";|\s\+\s", x["Datasets (nombre, país)"]):
        nombre = parte.strip(" .")
        if not nombre:
            continue
        t = s(nombre)
        tipo = "simulado" if re.search(r"simul|carla|sumo|vissim|sintet|juguete", t) else "real"
        publico = "sí" if re.search(PUBLICOS, t) and not re.search(r"propio|privad", t) else "no"
        out.append({"nombre": nombre, "tipo": tipo, "publico": publico})
    return out or [{"nombre": "No reportado", "tipo": "real", "publico": "no reportado"}]


def ejemplo(nombre):
    n = re.split(r"\s[\(\[:,—–-]\s?|:", nombre)[0].strip()
    return corto(n, 28)


def codigo(texto):
    """URL del código de los autores; los enlaces que solo llevan a datos o a librerías de terceros no cuentan."""
    m = re.search(r"https?://\S+", texto or "")
    if not m:
        return texto or "No"
    url = m.group(0).rstrip(".,;)")
    if re.search(r"kaggle|dataset|dataport|10\.21227|dot\.ca\.gov|ankitshah009|ultralytics", url.lower()):
        return f"No (el enlace es de datos o de una librería de terceros: {url})"
    return url


def bibtex_por_id():
    """Entradas BibTeX de las exportaciones (campo note «ID cribado Rxxxx»)."""
    out = {}
    for ruta in (SALIDA / "parsifal").glob("*.bib"):
        texto = ruta.read_text(encoding="utf-8")
        for m in re.finditer(r"@(\w+)\s*\{\s*[^,]*,(.*?)\n\}", texto, re.S):
            campos = _campos_bibtex(m.group(2))
            i = re.search(r"ID cribado (R\d+)", campos.get("note", ""))
            if i:
                out[i.group(1)] = (m.group(1).lower(), campos)
    return out


def clave(primer_autor, anio, titulo, usadas):
    vacias = {"a", "an", "the", "on", "of", "for", "and", "in", "with", "based", "using", "via", "to", "by"}
    pal = next((w for w in re.findall(r"[a-z0-9]+", s(titulo)) if w not in vacias), "estudio")
    base = f"{re.sub(r'[^a-z]', '', s(primer_autor)) or 'anon'}{anio}{pal}"
    k, n = base, 1
    while k in usadas:
        n += 1
        k = f"{base}{chr(96 + n)}"
    usadas.add(k)
    return k


def main():
    ext = json.loads((SALIDA / "15_extraccion_TC.json").read_text(encoding="utf-8"))
    reg = {r["id"]: r for r in leer_csv(SALIDA / "02_registros_unicos.csv")}
    bib = bibtex_por_id()
    # Corpus de la versión anterior (curación + fichas), para reutilizar sus claves BibTeX ya citadas.
    cur = json.loads((SUPL / "curacion.json").read_text(encoding="utf-8"))
    previo = []
    for c in cur["incluidos"]:
        f = json.loads((SUPL / "extraccion_individual" / f"{c['clave_extraccion']}.json").read_text(encoding="utf-8"))
        previo.append({"doi": f.get("doi", ""), "titulo": f["titulo"], "bibkey": c["bibkey"]})
    previo_doi = {normalizar_doi(e.get("doi", "")): e for e in previo if normalizar_doi(e.get("doi", ""))}
    previo_tit = {normalizar_titulo(e["titulo"]): e for e in previo}
    refs = (MANUS / "referencias.bib").read_text(encoding="utf-8")
    usadas = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", refs))

    orig_fam = textos_originales()
    filas = []
    for rid, e in ext.items():
        r, x = reg[rid], e["extraccion"]
        autores = [a.strip() for a in re.split(r";| and ", r["autores"]) if a.strip()]
        meta = METADATOS.get(rid, {})
        if not autores and meta.get("author"):
            autores = [a.strip() for a in meta["author"].split(" and ")]
        primer = apellido(autores[0]) if autores else "Anónimo"
        filas.append((int(r["anio"]), s(primer), rid, primer, autores))
    filas.sort()

    corpus, entradas_bib = [], []
    for n, (anio, _, rid, primer, autores) in enumerate(filas, 1):
        r, e = dict(reg[rid]), ext[rid]
        meta = METADATOS.get(rid, {})
        r["fuente"] = r["fuente"] or meta.get("fuente", "")
        x = e["extraccion"]
        ant = previo_doi.get(normalizar_doi(r["doi"])) or previo_tit.get(normalizar_titulo(r["titulo"]))
        if ant:
            bibkey = ant["bibkey"]
        else:
            bibkey = clave(primer, anio, r["titulo"], usadas)
            tipo, campos = bib.get(rid, ("article", {}))
            tipo = meta.get("tipo", "inproceedings" if tipo == "misc" else tipo)
            campos = {k: v for k, v in campos.items() if k not in ("note", "abstract", "keywords", "file", "url")}
            campos.setdefault("title", r["titulo"])
            if not campos.get("author"):
                campos["author"] = " and ".join(autores)
            for k in ("pages", "publisher"):
                if meta.get(k):
                    campos.setdefault(k, meta[k])
            campos.setdefault("year", str(anio))
            if r["doi"] and "doi" not in campos:
                campos["doi"] = normalizar_doi(r["doi"])
            if r["fuente"] and not any(k in campos for k in ("journal", "booktitle")):
                campos["journal" if tipo == "article" else "booktitle"] = r["fuente"]
            entradas_bib.append(f"@{tipo}{{{bibkey},\n" + ",\n".join(f"  {k} = {{{v}}}" for k, v in campos.items()) + "\n}\n")
        f, fam_p = familias(x, orig_fam.get(rid, ""))
        mf, ml = metricas(x)
        et, et_corta = etiquetas(x)
        ds = datasets(x)
        cal = {q: {"p": float(v["p"]), "ev": v["ev"]} for q, v in e["calidad"].items()}
        corpus.append({
            "id": f"S{n:02d}", "id_version_anterior": rid, "bibkey": bibkey,
            "autores": ", ".join(apellido(a) for a in autores) or "No reportado", "primer_autor": primer,
            "anio": anio, "titulo": r["titulo"], "venue": r["fuente"] or "No reportado",
            "editorial": corto(r["fuente"], 40) or "No reportado", "tipo_doc": r["tipo_doc"],
            "doi": normalizar_doi(r["doi"]) or "No reportado",
            "entorno": ENTORNO[x["Entorno"]], "tipo_dato": TIPO[x["Tipo de dato"]],
            "tipo_dato_detalle": x["Tipo de dato"], "tipo_dato_corto": TIPO_CORTO[x["Tipo de dato"]],
            "pais_region_datos": x["Datasets (nombre, país)"], "datasets": ds,
            "datasets_corto": corto(x["Datasets (nombre, país)"], 45),
            "datasets_ejemplo": sorted({ejemplo(d["nombre"]) for d in ds})[:3],
            "origen_etiquetas": et, "origen_etiquetas_detalle": x["Origen de etiquetas"], "etiqueta_corta": et_corta,
            "tasa_anomalias": x["Tasa de anomalías"], "paradigma": PARADIGMA[x["Paradigma"]], "enfoque": enfoque(x),
            "unidad_evaluacion": x["Unidad de evaluación"], "umbral": umbral(x), "particion": x["Partición"],
            "familia_principal": fam_p, "familias": f, "hibrido": x["¿Híbrido?"] == "Sí",
            "multimodal": x["Tipo de dato"] == "Multimodal", "arquitectura": x["Arquitectura (nombre)"],
            "modelo_corto": corto(re.split(r"[;:.]\s", x["Arquitectura (nombre)"])[0], 45),
            "metricas": ml, "metricas_flags": mf, "resultado_principal": x["Resultado principal"],
            "resultado_corto": corto(x["Resultado principal"], 55),
            "baselines": [b.strip() for b in re.split(r"[,;]", re.sub(r"^\s*\d+\s*:", "", x["Líneas base (cuántas y cuáles)"]))
                          if b.strip()][:12],
            "baselines_corto": corto(x["Líneas base (cuántas y cuáles)"], 60),
            "baseline_no_dl": x["¿Línea base no DL?"] == "Sí",
            "ventaja_vs_mejor_baseline": x["Ventaja vs. mejor línea base"],
            "ventaja_corta": corto(x["Ventaja vs. mejor línea base"], 50),
            "limitaciones_autores": x["Limitaciones que reportan"], "limitaciones_flags": limitaciones(x),
            "codigo_disponible": codigo(x["Código público (URL)"]),
            "categoria_anomalia": CATEGORIA[x["Categoría de anomalía"]], "categoria_anomalia_secundaria": "",
            "categoria_corta": CATEGORIA_CORTA[x["Categoría de anomalía"]],
            "calidad": cal, "caso_limite": "", "decision_limite": "",
            "notas": e["nota"], "evidencia_inclusion": e["evidencia"],
        })
    (SUPL / "corpus.json").write_text(json.dumps(corpus, ensure_ascii=False, indent=1), encoding="utf-8")
    (MANUS / "estudios.bib").write_text("% Generado por suplementos/construir_corpus.py (estudios incluidos sin entrada previa).\n\n"
                                        + "\n".join(entradas_bib), encoding="utf-8")
    print(f"Corpus: {len(corpus)} estudios (S01-S{len(corpus):02d}); {len(entradas_bib)} entradas nuevas en manuscrito/estudios.bib.")


if __name__ == "__main__":
    main()
