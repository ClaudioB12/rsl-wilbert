# Pendientes para los autores (versión 2 de la RSL)

> **Paso a paso detallado: `RSL/cribado/README.md`** (búsqueda, Parsif.al, cribado con scripts, PRISMA, calidad y Overleaf). **Criterios de cribado con su fundamento: `RSL/cribado/MANUAL_CRIBADO.md`.** Los scripts escriben solos las fechas, los conteos PRISMA y los kappa en `datos_busqueda.tex`.

Lo que sigue solo pueden hacerlo ustedes. En el PDF, cada dato pendiente aparece **en rojo y entre corchetes**. Casi todos se completan en un único archivo: `RSL/manuscrito/datos_busqueda.tex`.

## 1. Re-ejecutar la búsqueda (Obs. 3, 7)
- Ejecutar las cadenas de `RSL/suplementos/cadenas_busqueda.txt` en Scopus, Web of Science, IEEE Xplore, ScienceDirect y ACM DL.
- Anotar, por base, la **fecha** y el **número de registros**, y exportar los resultados (RIS o BibTeX) a Parsif.al.
- Rellenar `\NScopus`, `\FScopus`, etc., y `\FechaBusqueda` en `datos_busqueda.tex`.
- Comprobar que los 21 estudios incluidos aparecen. Anotar la base de cada uno en `\BaseRecup` (Anexo B). S03 y S14 solo aparecen buscando en texto completo, por eso van en la rama «otros métodos».
- **E23 (Giasemis y Sopasakis):** la planilla de Parsif.al enlaza un documento de IEEE Xplore (n.º 11171552). Si es una versión revisada por pares y la búsqueda en IEEE Xplore la recupera, el estudio debe reincorporarse citando esa versión (avísenme y regenero todo).

## 2. Re-cribar con dos revisores (Obs. 6)
- Cribado independiente por título y resumen, y después por texto completo, con dos revisores; un tercero resuelve los desacuerdos.
- Calcular el kappa de Cohen en cada etapa y en la evaluación de calidad (`\KappaTA`, `\KappaTC`, `\KappaCalidad`).
- Registrar el motivo de cada exclusión a texto completo (CE-2 a CE-6, CI-6) y completar el flujo PRISMA (`\Pidentificados` … `\PexclCEseis`).
- Si en realidad el cribado lo hizo una sola persona, **no lo oculten**: cambien el texto de §3.5 y añádanlo a las amenazas (§5.4).

## 3. Verificar la evaluación de calidad y la extracción
- La matriz (`RSL/suplementos/matriz_extraccion.xlsx`) y la puntuación de calidad se prellenaron leyendo cada PDF, con la evidencia de cada puntaje en la hoja «Calidad». **Dos de ustedes deben revisarla de forma independiente**, porque así se declara en el método.
- Si cambian un valor, edítenlo en `RSL/suplementos/extraccion_individual/<clave>.json` (o en `curacion.json`) y ejecuten:
  ```
  cd RSL
  python3 suplementos/generar_conteos.py
  python3 suplementos/prueba_sensibilidad_cadena.py
  cd manuscrito && pdflatex RSL_v2 && bibtex RSL_v2 && pdflatex RSL_v2 && pdflatex RSL_v2
  ```
  Todas las cifras del texto se actualizan solas.

## 4. Registro, declaraciones y autoría (Obs. 14, 16)
- Registrar el protocolo en OSF (osf.io → Registrations) y poner el DOI en `\RegistroOSF`.
- Completar las fechas del historial del protocolo (Anexo A, Tabla «Historial»).
- Completar el **correo institucional del tercer autor** y confirmar su nombre exacto. La versión 1 usaba «Ender Prieto Quispe», «Prieto Quispe, J. E.» y el correo `juan.prieto`.
- Completar la **declaración de uso de IA generativa** (Declaraciones). En esta revisión se usó un asistente de IA para verificar la extracción contra los PDF, redactar y generar los scripts; decláralo según la política de la revista.
- **Repositorio de datos:** la disponibilidad de datos apunta a este repositorio. **No lo hagan público con los PDF de los artículos** (`RSL/Articulos evaluados por calidad/`), porque tienen derechos de autor. Publiquen solo `RSL/suplementos/` y el manuscrito, por ejemplo en OSF o en un repositorio aparte, y actualicen `\RepositorioDatos`.

## 5. Verificaciones bibliográficas que no pude cerrar sin acceso a las editoriales
- Cai et al. 2021 (SIGSPATIAL): pp. 354–364 se tomaron de la v1; el PDF no imprime la paginación.
- Chakraborty et al. 2023 (AAMAS): sin DOI. Confirmen la URL `ifaamas.org/Proceedings/aamas2023/pdfs/p1125.pdf`.
- Zhang et al. 2020 (IEEE Trans. Big Data, revisión previa): volumen y páginas tomados de citas secundarias.
