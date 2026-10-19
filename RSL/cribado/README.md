# Guía completa — de cero a la RSL terminada (autor único: Wilbert A. Mayta Arotaype)

Esta guía se sigue **en orden**, sin saltarse partes. Cada parte dice qué hacer, qué comando copiar y qué revisar. Si algo sale distinto de lo que dice la guía, **copia lo que salió en pantalla y pégamelo en el chat**.

**Documentos que acompañan esta guía:**

| Documento | Para qué |
|---|---|
| `MANUAL_CRIBADO.md` | Criterios de inclusión y exclusión con su fundamento y ejemplos. Léelo **antes** de cribar |
| `PARSIFAL_COPIAR_PEGAR.md` | Todos los textos de Parsif.al listos para Ctrl+C / Ctrl+V |
| `..\suplementos\cadenas_busqueda.txt` | Cadenas de búsqueda exactas de cada base |

**Cómo te ayuda el asistente (los scripts):**
- **Título y resumen:** pre-clasifica cada registro como «Excluir (regla)», «Probable incluir» o «Revisar». Solo propone exclusiones por criterios objetivos (survey, año, idioma o dominio claramente no vial), que tú verificas. Todo lo demás lo decides tú, ayudado por el motivo que te muestra.
- **Texto completo:** lee cada PDF y te muestra, con página, las frases donde aparecen las métricas de detección, lo que proponen los autores y los términos de Deep Learning. Así no tienes que leer el artículo entero para encontrar la evidencia, pero **la decisión es tuya**.
- **PRISMA:** calcula todas las cifras y las escribe en el manuscrito.

> **Por qué no decide todo solo:** el ingeniero pidió que la selección sea verificable y no sesgada. Un script que excluye sin que nadie lo verifique es justo lo que un revisor rechazaría. Con este esquema, el asistente te ahorra la mayor parte del tiempo, cada decisión tiene una persona responsable y el artículo puede reportar cuánto coincidieron tú y el asistente.

---

## PARTE 0 — Preparar tu computadora (una sola vez, ~20 min)

### 0.1 Actualizar el repositorio
Abre **CMD** (tecla Windows → escribe `cmd` → Enter) y copia:
```bat
cd "C:\Users\mayta\OneDrive\Documents\Cursos\2026-2\Investigación IV\rsl-wilbert"
git checkout claude/loving-volta-papmwq
git pull
```

### 0.2 Instalar Python
1. Ve a https://www.python.org/downloads/ → *Download Python 3.x*.
2. Al instalar, **marca la casilla «Add python.exe to PATH»** (abajo, en la primera pantalla) → *Install Now*.
3. Cierra el CMD, ábrelo de nuevo y comprueba:
```bat
python --version
```
Debe decir `Python 3.x.x`. Si dice que no se reconoce el comando, prueba con `py --version`. Si funciona `py`, usa **`py` en lugar de `python`** en todos los comandos de esta guía.

### 0.3 Instalar las dos librerías
```bat
pip install openpyxl pypdf
```

### 0.4 Ir a la carpeta de trabajo y probar
Todos los comandos de la guía se ejecutan **desde la carpeta `RSL`**:
```bat
cd "C:\Users\mayta\OneDrive\Documents\Cursos\2026-2\Investigación IV\rsl-wilbert\RSL"
python cribado\scripts\01_unificar_exportaciones.py
```
Si responde *«No se encontraron exportaciones…»*, **todo está bien instalado**: aún no hay datos.

### 0.5 Rutina de Git (cada vez que termines una parte)
```bat
cd "C:\Users\mayta\OneDrive\Documents\Cursos\2026-2\Investigación IV\rsl-wilbert"
git add RSL
git commit -m "Describe lo que hiciste"
git push
```

---

## PARTE 1 — Crear el proyecto en Parsif.al: Planning (~40 min)

Abre `PARSIFAL_COPIAR_PEGAR.md` y sigue sus secciones **1 y 2**: crear la revisión, objetivos, PICOC, preguntas, palabras clave, cadena, fuentes, criterios, lista de calidad y formulario de extracción. Todo es copiar y pegar.

Al terminar, en Parsif.al deben aparecer:
- **5 fuentes**: Scopus, Web of Science, IEEE Xplore, ScienceDirect y ACM DL;
- **12 criterios**: CI-1 a CI-6 y CE-1 a CE-6;
- **8 preguntas de calidad**: QA1 a QA8.

---

## PARTE 2 — Hacer la búsqueda y descargar los resultados (~1 día)

**Hazlo todo el mismo día o en días seguidos:** la fecha de la última búsqueda se reporta en el artículo.

Entra a cada base **desde la biblioteca virtual de la UPeU**, para tener acceso completo. Abre `RSL\suplementos\cadenas_busqueda.txt` y, para cada base:

### 2.1 Scopus
1. *Search* → *Advanced document search*.
2. Borra lo que haya y pega la cadena de la sección **«## Scopus»**. Debe empezar con `TITLE-ABS-KEY` (si pegas la cadena general sin eso, Scopus busca en todos los campos y salen más de 100 000 resultados). Esa cadena ya incluye los filtros de año, tipo e idioma → *Search*.
3. Anota el **número de resultados** (por ejemplo, «312 documents found»).
4. Toma una **captura de pantalla** (tecla Windows + Shift + S) y guárdala en `RSL\suplementos\capturas_busqueda\Scopus.png`.
5. Marca la casilla *All* → *Export* → **CSV** → marca todo, sobre todo **«Abstract & keywords»** → *Export*.
6. Mueve el archivo descargado a `RSL\cribado\exportaciones\Scopus\`.

### 2.2 Web of Science
1. *Advanced search* → pega la cadena **«## Web of Science»** (empieza con `TS=`) → *Search*.
2. A la izquierda, filtra: *Publication Years* 2020–2026; *Document Types*: Article y Proceeding Paper; *Languages*: English y Spanish.
3. Anota el número de resultados y toma la captura (`WoS.png`).
4. *Export* → **Tab delimited file** → *Records from*: 1 to 1000 → *Record Content*: **Full Record** → *Export*.
5. Si hay más de 1000 resultados, repite con 1001 a 2000, y así sucesivamente.
6. Mueve los archivos a `RSL\cribado\exportaciones\WoS\`.

### 2.3 IEEE Xplore
1. *Advanced Search* → pestaña **Command Search** → pega la **Consulta 1** de la sección «## IEEE Xplore» → *Search*.
2. Filtra: *Year* 2020–2026; *Content Type*: Journals y Conferences.
3. Anota el número de resultados y toma la captura (`IEEE_1.png`).
4. *Select All on Page* → **Export** → pestaña *Results* → **CSV** → *Export*. Si hay varias páginas, cambia a 100 resultados por página y exporta cada página.
5. Repite todo con la **Consulta 2** (`IEEE_2.png`) y la **Consulta 3** (`IEEE_3.png`).
6. Mueve todos los CSV a `RSL\cribado\exportaciones\IEEE\`.

### 2.4 ScienceDirect
1. *Advanced search* → campo **«Title, abstract or author-specified keywords»** → pega la **Consulta 1** de la sección «## ScienceDirect» → *Search*.
2. Filtra: *Years* 2020–2026; *Article type*: Research articles.
3. Anota el número de resultados y toma la captura (`SD_1.png`).
4. Marca la casilla de selección (arriba) → *Export* → **Export citation to RIS**. ScienceDirect exporta **por página**: muestra 100 por página y repite en cada una.
5. Repite con las **Consultas 2, 3, 4 y 5**.
6. Mueve todos los archivos a `RSL\cribado\exportaciones\ScienceDirect\`.

### 2.5 ACM Digital Library
1. *Advanced Search* → pega la cadena **«## ACM Digital Library»** (o arma los tres bloques en el formulario, en el campo *Abstract*) → *Search*.
2. Filtra: *Publication Date* 2020–2026; *Content Type*: Research Article.
3. Anota el número de resultados y toma la captura (`ACM.png`).
4. *Select All* → **Export Citations** → **BibTeX** → *Download*. Si hay varias páginas, exporta cada una.
5. Mueve los archivos a `RSL\cribado\exportaciones\ACM\`.

### 2.6 Anotar fechas y conteos
Abre `RSL\cribado\exportaciones\fechas_busqueda.csv` con el Bloc de notas y complétalo así (con tus números reales):
```
base,fecha,resultados_en_pantalla,responsable,observaciones
Scopus,20/10/2026,312,W. Mayta,
WoS,20/10/2026,198,W. Mayta,
IEEE,20/10/2026,240,W. Mayta,consulta 1 = 150; consulta 2 = 60; consulta 3 = 30
ScienceDirect,21/10/2026,150,W. Mayta,suma de las consultas 1 a 5
ACM,21/10/2026,95,W. Mayta,
```
- La fecha va como **dd/mm/aaaa**.
- En IEEE y ScienceDirect, el número es la **suma** de sus consultas.

**Sube a GitHub** (Parte 0.5) con el mensaje `"Búsqueda v2 ejecutada"`.

---

## PARTE 3 — Unir, quitar duplicados e importar en Parsif.al (~15 min)

```bat
python cribado\scripts\01_unificar_exportaciones.py
python cribado\scripts\02_deduplicar.py
```

**Revisa en la pantalla:**
- **Script 01:** en cada base, «leídos» debe ser igual a «pantalla». Si dice **NO COINCIDE**, falta exportar una página o un lote: búscalo y vuelve a ejecutar.
- **Script 02:** «Conjunto de control: 19 de 21 estudios incluidos aparecen». Lo esperado es que **solo falten S03 y S14**. Si falta otro, **pégame la salida**.

**Importar en Parsif.al:** sigue la sección **3.1** de `PARSIFAL_COPIAR_PEGAR.md`. Los archivos están en `RSL\cribado\salida\parsifal\`.

**Pégame en el chat** lo que imprimieron los scripts 01 y 02: reviso contigo que la búsqueda esté completa antes de cribar.

**Sube a GitHub** con el mensaje `"Deduplicación e importación a Parsif.al"`.

---

## PARTE 4 — Cribado por título y resumen (la parte larga; con el asistente, 1 a 3 días)

### 4.1 Antes de empezar
Lee completo `MANUAL_CRIBADO.md` (unos 20 minutos). Ten abierta la hoja «Criterios» del Excel mientras trabajas.

### 4.2 Crear la hoja con las sugerencias del asistente
```bat
python cribado\scripts\03_preparar_cribado_TA.py
```
La pantalla muestra cuántos registros cayeron en cada grupo. Abre **`RSL\cribado\revision\TA.xlsx`**.

### 4.3 Cómo trabajar en el Excel (en este orden)
Las filas ya vienen ordenadas: primero «Excluir (regla)», luego «Probable incluir» y al final «Revisar».

**Paso A — «Excluir (regla)»** (en rojo; es lo más rápido):
- La DECISIÓN ya viene puesta como *Excluir*, con su criterio.
- Lee **solo el título y el motivo**. Si estás de acuerdo, no toques nada.
- Si no estás de acuerdo (por ejemplo, el título dice «review» pero es un estudio con experimentos), cambia la DECISIÓN a *Incluir* o *Duda*.

**Paso B — «Probable incluir»** (en verde):
- Lee el título y el resumen. Si cumple, elige *Incluir*.
- Ojo con los motivos que dicen «ojo: …» o «parece pronóstico»: ahí puede ser CE-2 o CE-3.
- Para ir rápido: selecciona varias celdas seguidas de DECISIÓN, escribe *Incluir* en la primera y pulsa **Ctrl+D** para rellenar hacia abajo. **Solo** en filas que ya leíste.

**Paso C — «Revisar»** (sin color):
- Lee el título y el resumen. El motivo te dice qué falta (por ejemplo, «No menciona Deep Learning, posible CE-4»).
- Aplica el árbol del manual:
  - Excluye **solo si es claro** → *Excluir* + CRITERIO.
  - Si no puedes saberlo con el resumen → **Duda**, y pasa a texto completo.
- Si dice «SIN RESUMEN», busca el artículo por su título en Google Scholar antes de decidir.

**Control:** la hoja «Avance» te dice cuántos faltan. Al terminar, **«Excluir SIN criterio» debe ser 0**.

Guarda seguido (Ctrl+S) y sube a GitHub al final de cada día.

### 4.4 Cerrar la etapa
```bat
python cribado\scripts\04_cerrar_etapa.py --etapa TA
```
Si falta algo, te dice qué registro y no cierra: complétalo y vuelve a ejecutar. Al cerrar, muestra el acuerdo entre tú y el asistente.

### 4.5 Preparar el re-cribado (para medir tu consistencia)
```bat
python cribado\scripts\04b_recribado.py --etapa TA --preparar
```
Crea `recribado_TA.xlsx` con una muestra al azar, en otro orden. **No lo hagas hoy:** espera al menos 7 días y sigue mientras tanto con la Parte 5. Cuando lo hagas, **no mires TA.xlsx**. Al terminarlo:
```bat
python cribado\scripts\04b_recribado.py --etapa TA --calcular
```
Te da el kappa intra-revisor:
- **≥ 0,61** es bueno.
- Si es menor, revisa los registros que salgan distintos, precisa el manual (sección 7) y corrige en TA.xlsx lo que estaba mal. Luego vuelve a cerrar la etapa con 04.

**Sube a GitHub.**

---

## PARTE 5 — Cribado a texto completo (con el asistente leyendo los PDF)

### 5.1 Crear la hoja y la lista de PDF
```bat
python cribado\scripts\05_preparar_texto_completo.py
```
Abre `RSL\cribado\salida\05_lista_pdf_a_conseguir.csv` en Excel: tiene el enlace DOI de cada artículo.

### 5.2 Descargar los PDF
- Abre cada enlace (conectado a la biblioteca UPeU) y descarga el PDF.
- **Guárdalo con el nombre del ID**, por ejemplo `R0123.pdf`, en la carpeta **`RSL\cribado\pdf\`**. Esa carpeta no se sube a GitHub, por derechos de autor.
- Si no lo consigues: prueba con Google Scholar («Todas las versiones»), ResearchGate o un correo al autor. Si no aparece, en TC.xlsx pon «Texto completo» = **No recuperado**.

### 5.3 Que el asistente lea los PDF
```bat
python cribado\scripts\05b_leer_pdfs.py
```
Llena en `TC.xlsx`, para cada artículo:
- la **SUGERENCIA** y su motivo;
- las **frases con página** donde aparecen las métricas de detección, **qué proponen los autores**, los términos de Deep Learning y los de anomalía o tráfico.

Puedes ejecutarlo de nuevo cada vez que descargues más PDF: **no borra tus decisiones**.

### 5.4 Decidir (abre TC.xlsx y el PDF al lado)
Para cada artículo:
1. Mira **«qué proponen»**. ¿El método propio es Deep Learning? Si es un método clásico y el DL solo aparece como comparación → **CE-4**.
2. Mira **«métricas de detección»**. ¿Hay números de precision, recall, F1, AUC o tasa de detección **sobre la detección de anomalías**?
   - Si solo hay MAE/RMSE de pronóstico, o métricas de otra tarea (Kinetics, reconocimiento de acciones) → **CI-6**.
   - Si la detección solo se muestra en figuras → **CI-6**.
3. Si la sugerencia es «Revisar», lee el motivo y ve a la página indicada del PDF.
4. Llena **DECISIÓN** y, si excluyes, **CRITERIO** y **EVIDENCIA**. En la evidencia puedes **copiar la frase sugerida** si es la correcta, o escribir la tuya, siempre con la página. Ejemplo:
```
p. 9, Sec. 5: "the detection results are shown qualitatively in Fig. 7" (no reporta métricas de detección)
```

### 5.5 Cerrar la etapa y re-cribar
```bat
python cribado\scripts\04_cerrar_etapa.py --etapa TC
python cribado\scripts\04b_recribado.py --etapa TC --preparar
```
Pasados 7 días, haz `recribado_TC.xlsx` y ejecuta:
```bat
python cribado\scripts\04b_recribado.py --etapa TC --calcular
```

**Sube a GitHub.**

---

## PARTE 6 — Resultados PRISMA y registro en Parsif.al (~1 hora)

```bat
python cribado\scripts\06_resultados_prisma.py
```
Muestra el resumen PRISMA completo y lo escribe en `manuscrito\datos_busqueda.tex`.

**Lee los AVISOS del final y pégamelos en el chat:**
- *«S0X está en el corpus pero el cribado lo dejó como Excluir»*: revisemos juntos si la decisión es correcta.
- *«NUEVO estudio incluido R0XXX»*: la búsqueda nueva encontró un estudio que no estaba. **Pásame el PDF por el chat** y lo extraigo con el mismo formato que los demás.

**Registrar en Parsif.al:** sigue la sección **3.2** de `PARSIFAL_COPIAR_PEGAR.md`, con `salida\06_estado_para_parsifal.csv`.

**Sube a GitHub.**

---

## PARTE 7 — Verificar la calidad (QA1–QA8) (~1 a 2 días)

```bat
python cribado\scripts\07_calidad.py --preparar
```
Abre `RSL\cribado\revision\calidad.xlsx`. Hay una fila por estudio e ítem (21 × 8), con el **puntaje propuesto** y su **evidencia**. Para cada fila:
- Lee la evidencia y, si dudas, búscala en el PDF (están en `RSL\Articulos evaluados por calidad\`).
- Escribe **TU PUNTAJE** (1, 0.5 o 0). Si cambias el propuesto, escribe la **justificación**.

Al terminar:
```bat
python cribado\scripts\07_calidad.py --aplicar
python suplementos\generar_conteos.py
python cribado\scripts\06_resultados_prisma.py
```
Copia los puntajes también a Parsif.al (sección **3.3** de `PARSIFAL_COPIAR_PEGAR.md`). **Sube a GitHub.**

---

## PARTE 8 — Registrar el protocolo en OSF (~30 min)

1. Crea una cuenta en https://osf.io (puede ser con tu correo UPeU).
2. *Create new project* → título: «RSL Detección de anomalías en tráfico vehicular con Deep Learning (v2)».
3. *Files* → sube:
   - el protocolo exportado de Parsif.al (Reporting);
   - `RSL\suplementos\cadenas_busqueda.txt`;
   - `RSL\cribado\MANUAL_CRIBADO.md`;
   - las capturas de `RSL\suplementos\capturas_busqueda\`.
4. *Registrations* → *New registration* → plantilla **«Open-Ended Registration»** → en el resumen pega la *Description* de Parsif.al → *Register*.
5. Copia el **DOI** que te da OSF (algo como `10.17605/OSF.IO/ABCDE`) y pégalo en `RSL\manuscrito\datos_busqueda.tex`, en la línea de `\RegistroOSF`:
```
\newcommand{\RegistroOSF}{OSF, DOI 10.17605/OSF.IO/ABCDE}
```

---

## PARTE 9 — Overleaf (el manuscrito se trabaja ahí)

### 9.1 Crear el proyecto (una vez)
```bat
python cribado\scripts\08_paquete_overleaf.py
```
En https://www.overleaf.com:
1. *New Project* → *Upload Project* → elige `RSL\cribado\salida\overleaf_proyecto_completo.zip`.
2. *Menu* (arriba a la izquierda):
   - **Main document** = `RSL_v2.tex`
   - **Compiler** = `pdfLaTeX`
3. *Recompile*.

### 9.2 Reglas
- En Overleaf **solo editas** `RSL_v2.tex` (redacción) y `referencias.bib`.
- **No edites en Overleaf** `datos_busqueda.tex` ni la carpeta `generado`: los escriben los scripts y se reemplazan en cada actualización.

### 9.3 Actualizar Overleaf cuando cambian los datos
Después de los scripts 06 o 07, o de `generar_conteos.py`:
```bat
python cribado\scripts\08_paquete_overleaf.py
```
Luego:
1. Descomprime `RSL\cribado\salida\overleaf_actualizar.zip`.
2. En Overleaf, *Upload*: sube `datos_busqueda.tex` y los archivos de la carpeta `generado`, **reemplazando** los existentes.
3. *Recompile*.

### 9.4 Guardar en GitHub lo que escribas en Overleaf
Cada cierto tiempo: Overleaf → *Menu* → *Download* → *Source*. Copia `RSL_v2.tex` y `referencias.bib` a `RSL\manuscrito\` y sube a GitHub.

---

## PARTE 10 — Cierre

1. En el PDF de Overleaf **no debe quedar nada en rojo**.
2. Avísame en el chat. Reviso la coherencia de todo (resumen, tablas, PRISMA y conclusiones) y actualizo la respuesta al ingeniero (`RSL\respuesta_revision.docx`).
3. Entrega al ingeniero:
   - el PDF de Overleaf;
   - la respuesta;
   - el material suplementario: `suplementos\matriz_extraccion.xlsx`, `cribado\revision\TA.xlsx` y `TC.xlsx`, `cribado\salida\06_excluidos_texto_completo.csv`, `cribado\salida\02_duplicados.csv`, `suplementos\cadenas_busqueda.txt` y `cribado\MANUAL_CRIBADO.md`;
   - el enlace a OSF.

---

## Resumen de comandos (en orden)

```bat
python cribado\scripts\01_unificar_exportaciones.py
python cribado\scripts\02_deduplicar.py
python cribado\scripts\03_preparar_cribado_TA.py
python cribado\scripts\04_cerrar_etapa.py --etapa TA
python cribado\scripts\04b_recribado.py --etapa TA --preparar
python cribado\scripts\05_preparar_texto_completo.py
python cribado\scripts\05b_leer_pdfs.py
python cribado\scripts\04_cerrar_etapa.py --etapa TC
python cribado\scripts\04b_recribado.py --etapa TC --preparar
python cribado\scripts\04b_recribado.py --etapa TA --calcular
python cribado\scripts\04b_recribado.py --etapa TC --calcular
python cribado\scripts\06_resultados_prisma.py
python cribado\scripts\07_calidad.py --preparar
python cribado\scripts\07_calidad.py --aplicar
python suplementos\generar_conteos.py
python cribado\scripts\06_resultados_prisma.py
python cribado\scripts\08_paquete_overleaf.py
```

**Si un script da error:** copia todo lo que salió en pantalla y pégamelo en el chat.

**Ninguno de los scripts borra tu trabajo:** si una hoja ya existe, se niegan a sobrescribirla, salvo que agregues `--forzar`.
