#!/usr/bin/env python3
"""PASO 13. Descarga los PDF de acceso abierto de los estudios que pasaron el título y resumen.

Usa el enlace al texto completo gratuito que encontró 11_acceso_abierto.py (y, si falla, el DOI).
Guarda cada PDF como cribado/pdf/<ID>.pdf y comprueba que de verdad sea un PDF (algunas editoriales
devuelven una página web o un captcha). Los que no se puedan bajar quedan en una lista con su enlace
para descargarlos a mano desde el navegador.

Uso (desde la carpeta RSL):   python cribado/scripts/13_descargar_pdfs.py
Se puede ejecutar varias veces: no vuelve a bajar los PDF que ya están.
Salida: cribado/salida/13_pdf_a_mano.csv  (los que faltan, con el enlace y el nombre con que guardarlos)
"""
import sys
import time
import urllib.error
import urllib.request

from comun import CRIBADO, SALIDA, asegurar_utf8_consola, cargar_json, escribir_csv, leer_csv

CARPETA = CRIBADO / "pdf"
CABECERAS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/124.0 Safari/537.36", "Accept": "application/pdf,*/*;q=0.8"}


def candidatos(r):
    """Enlaces a probar, del más directo al menos directo."""
    enl, doi = r.get("enlace_texto_completo", ""), r.get("doi", "")
    out = [enl] if enl else []
    if "arxiv.org/abs/" in enl:
        out.insert(0, enl.replace("/abs/", "/pdf/"))
    if "mdpi.com" in enl and not enl.rstrip("/").endswith("pdf"):
        out.insert(0, enl.rstrip("/") + "/pdf")
    if doi:
        out.append(f"https://doi.org/{doi}")
    return list(dict.fromkeys(out))


def bajar(url):
    req = urllib.request.Request(url, headers=CABECERAS)
    with urllib.request.urlopen(req, timeout=60) as resp:
        datos = resp.read()
    return datos if datos[:5] == b"%PDF-" else None


def main():
    asegurar_utf8_consola()
    decision = cargar_json(SALIDA / "decision_TA.json")
    if not decision:
        sys.exit("Primero cierra la etapa de título y resumen: 04_cerrar_etapa.py --etapa TA")
    oa = SALIDA / "11_acceso_abierto.csv"
    if not oa.exists():
        sys.exit("Falta salida/11_acceso_abierto.csv: ejecuta antes 11_acceso_abierto.py")
    filas = [r for r in leer_csv(oa) if decision.get(r["id"], {}).get("decision") == "Incluir"]
    CARPETA.mkdir(parents=True, exist_ok=True)
    ya, nuevos, a_mano = 0, 0, []
    for n, r in enumerate(filas, 1):
        destino = CARPETA / f"{r['id']}.pdf"
        if destino.exists() and destino.stat().st_size > 1000:
            ya += 1
            continue
        pdf = None
        for url in candidatos(r):
            try:
                pdf = bajar(url)
            except (urllib.error.URLError, TimeoutError, OSError):
                pdf = None
            if pdf:
                break
            time.sleep(1)
        if pdf:
            destino.write_bytes(pdf)
            nuevos += 1
            print(f"[{n}/{len(filas)}] {r['id']} descargado")
        else:
            a_mano.append({**r, "guardar_como": f"cribado\\pdf\\{r['id']}.pdf",
                           "enlace": r.get("enlace_texto_completo") or f"https://doi.org/{r['doi']}"})
            print(f"[{n}/{len(filas)}] {r['id']} → a mano")
    escribir_csv(SALIDA / "13_pdf_a_mano.csv", a_mano, ["id", "guardar_como", "enlace", "titulo", "doi"])
    print(f"\nPDF que ya estaban: {ya}. Descargados ahora: {nuevos}. Faltan (bajar a mano): {len(a_mano)}.")
    if a_mano:
        print("Abre cribado\\salida\\13_pdf_a_mano.csv: entra a cada enlace, descarga el PDF y guárdalo con el nombre "
              "de la columna «guardar_como». Luego vuelve a ejecutar este script para comprobar que no falte ninguno.")


if __name__ == "__main__":
    main()
