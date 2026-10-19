"""Funciones comunes del flujo de cribado (lectura de exportaciones, normalización, Excel).

No se ejecuta directamente: lo usan los scripts 01_ a 08_.
"""
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ_RSL = Path(__file__).resolve().parents[2]          # carpeta RSL
CRIBADO = RAIZ_RSL / "cribado"
EXPORTACIONES = CRIBADO / "exportaciones"
SALIDA = CRIBADO / "salida"
REVISION = CRIBADO / "revision"                          # hojas que llenan los revisores
MANUSCRITO = RAIZ_RSL / "manuscrito"
SUPLEMENTOS = RAIZ_RSL / "suplementos"

# Orden de prioridad para atribuir un registro duplicado a una base (y nombres de carpeta).
BASES = ["Scopus", "WoS", "IEEE", "ScienceDirect", "ACM"]
NOMBRE_BASE = {"Scopus": "Scopus", "WoS": "Web of Science", "IEEE": "IEEE Xplore",
               "ScienceDirect": "ScienceDirect", "ACM": "ACM Digital Library"}

DECISIONES_TA = ["Incluir", "Duda", "Excluir"]
DECISIONES_TC = ["Incluir", "Excluir"]
# Criterios de exclusión válidos (ver MANUAL_CRIBADO.md). El orden es el del árbol de decisión.
CRITERIOS = ["CE-1", "CE-5", "CI-3", "CI-2", "CE-2", "CE-3", "CE-4", "CI-6", "CE-6"]
CRITERIOS_TA = ["CE-1", "CE-5", "CI-3", "CI-2", "CE-2", "CE-3", "CE-4"]
DESCRIPCION_CRITERIO = {
    "CE-1": "Duplicado o versión menos completa del mismo estudio",
    "CE-5": "Revisión, survey, capítulo, tesis, resumen, póster, editorial o preprint sin versión revisada",
    "CI-3": "Fuera del periodo 2020-2026",
    "CI-2": "Idioma distinto de inglés o español",
    "CE-2": "No trata de tráfico vehicular por carretera",
    "CE-3": "No evalúa detección de anomalías (solo pronóstico, clasificación general, riesgo a largo plazo)",
    "CE-4": "La detección no se basa en Deep Learning",
    "CI-6": "Sin evaluación cuantitativa de la tarea de detección",
    "CE-6": "Información insuficiente sobre modelo, datos o resultados",
}


def asegurar_utf8_consola():
    """Evita errores de codificación al imprimir en la consola de Windows."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# ---------------------------------------------------------------- normalización
def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def normalizar_titulo(t):
    t = sin_tildes(unicodedata.normalize("NFKC", t or "")).lower()
    t = re.sub(r"<[^>]+>", " ", t)          # etiquetas HTML (<i>, <sub>...)
    t = re.sub(r"[{}\\$]", "", t)            # restos de LaTeX
    return re.sub(r"[^a-z0-9]+", "", t)


def normalizar_doi(d):
    d = (d or "").strip().lower()
    d = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", d)
    d = re.sub(r"^doi:\s*", "", d)
    return d.rstrip(".")


def anio(v):
    m = re.search(r"(19|20)\d{2}", str(v or ""))
    return int(m.group(0)) if m else None


def limpiar(s):
    s = unicodedata.normalize("NFKC", str(s or ""))
    s = re.sub(r"[{}]", "", s)
    s = s.replace("\\&", "&").replace("\\%", "%").replace("\\_", "_")
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------- lectura de archivos
def leer_texto(ruta):
    datos = Path(ruta).read_bytes()
    for enc in ("utf-8-sig", "utf-16", "cp1252", "latin-1"):
        try:
            texto = datos.decode(enc)
            if enc == "utf-16" and "\x00" in texto[:200]:
                continue
            return texto
        except UnicodeDecodeError:
            continue
    return datos.decode("latin-1", errors="replace")


def _registro(base, archivo, **kw):
    r = {"base": base, "archivo": Path(archivo).name, "titulo": "", "autores": "", "anio": None,
         "fuente": "", "doi": "", "resumen": "", "palabras_clave": "", "tipo_doc": "", "idioma": "", "url": ""}
    for k, v in kw.items():
        r[k] = anio(v) if k == "anio" else limpiar(v)
    return r


def leer_ris(ruta, base):
    regs, actual = [], None
    for linea in leer_texto(ruta).splitlines():
        m = re.match(r"^([A-Z][A-Z0-9])  -\s?(.*)$", linea)
        if not m:
            if actual is not None and actual.get("_ult") and linea.strip():
                actual[actual["_ult"]].append(linea.strip())
            continue
        tag, val = m.group(1), m.group(2).strip()
        if tag == "TY":
            actual = {"TY": [val]}
            continue
        if actual is None:
            continue
        if tag == "ER":
            regs.append(actual)
            actual = None
            continue
        actual.setdefault(tag, []).append(val)
        actual["_ult"] = tag
    out = []
    for r in regs:
        g = lambda *tags, sep="; ": sep.join(v for t in tags for v in r.get(t, []) if v)
        tipo = {"JOUR": "Article", "JFULL": "Article", "EJOUR": "Article", "CONF": "Conference Paper",
                "CPAPER": "Conference Paper", "CHAP": "Book Chapter", "BOOK": "Book", "THES": "Thesis",
                "RPRT": "Report", "GEN": "Generic", "UNPB": "Preprint"}.get(g("TY"), g("TY"))
        out.append(_registro(base, ruta, titulo=g("TI", "T1", sep=" "), autores=g("AU", "A1", "A2"),
                             anio=g("PY", "Y1", "DA"), fuente=g("T2", "JO", "JF", "BT", "SO", sep=" | "),
                             doi=g("DO"), resumen=g("AB", "N2", sep=" "), palabras_clave=g("KW"),
                             tipo_doc=tipo, idioma=g("LA"), url=g("UR")))
    return out


def _campos_bibtex(cuerpo):
    campos, i, n = {}, 0, len(cuerpo)
    while i < n:
        m = re.compile(r"\s*,?\s*([A-Za-z][\w-]*)\s*=\s*").match(cuerpo, i)
        if not m:
            break
        nombre, i = m.group(1).lower(), m.end()
        if i < n and cuerpo[i] == "{":
            prof, j = 0, i
            while j < n:
                if cuerpo[j] == "{":
                    prof += 1
                elif cuerpo[j] == "}":
                    prof -= 1
                    if prof == 0:
                        break
                j += 1
            campos[nombre], i = cuerpo[i + 1:j], j + 1
        elif i < n and cuerpo[i] == '"':
            j = cuerpo.find('"', i + 1)
            campos[nombre], i = cuerpo[i + 1:j], j + 1
        else:
            m2 = re.compile(r"[^,}\s]+").match(cuerpo, i)
            campos[nombre], i = (m2.group(0), m2.end()) if m2 else ("", i + 1)
    return campos


def leer_bibtex(ruta, base):
    texto, out = leer_texto(ruta), []
    for m in re.finditer(r"@(\w+)\s*\{", texto):
        tipo = m.group(1).lower()
        if tipo in ("comment", "preamble", "string"):
            continue
        prof, j = 1, m.end()
        while j < len(texto) and prof:
            prof += {"{": 1, "}": -1}.get(texto[j], 0)
            j += 1
        cuerpo = texto[m.end():j - 1]
        cuerpo = cuerpo.split(",", 1)[1] if "," in cuerpo else ""
        c = _campos_bibtex(cuerpo)
        tipo_doc = {"article": "Article", "inproceedings": "Conference Paper", "conference": "Conference Paper",
                    "incollection": "Book Chapter", "inbook": "Book Chapter", "book": "Book",
                    "phdthesis": "Thesis", "mastersthesis": "Thesis", "misc": "Misc",
                    "techreport": "Report", "unpublished": "Preprint"}.get(tipo, tipo)
        out.append(_registro(base, ruta, titulo=c.get("title", ""),
                             autores=c.get("author", "").replace(" and ", "; "), anio=c.get("year", ""),
                             fuente=c.get("journal") or c.get("booktitle") or c.get("publisher", ""),
                             doi=c.get("doi", ""), resumen=c.get("abstract", ""),
                             palabras_clave=c.get("keywords", "") or c.get("author_keywords", ""),
                             tipo_doc=c.get("type") or c.get("document_type") or tipo_doc,
                             idioma=c.get("language", ""), url=c.get("url", "")))
    return out


def _col(fila, *nombres):
    for n in nombres:
        for k in fila:
            if k and k.strip().lower() == n.lower():
                return fila[k] or ""
    return ""


def leer_tabla(ruta, base):
    """CSV de Scopus/IEEE/ScienceDirect, o texto delimitado por tabuladores de Web of Science."""
    texto = leer_texto(ruta)
    primera = texto.splitlines()[0] if texto else ""
    delim = "\t" if primera.count("\t") > primera.count(",") else ","
    filas = list(csv.DictReader(texto.splitlines(), delimiter=delim))
    out = []
    for f in filas:
        if delim == "\t" and "TI" in f:          # Web of Science (etiquetas de 2 letras)
            out.append(_registro(base, ruta, titulo=f.get("TI", ""), autores=f.get("AU", ""), anio=f.get("PY", ""),
                                 fuente=f.get("SO", ""), doi=f.get("DI", ""), resumen=f.get("AB", ""),
                                 palabras_clave="; ".join(x for x in (f.get("DE", ""), f.get("ID", "")) if x),
                                 tipo_doc=f.get("DT", ""), idioma=f.get("LA", "")))
            continue
        out.append(_registro(base, ruta,
                             titulo=_col(f, "Title", "Document Title", "Article Title"),
                             autores=_col(f, "Authors", "Author full names", "Author"),
                             anio=_col(f, "Year", "Publication Year"),
                             fuente=_col(f, "Source title", "Publication Title", "Source Title", "Journal"),
                             doi=_col(f, "DOI"),
                             resumen=_col(f, "Abstract"),
                             palabras_clave="; ".join(x for x in (_col(f, "Author Keywords"), _col(f, "Index Keywords", "IEEE Terms")) if x),
                             tipo_doc=_col(f, "Document Type", "Document Identifier", "Publication Type"),
                             idioma=_col(f, "Language of Original Document", "Language"),
                             url=_col(f, "Link", "PDF Link", "URL")))
    return out


def leer_exportacion(ruta, base):
    ext = Path(ruta).suffix.lower()
    if ext in (".ris", ".nbib"):
        return leer_ris(ruta, base)
    if ext in (".bib", ".bibtex"):
        return leer_bibtex(ruta, base)
    if ext in (".csv", ".tsv"):
        return leer_tabla(ruta, base)
    if ext == ".txt":
        texto = leer_texto(ruta)
        if re.search(r"^TY  - ", texto, re.M):
            return leer_ris(ruta, base)
        if texto.lstrip().startswith("@"):
            return leer_bibtex(ruta, base)
        return leer_tabla(ruta, base)
    return []


# ---------------------------------------------------------------- señales de apoyo al cribado
RE_ANOMALIA = re.compile(r"anomal|abnormal|outlier|incident|accident|crash|collision|road closure|dangerous driving|"
                         r"near[- ]?(miss|accident)|extreme event|disruption|wrong[- ]way|congestion detection|unusual event", re.I)
RE_DL = re.compile(r"deep learning|deep neural|neural network|\blstm|\bgru\b|\bcnns?\b|convolutional|autoencoder|"
                   r"transformer|graph neural|\bgnn|\bgcn|attention|\bgan\b|generative adversarial|variational|"
                   r"\byolo|resnet|diffusion model|recurrent", re.I)
RE_PRONOSTICO = re.compile(r"forecast|prediction of traffic|traffic prediction|flow prediction|speed prediction", re.I)
RE_NO_VIAL = re.compile(r"network traffic|internet traffic|intrusion|cyber|packet|ddos|botnet|malware|"
                        r"\bcan[- ]bus|in-vehicle network|pedestrian crowd|crowd anomal|maritime|vessel|\bship|\bais\b|"
                        r"aircraft|aviation|flight|railway|rail transit|\bmetro\b|subway|pothole|pavement (crack|distress)|"
                        r"drowsiness|driver fatigue|driver distraction", re.I)
RE_REVISION = re.compile(r"\b(survey|review|overview|state[- ]of[- ]the[- ]art|systematic|bibliometric|tutorial)\b", re.I)


def senales(r):
    """Avisos automáticos para ayudar al revisor. NO deciden la inclusión."""
    texto = " ".join([r["titulo"], r["resumen"], r["palabras_clave"]])
    s = []
    tipo = (r["tipo_doc"] or "").lower()
    if any(x in tipo for x in ("review", "survey", "chapter", "book", "thesis", "editorial", "erratum", "note", "letter", "preprint")) \
            or RE_REVISION.search(r["titulo"]) or "arxiv" in (r["fuente"] or "").lower():
        s.append("CE-5? (revisión/tipo de documento)")
    if r["anio"] and not (2020 <= r["anio"] <= 2026):
        s.append(f"CI-3? (año {r['anio']})")
    if r["idioma"] and not re.search(r"english|ingl|spanish|espa|^en$|^es$", r["idioma"], re.I):
        s.append(f"CI-2? (idioma {r['idioma']})")
    if RE_NO_VIAL.search(texto):
        s.append("CE-2? (posible dominio no vial: " + RE_NO_VIAL.search(texto).group(0) + ")")
    if not RE_ANOMALIA.search(texto):
        s.append("CE-3? (sin términos de anomalía/incidente" + ("; parece pronóstico" if RE_PRONOSTICO.search(texto) else "") + ")")
    if not RE_DL.search(texto):
        s.append("CE-4? (sin términos de Deep Learning)")
    if not r["resumen"]:
        s.append("SIN RESUMEN: buscar en la web antes de decidir")
    return " | ".join(s)


# ---------------------------------------------------------------- utilidades de tablas
def escribir_csv(ruta, filas, campos):
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        for r in filas:
            w.writerow(r)


def leer_csv(ruta):
    with open(ruta, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def kappa_cohen(pares):
    """Kappa de Cohen para una lista de pares (r1, r2) de categorías."""
    pares = [(a, b) for a, b in pares if a and b]
    n = len(pares)
    if n == 0:
        return None, 0, None
    cats = sorted({x for p in pares for x in p})
    po = sum(1 for a, b in pares if a == b) / n
    pe = sum((sum(1 for a, _ in pares if a == c) / n) * (sum(1 for _, b in pares if b == c) / n) for c in cats)
    k = 1.0 if pe == 1 else (po - pe) / (1 - pe)
    return k, n, po


def interpretar_kappa(k):
    if k is None:
        return "sin datos"
    return ("pobre" if k <= 0.20 else "débil" if k <= 0.40 else "moderado" if k <= 0.60
            else "bueno" if k <= 0.80 else "muy bueno")


def guardar_json(ruta, datos):
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    Path(ruta).write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")


def cargar_json(ruta, defecto=None):
    p = Path(ruta)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else defecto
