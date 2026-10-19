# Pendientes (versión 2 de la RSL, autor único)

> **Paso a paso detallado: `RSL/cribado/README.md`** (búsqueda, Parsif.al, cribado con scripts, PRISMA, calidad y Overleaf). **Criterios de cribado con su fundamento: `RSL/cribado/MANUAL_CRIBADO.md`.** Los scripts escriben solos las fechas, los conteos PRISMA y los kappa en `datos_busqueda.tex`.

Lo que sigue solo puedes hacerlo tú. En el PDF, cada dato pendiente aparece **en rojo y entre corchetes**. Casi todos se completan en un único archivo: `RSL/manuscrito/datos_busqueda.tex`.

## 1. Re-ejecutar la búsqueda (Obs. 3, 7)
- Ejecutar las cadenas de `RSL/suplementos/cadenas_busqueda.txt` en Scopus, Web of Science, IEEE Xplore, ScienceDirect y ACM DL.
- Anotar, por base, la **fecha** y el **número de registros**, y exportar los resultados (RIS o BibTeX) a Parsif.al.
- Rellenar `\NScopus`, `\FScopus`, etc., y `\FechaBusqueda` en `datos_busqueda.tex`.
- Comprobar que los 21 estudios incluidos aparecen. Anotar la base de cada uno en `\BaseRecup` (Anexo B). S03 y S14 solo aparecen buscando en texto completo, por eso van en la rama «otros métodos».
- **E23 (Giasemis y Sopasakis):** la planilla de Parsif.al enlaza un documento de IEEE Xplore (n.º 11171552). Si es una versión revisada por pares y la búsqueda en IEEE Xplore la recupera, el estudio debe reincorporarse citando esa versión (avísenme y regenero todo).

## 2. Cribado asistido y fiabilidad (Obs. 6)
- Cribado por título y resumen y a texto completo con el asistente (scripts 03, 04, 05 y 05b). Cada exclusión a texto completo lleva su cita.
- Re-cribado ciego de una muestra, al menos 7 días después de cada etapa (script 04b), para el kappa intra-revisor.
- El manuscrito ya declara la revisión de autor único y sus medidas de mitigación (§3.5 y §5.4).

## 3. Verificar la evaluación de calidad y la extracción
- La matriz (`RSL/suplementos/matriz_extraccion.xlsx`) y los puntajes de calidad se prellenaron leyendo cada PDF (con asistencia de IA), con la evidencia de cada dato. **Debes verificarlos tú** (script 07, Parte 7 de la guía), porque así se declara en el método.

## 4. Registro y declaraciones (Obs. 16)
- Registrar el protocolo en OSF y poner el DOI en `\RegistroOSF` (Parte 8 de la guía).
- Completar las fechas del historial del protocolo (Anexo A, Tabla «Historial»), directamente en Overleaf.
- Revisar la **declaración de uso de IA** que ya está en el manuscrito y ajustarla si el curso o la revista pide otro formato.
- **Repositorio de datos:** no hagas público el repositorio con los PDF de los artículos (tienen derechos de autor). Comparte solo `RSL/suplementos`, `RSL/cribado` (sin la carpeta `pdf`) y el manuscrito, por ejemplo en OSF.

## 5. Verificaciones bibliográficas que no pude cerrar sin acceso a las editoriales
- Cai et al. 2021 (SIGSPATIAL): pp. 354–364 se tomaron de la v1; el PDF no imprime la paginación.
- Chakraborty et al. 2023 (AAMAS): sin DOI. Confirmen la URL `ifaamas.org/Proceedings/aamas2023/pdfs/p1125.pdf`.
- Zhang et al. 2020 (IEEE Trans. Big Data, revisión previa): volumen y páginas tomados de citas secundarias.
