"""Creación y lectura de las hojas Excel del cribado (un solo revisor, con sugerencias del asistente)."""
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

from comun import CRITERIOS, CRITERIOS_TA, DESCRIPCION_CRITERIO

AZUL = PatternFill("solid", fgColor="00467F")
VERDE_OSC = PatternFill("solid", fgColor="375623")
GRIS = PatternFill("solid", fgColor="F2F2F2")
AMARILLO = PatternFill("solid", fgColor="FFF2CC")
ROJO = PatternFill("solid", fgColor="F8CBAD")
VERDE = PatternFill("solid", fgColor="E2EFDA")
BLANCO_NEGRITA = Font(bold=True, color="FFFFFF")
AJUSTE = Alignment(wrap_text=True, vertical="top")

COL_DECISION = "DECISIÓN"
COL_CRITERIO = "CRITERIO (si excluye)"
COL_EVIDENCIA = "EVIDENCIA (cita textual + página o sección)"
COL_TEXTO = "Texto completo"

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


def crear_hoja(ruta, etapa, registros, columnas, prefill=None, titulo_avance="Wilbert A. Mayta Arotaype"):
    """Crea la hoja de cribado.

    columnas: lista de (encabezado, ancho, clave_en_registro | None). Las columnas de decisión
    (DECISIÓN, CRITERIO, Comentario y, en TC, Texto completo y EVIDENCIA) se agregan al final.
    prefill: {id: {encabezado: valor}} para prellenar celdas.
    """
    prefill = prefill or {}
    es_tc = etapa == "TC"
    wb = Workbook()
    ws = wb.active
    ws.title = "Cribado"
    decision_cols = ([(COL_TEXTO, 13)] if es_tc else []) + [(COL_DECISION, 11), (COL_CRITERIO, 12)] + \
                    ([(COL_EVIDENCIA, 45)] if es_tc else []) + [("Comentario", 30)]
    cab = [c[0] for c in columnas] + [c[0] for c in decision_cols]
    anchos = [c[1] for c in columnas] + [c[1] for c in decision_cols]
    ws.append(cab)
    for i, (c, ancho) in enumerate(zip(ws[1], anchos), 1):
        c.fill = VERDE_OSC if c.value in dict(decision_cols) else AZUL
        c.font, c.alignment = BLANCO_NEGRITA, Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[c.column_letter].width = ancho
    ws.row_dimensions[1].height = 36
    for r in registros:
        fila = [r.get(clave, "") if clave else "" for _, _, clave in columnas] + [None] * len(decision_cols)
        for enc, val in prefill.get(r["id"], {}).items():
            if enc in cab:
                fila[cab.index(enc)] = val
        ws.append(fila)
    n = len(registros) + 1
    alto = 30 if es_tc else 105
    for fila in ws.iter_rows(min_row=2, max_row=n):
        for c in fila:
            c.alignment = AJUSTE
        ws.row_dimensions[fila[0].row].height = alto
    L = lambda nombre: ws.cell(row=1, column=cab.index(nombre) + 1).column_letter
    _lista(ws, f"{L(COL_DECISION)}2:{L(COL_DECISION)}{n}", ["Incluir", "Excluir"] if es_tc else ["Incluir", "Duda", "Excluir"])
    _lista(ws, f"{L(COL_CRITERIO)}2:{L(COL_CRITERIO)}{n}", CRITERIOS if es_tc else CRITERIOS_TA)
    if es_tc:
        _lista(ws, f"{L(COL_TEXTO)}2:{L(COL_TEXTO)}{n}", ["Sí", "No recuperado"])
        ws.conditional_formatting.add(f"{L(COL_EVIDENCIA)}2:{L(COL_EVIDENCIA)}{n}",
                                      FormulaRule(formula=[f'AND(${L(COL_DECISION)}2="Excluir",{L(COL_EVIDENCIA)}2="")'], fill=AMARILLO))
    ws.conditional_formatting.add(f"{L(COL_CRITERIO)}2:{L(COL_CRITERIO)}{n}",
                                  FormulaRule(formula=[f'AND(${L(COL_DECISION)}2="Excluir",{L(COL_CRITERIO)}2="")'], fill=ROJO))
    ws.conditional_formatting.add(f"{L(COL_DECISION)}2:{L(COL_DECISION)}{n}",
                                  FormulaRule(formula=[f'{L(COL_DECISION)}2=""'], fill=AMARILLO))
    if "SUGERENCIA" in cab:
        s = L("SUGERENCIA")
        ws.conditional_formatting.add(f"{s}2:{s}{n}", FormulaRule(formula=[f'LEFT({s}2,7)="Excluir"'], fill=ROJO))
        ws.conditional_formatting.add(f"{s}2:{s}{n}", FormulaRule(formula=[f'LEFT({s}2,8)="Probable"'], fill=VERDE))
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:{ws.cell(row=1, column=len(cab)).column_letter}{n}"

    av = wb.create_sheet("Avance", 0)
    av.column_dimensions["A"].width = 36
    av.column_dimensions["B"].width = 90
    D, C = L(COL_DECISION), L(COL_CRITERIO)
    datos = [("Revisor", titulo_avance),
             ("Etapa", {"TA": "Título y resumen", "TC": "Texto completo", "retest": "Re-cribado (fiabilidad)"}[etapa]),
             ("Registros en la hoja", n - 1),
             ("Decididos", f"=COUNTA(Cribado!{D}2:{D}{n})"),
             ("Faltan", "=B4-B5"),
             ("Incluir", f'=COUNTIF(Cribado!{D}2:{D}{n},"Incluir")'),
             ("Duda", f'=COUNTIF(Cribado!{D}2:{D}{n},"Duda")'),
             ("Excluir", f'=COUNTIF(Cribado!{D}2:{D}{n},"Excluir")'),
             ("Excluir SIN criterio (debe ser 0)", f'=COUNTIFS(Cribado!{D}2:{D}{n},"Excluir",Cribado!{C}2:{C}{n},"")')]
    for a, b in datos:
        av.append([a, b])
        av.cell(row=av.max_row, column=1).font = Font(bold=True)
    av.append([])
    av.append(["Cómo trabajar", "Filtra la columna SUGERENCIA (flecha del encabezado). Empieza por «Excluir (regla)»: "
                                "verifica cada uno leyendo el título y, si estás de acuerdo, deja la decisión prellenada. "
                                "Luego «Probable incluir» y al final «Revisar». La SUGERENCIA es solo una ayuda: la decisión es tuya. "
                                "Lee la hoja «Criterios» y el MANUAL_CRIBADO.md."])
    av.cell(row=av.max_row, column=2).alignment = AJUSTE
    _hoja_criterios(wb, "TC" if es_tc else "TA")
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    wb.save(ruta)


def leer_hoja(ruta):
    """Devuelve {id: {encabezado: valor}} y añade claves normalizadas: decision, criterio, evidencia, etc."""
    wb = load_workbook(ruta, data_only=True)
    ws = wb["Cribado"]
    cab = [c.value for c in ws[1]]
    out = {}
    for fila in ws.iter_rows(min_row=2, values_only=True):
        if not fila or not fila[0]:
            continue
        d = {cab[i]: ("" if v is None else str(v).strip()) for i, v in enumerate(fila) if i < len(cab) and cab[i]}
        d.update({"decision": d.get(COL_DECISION, ""), "criterio": d.get(COL_CRITERIO, ""),
                  "comentario": d.get("Comentario", ""), "texto_completo": d.get(COL_TEXTO, ""),
                  "evidencia": d.get(COL_EVIDENCIA, ""), "sugerencia": d.get("SUGERENCIA", "")})
        out[str(fila[0]).strip()] = d
    return out
