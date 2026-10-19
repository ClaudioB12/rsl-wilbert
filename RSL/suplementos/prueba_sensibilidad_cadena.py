#!/usr/bin/env python3
"""Prueba de sensibilidad de la cadena base sobre los estudios incluidos.

Comprueba si el título, el resumen y las palabras clave de cada estudio incluido
satisfacen los tres bloques de la cadena base (A AND B AND C). Es una aproximación
local: el texto se toma de la primera página del PDF (antes de la Introducción).
Un estudio que no satisface la cadena indica que no habría sido recuperado por la
búsqueda en bases de datos y debe declararse en la rama «otros métodos» de PRISMA.

Uso: python3 suplementos/prueba_sensibilidad_cadena.py
     (lee los PDF de «Articulos evaluados por calidad/» con pdftotext y escribe
      manuscrito/generado/sensibilidad.tex con las cifras que cita el manuscrito)
"""
import json
import re
import unicodedata
import subprocess
from pathlib import Path

# Bloques de la cadena v2.1 (ver cadenas_busqueda.txt). Los comodines (*) se traducen a \w*.
BLOQUES = {
    "A": [r"\banomal\w*", r"\babnormal\w*", r"outlier detection", r"incident detection", r"accident detection",
          r"accident (prediction|anticipation)", r"road closure\w*", r"dangerous driving", r"near[- ]accident\w*",
          r"near[- ]miss\w*", r"extreme events?"],
    "B": [r"deep learning", r"deep neural", r"neural networks?", r"\blstm", r"\bgru\b", r"\bcnns?\b",
          r"convolutional", r"autoencoders?", r"transformers?", r"graph neural", r"self-attention",
          r"attention mechanism"],
    "C": [r"(road|urban|vehicular|highway|freeway|expressway) traffic", r"traffic flows?", r"traffic speed",
          r"traffic volumes?", r"traffic data", r"traffic monitoring", r"traffic videos?", r"traffic surveillance",
          r"traffic cameras?", r"traffic scenes?", r"traffic scenarios?", r"traffic events?", r"traffic incidents?",
          r"traffic accidents?", r"traffic anomal\w*", r"traffic congestion", r"road accidents?", r"road closures?",
          r"intelligent transportation", r"transportation networks?", r"road networks?", r"vehicle trajector\w*",
          r"vehicle behavio\w*", r"driving behavio\w*", r"\btaxi\w*"],
}


def cabecera(texto):
    """Título + resumen + palabras clave: todo lo previo a la Introducción."""
    corte = re.search(r"\n\s*(1\.?\s*|I\.\s*)?introduction\b", texto, re.I)
    return texto[: corte.start()] if corte else texto[:6000]


RAIZ = Path(__file__).resolve().parent.parent


def texto_pdf(pdf):
    return subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout


def main():
    estudios = json.loads((RAIZ / "suplementos" / "matriz_extraccion.json").read_text(encoding="utf-8"))
    fallos = []
    for e in estudios:
        t = unicodedata.normalize("NFKC", texto_pdf(RAIZ / "Articulos evaluados por calidad" / e["pdf"]))  # ligaduras: ﬃ → ffi
        t = re.sub(r"-\s*\n\s*", "", t)
        t = re.sub(r"\s+", " ", cabecera(t)).lower()
        res = {b: [p for p in pats if re.search(p, t)] for b, pats in BLOQUES.items()}
        ok = all(res.values())
        print(f"{e['id']}  {'OK ' if ok else 'NO '}  " + "  ".join(f"{b}:{len(v)}" for b, v in res.items()))
        if not ok:
            fallos.append((e["id"], [b for b, v in res.items() if not v]))
    n_ok = len(estudios) - len(fallos)
    print(f"\nRecuperados por la cadena base: {n_ok}/{len(estudios)}")
    for i, b in fallos:
        print(f"  {i}: no satisface el bloque {', '.join(b)}")
    salida = RAIZ / "manuscrito" / "generado" / "sensibilidad.tex"
    salida.write_text("% Generado por suplementos/prueba_sensibilidad_cadena.py. No editar a mano.\n"
                      f"\\newcommand{{\\NsensibOK}}{{{n_ok}}}\n"
                      f"\\newcommand{{\\IDsensibNo}}{{{', '.join(i for i, _ in fallos) or '---'}}}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
