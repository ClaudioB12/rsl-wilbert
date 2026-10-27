#!/usr/bin/env python3
"""PASO 8. Prepara los archivos para subir a Overleaf.

Uso (desde la carpeta RSL):   python cribado/scripts/08_paquete_overleaf.py
Salidas en cribado/salida/:
  overleaf_proyecto_completo.zip   para crear el proyecto la PRIMERA vez (Nuevo proyecto > Subir proyecto)
  overleaf_actualizar.zip          solo los archivos que generan los scripts (datos_busqueda.tex y generado/);
                                   descomprimir y subirlos a Overleaf reemplazando los existentes
"""
import zipfile

from comun import MANUSCRITO, SALIDA, asegurar_utf8_consola

FUENTES = ["RSL_v3.tex", "RSL_v3_suplemento.tex", "referencias.bib", "estudios.bib", "datos_busqueda.tex"]


def main():
    asegurar_utf8_consola()
    SALIDA.mkdir(parents=True, exist_ok=True)
    generados = sorted((MANUSCRITO / "generado").glob("*.tex"))
    with zipfile.ZipFile(SALIDA / "overleaf_proyecto_completo.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in FUENTES:
            z.write(MANUSCRITO / f, f)
        for g in generados:
            z.write(g, f"generado/{g.name}")
    with zipfile.ZipFile(SALIDA / "overleaf_actualizar.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.write(MANUSCRITO / "datos_busqueda.tex", "datos_busqueda.tex")
        for g in generados:
            z.write(g, f"generado/{g.name}")
    print(f"Listo:\n  {SALIDA / 'overleaf_proyecto_completo.zip'}\n  {SALIDA / 'overleaf_actualizar.zip'}")
    print("En Overleaf NO editen datos_busqueda.tex ni la carpeta generado/: se reemplazan con cada actualización.")


if __name__ == "__main__":
    main()
