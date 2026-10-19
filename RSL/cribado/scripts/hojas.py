"""Creación y lectura de las hojas Excel que llenan los revisores."""
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

from comun import CRITERIOS, CRITERIOS_TA, DESCRIPCION_CRITERIO

AZUL = PatternFill("solid", fgColor="00467F")
GRIS = PatternFill("solid", fgColor="F2F2F2")
AMARILLO = PatternFill("solid", fgColor="FFF2CC")
ROJO = PatternFill("solid", fgColor="F8CBAD")
BLANCO_NEGRITA = Font(bold=True, color="FFFFFF")
AJUSTE = Alignment(wrap_text=True, vertical="top")

ARBOL_TA = [
    ("1", "¿Es el mismo estudio que otro registro (duplicado o versión menos completa)?", "Sí → Excluir, CE-1"),
    ("2", "¿Es revisión/survey, capítulo, tesis, resumen, póster, editorial o preprint?", "Sí → Excluir, CE-5"),
    ("3", "¿Publicado fuera de 2020-2026?", "Sí → Excluir, CI-3"),
    ("4", "¿Idioma distinto de inglés o español?", "Sí → Excluir, CI-2"),
    ("5", "¿El objeto NO es el tráfico vehicular por carretera (urbano o autopista)?", "Sí → Excluir, CE-2"),
    ("6", "¿NO trata la detección/anticipación de anomalías del tráfico (solo pronóstico, clasificación general, riesgo a largo plazo)?", "Sí → Excluir, CE-3"),
    ("7", "¿La detección claramente NO usa Deep Learning?", "Sí → Excluir, CE-4"),
    ("8", "Si pasó todo, o si no se puede saber con el título y resumen:", "Incluir (o Duda). Ante la duda, NO excluir."),
]
ARBOL_TC = ARBOL_TA[:7] + [
    ("8", "¿El texto completo no evalúa cuantitativamente la DETECCIÓN (solo pronóstico, reconocimiento de acciones o figuras cualitativas)?", "Sí → Excluir, CI-6"),
    ("9", "¿No describe modelo, datos o resultados lo suficiente para extraerlos?", "Sí → Excluir, CE-6"),
    ("10", "Si pasó todo:", "Incluir"),
]


def _cabecera(ws, columnas):
    ws.append([c for c, _ in columnas])
    for i, (c, ancho) in enumerate(columnas, 1):
        celda = ws.cell(row=1, column=i)
        celda.fill, celda.font, celda.alignment = AZUL, BLANCO_NEGRITA, Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[celda.column_letter].width = ancho
    ws.row_dimensions[1].height = 34
    ws.freeze_panes = "C2"


def _lista(ws, rango, valores):
    dv = DataValidation(type="list", formula1='"' + ",".join(valores) + '"', allow_blank=True,
                        showErrorMessage=True, errorTitle="Valor no válido",
                        error="Elige un valor de la lista desplegable.")
    ws.add_data_validation(dv)
    dv.add(rango)


def _hoja_criterios(wb, etapa):
    ws = wb.create_sheet("Criterios")
    ws.column_dimensions["A"].width = 6
    ws.column_dimensions["B"].width = 95
    ws.column_dimensions["C"].width = 40
    ws.append(["Paso", "Pregunta (aplicar en este orden; la PRIMERA que se cumpla da el criterio)", "Decisión"])
    for c in ws[1]:
        c.fill, c.font = AZUL, BLANCO_NEGRITA
    for fila in (ARBOL_TC if etapa == "TC" else ARBOL_TA):
        ws.append(list(fila))
    ws.append([])
    ws.append(["", "Códigos de criterio", ""])
    ws.cell(row=ws.max_row, column=2).font = Font(bold=True)
    for c in (CRITERIOS if etapa == "TC" else CRITERIOS_TA):
        ws.append([c, DESCRIPCION_CRITERIO[c], ""])
    ws.append([])
    ws.append(["", "Definiciones completas y ejemplos: cribado/MANUAL_CRIBADO.md", ""])
    for fila in ws.iter_rows(min_row=2):
        for c in fila:
            c.alignment = AJUSTE


def crear_hoja_revisor(ruta, revisor, etapa, registros, previas=None):
    """etapa: 'piloto', 'TA' o 'TC'. previas: {id: (decision, criterio, comentario)} para prellenar."""
    previas = previas or {}
    wb = Workbook()
    ws = wb.active
    ws.title = "Cribado"
    es_tc = etapa == "TC"
    cols = [("ID", 8), ("Título", 45)]
    if es_tc:
        cols += [("Autores", 22), ("Año", 6), ("Fuente", 22), ("DOI / enlace", 24),
                 ("Texto completo", 13), ("DECISIÓN", 11), ("CRITERIO (si excluye)", 12),
                 ("EVIDENCIA (cita textual + página o sección)", 45), ("Comentario", 30)]
    else:
        cols += [("Resumen", 80), ("Palabras clave", 22), ("Año", 6), ("Fuente", 20), ("Tipo doc.", 12),
                 ("Señales automáticas (solo apoyo, NO deciden)", 26), ("DECISIÓN", 11),
                 ("CRITERIO (si excluye)", 12), ("Comentario", 30)]
    _cabecera(ws, cols)
    nombres = [c for c, _ in cols]
    i_dec = nombres.index("DECISIÓN") + 1
    i_cri = nombres.index("CRITERIO (si excluye)") + 1
    for r in registros:
        if es_tc:
            fila = [r["id"], r["titulo"], r["autores"], r["anio"], r["fuente"],
                    f"https://doi.org/{r['doi']}" if r.get("doi") else r.get("url", ""), None, None, None, None, None]
        else:
            fila = [r["id"], r["titulo"], r["resumen"], r["palabras_clave"], r["anio"], r["fuente"],
                    r["tipo_doc"], r["senales"], None, None, None]
        if r["id"] in previas:
            d, c, com = previas[r["id"]]
            fila[i_dec - 1], fila[i_cri - 1], fila[-1] = d or None, c or None, com or None
        ws.append(fila)
    n = len(registros) + 1
    for fila in ws.iter_rows(min_row=2, max_row=n):
        for c in fila:
            c.alignment = AJUSTE
        ws.row_dimensions[fila[0].row].height = 30 if es_tc else 110
    L = lambda i: ws.cell(row=1, column=i).column_letter
    _lista(ws, f"{L(i_dec)}2:{L(i_dec)}{n}", ["Incluir", "Excluir"] if es_tc else ["Incluir", "Duda", "Excluir"])
    _lista(ws, f"{L(i_cri)}2:{L(i_cri)}{n}", CRITERIOS if es_tc else CRITERIOS_TA)
    if es_tc:
        i_tc = nombres.index("Texto completo") + 1
        i_ev = nombres.index("EVIDENCIA (cita textual + página o sección)") + 1
        _lista(ws, f"{L(i_tc)}2:{L(i_tc)}{n}", ["Sí", "No recuperado"])
        ws.conditional_formatting.add(f"{L(i_ev)}2:{L(i_ev)}{n}",
                                      FormulaRule(formula=[f'AND(${L(i_dec)}2="Excluir",{L(i_ev)}2="")'], fill=AMARILLO))
    ws.conditional_formatting.add(f"{L(i_cri)}2:{L(i_cri)}{n}",
                                  FormulaRule(formula=[f'AND(${L(i_dec)}2="Excluir",{L(i_cri)}2="")'], fill=ROJO))
    for i in (i_dec, i_cri):
        for fila in ws.iter_rows(min_row=2, max_row=n, min_col=i, max_col=i):
            fila[0].fill = AMARILLO if fila[0].value is None else PatternFill()
    # Hoja de avance
    av = wb.create_sheet("Avance", 0)
    av.column_dimensions["A"].width = 34
    av.column_dimensions["B"].width = 20
    datos = [("Revisor", revisor), ("Etapa", {"piloto": "Piloto (calibración)", "TA": "Título y resumen",
                                               "TC": "Texto completo"}[etapa]),
             ("Registros en la hoja", n - 1),
             ("Decididos", f"=COUNTA(Cribado!{L(i_dec)}2:{L(i_dec)}{n})"),
             ("Faltan", f"=B4-B5"),
             ("Incluir", f'=COUNTIF(Cribado!{L(i_dec)}2:{L(i_dec)}{n},"Incluir")'),
             ("Duda", f'=COUNTIF(Cribado!{L(i_dec)}2:{L(i_dec)}{n},"Duda")'),
             ("Excluir", f'=COUNTIF(Cribado!{L(i_dec)}2:{L(i_dec)}{n},"Excluir")'),
             ("Excluir SIN criterio (debe ser 0)", f'=COUNTIFS(Cribado!{L(i_dec)}2:{L(i_dec)}{n},"Excluir",Cribado!{L(i_cri)}2:{L(i_cri)}{n},"")')]
    for a, b in datos:
        av.append([a, b])
    for c in av["A"]:
        c.font = Font(bold=True)
    av.append([])
    av.append(["IMPORTANTE", "Trabaja SOLO en esta hoja, sin mirar la del otro revisor. No cambies el nombre del archivo, "
                             "ni el orden o los nombres de las columnas. Lee la hoja «Criterios» antes de empezar."])
    av.cell(row=av.max_row, column=2).alignment = AJUSTE
    av.column_dimensions["B"].width = 90
    _hoja_criterios(wb, "TC" if es_tc else "TA")
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    wb.save(ruta)


def leer_hoja_revisor(ruta):
    """Devuelve {id: {'decision', 'criterio', 'comentario', 'texto_completo', 'evidencia'}}."""
    wb = load_workbook(ruta, data_only=True)
    ws = wb["Cribado"]
    cab = [c.value for c in ws[1]]
    idx = {nombre: i for i, nombre in enumerate(cab)}
    out = {}
    for fila in ws.iter_rows(min_row=2, values_only=True):
        if not fila or not fila[0]:
            continue
        g = lambda nombre: (str(fila[idx[nombre]]).strip() if nombre in idx and fila[idx[nombre]] is not None else "")
        out[str(fila[0]).strip()] = {
            "decision": g("DECISIÓN"), "criterio": g("CRITERIO (si excluye)"), "comentario": g("Comentario"),
            "texto_completo": g("Texto completo"), "evidencia": g("EVIDENCIA (cita textual + página o sección)")}
    return out
