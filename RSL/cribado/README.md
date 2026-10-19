# Guía completa del cribado (búsqueda → Parsif.al → cribado → PRISMA → Overleaf)

Esta guía se sigue **parte por parte, en orden**. Cada parte dice **quién** la hace, **qué** se hace, **qué comando** se ejecuta y **qué se sube a GitHub**. Antes de cribar, lean **`MANUAL_CRIBADO.md`**: ahí están los criterios con su fundamento y ejemplos.

**Roles sugeridos** (ajústenlos, pero que R1 y R2 no cambien durante todo el proceso):

| Rol | Persona | Hace |
|---|---|---|
| Coordinador (R3) | Wrangler | Búsqueda, scripts, Parsif.al y desempates |
| Revisor 1 (R1) | Wilbert | Cribado independiente y calidad |
| Revisor 2 (R2) | Ender | Cribado independiente y calidad |

Todos los comandos se ejecutan en la consola de Windows (CMD) **desde la carpeta `RSL`** del repositorio:
```bat
cd "C:\Users\mayta\OneDrive\Documents\Cursos\2026-2\Investigación IV\rsl-wilbert\RSL"
```
Si `python` no funciona, usen `py` en su lugar (por ejemplo, `py cribado\scripts\01_unificar_exportaciones.py`).

---

## Parte 0. Preparación (una vez, cada integrante)

1. Instalar **Python 3** (https://www.python.org, marcando *Add Python to PATH*) y luego:
   ```bat
   pip install openpyxl
   ```
2. Actualizar el repositorio:
   ```bat
   git checkout claude/loving-volta-papmwq
   git pull
   ```
3. Comprobar que todo funciona:
   ```bat
   python cribado\scripts\01_unificar_exportaciones.py
   ```
   Si dice *«No se encontraron exportaciones…»*, la instalación está bien: aún no hay datos.

**Rutina de Git durante todo el proceso:**
- antes de trabajar: `git pull`
- al terminar: `git add RSL` → `git commit -m "qué hiciste"` → `git pull` → `git push`

---

## Parte 1. Ejecutar la búsqueda y descargar los resultados (R3)

Las cadenas exactas están en `RSL\suplementos\cadenas_busqueda.txt`. Entren a cada base desde la **biblioteca virtual UPeU**, para tener acceso completo.

Para **cada base**:
1. Abrir la **búsqueda avanzada** y pegar la cadena de esa base.
2. Aplicar los filtros indicados: años 2020–2026, artículo y conferencia, inglés o español.
3. Anotar el **número de resultados que muestra la pantalla**.
4. Tomar una **captura de pantalla** que muestre la cadena, los filtros y el número de resultados. Guardarla en `RSL\suplementos\capturas_busqueda\` (por ejemplo, `Scopus_2026-11-12.png`).
5. **Exportar todos los resultados con el resumen** y guardar los archivos en la carpeta de la base:

| Base | Carpeta | Cómo exportar |
|---|---|---|
| Scopus | `cribado\exportaciones\Scopus\` | *Export* → **CSV**, marcando *Citation information*, *Bibliographical information* y *Abstract & keywords* |
| Web of Science | `cribado\exportaciones\WoS\` | *Export* → **Tab delimited file**, *Full Record*. Máximo 1000 por vez: exportar en lotes (1–1000, 1001–2000…) |
| IEEE Xplore | `cribado\exportaciones\IEEE\` | Seleccionar todo → *Export* → **CSV**. Son **dos consultas**: exportar las dos |
| ScienceDirect | `cribado\exportaciones\ScienceDirect\` | Seleccionar todo → *Export* → **RIS**. Exporta por página: repetir en cada página. Son **tres consultas** |
| ACM DL | `cribado\exportaciones\ACM\` | Seleccionar todo → *Export Citations* → **BibTeX**, página por página |

6. Llenar `cribado\exportaciones\fechas_busqueda.csv` (se puede abrir con Excel y guardar como CSV):
   ```
   base,fecha,resultados_en_pantalla,responsable,observaciones
   Scopus,12/11/2026,312,Wrangler,
   WoS,12/11/2026,198,Wrangler,lotes 1-198
   IEEE,13/11/2026,240,Wrangler,consulta 1 = 180; consulta 2 = 60
   ...
   ```
   La fecha va como **dd/mm/aaaa**. En IEEE y ScienceDirect, `resultados_en_pantalla` es la **suma** de sus consultas.

> **Es importante hacer todas las búsquedas el mismo día o en días seguidos.** La fecha de la última búsqueda es la que se reporta en el artículo.

---

## Parte 2. Unir, contar y eliminar duplicados (R3)

```bat
python cribado\scripts\01_unificar_exportaciones.py
python cribado\scripts\02_deduplicar.py
```

**Qué revisar en la pantalla:**
- **Script 01:** «leídos» debe coincidir con «pantalla» en cada base. Si dice *NO COINCIDE*, falta exportar algún lote o una página: corríjanlo **antes** de seguir, porque el PRISMA exige el número exacto.
- **Script 02:** «Conjunto de control». Los 21 estudios ya incluidos en la RSL deberían aparecer, **salvo S03 y S14**, que se declaran como «otros métodos». Si falta otro:
  - revisen que se exportó todo;
  - si de verdad la cadena no lo recupera, avísenme: hay que decidir si se ajusta la cadena o se declara en «otros métodos».

**Qué se genera** en `cribado\salida\`:

| Archivo | Para qué |
|---|---|
| `01_registros_todos.csv` | Todos los registros (identificados por base) |
| `02_registros_unicos.csv` | Registros únicos con su ID (R0001…), que es el que se usa en todo el cribado |
| `02_duplicados.csv` | Evidencia de cada duplicado eliminado y con cuál coincidió |
| `02_conjunto_control.csv` | En qué bases apareció cada estudio del corpus |
| `parsifal\<Base>.bib` | Un archivo por base, **ya sin duplicados**, para importar en Parsif.al |

**Subir:** `git add RSL` → `git commit -m "Búsqueda v2 y deduplicación"` → `git pull` → `git push`.

---

## Parte 3. Preparar Parsif.al (R3)

Parsif.al es el **registro oficial** del protocolo y de las decisiones finales. Guarda **un solo estado por estudio**, no la decisión de cada revisor por separado. Por eso el cribado independiente se hace en las hojas Excel (Partes 4 a 6), y en Parsif.al se registra la **decisión de consenso** (Parte 7).

1. En https://parsif.al creen un proyecto nuevo **«RSL v2 – Detección de anomalías en tráfico (DL)»**, o dupliquen el anterior. Agreguen a los otros dos como coautores (*Co-authors*).
2. **Planning:**
   - *Objectives*, *PICOC* y *Research Questions*: copien los de la v2 desde el manuscrito (Tabla 2 y RQ1–RQ6).
   - *Keywords and Synonyms* y *Search String*: los bloques A, B y C de `cadenas_busqueda.txt`.
   - *Sources*: **Scopus, Web of Science, IEEE Xplore, ScienceDirect y ACM Digital Library**. Quiten MDPI y Taylor & Francis. En cada fuente peguen su cadena exacta.
   - *Selection Criteria*: cargar los criterios **exactamente** como en el manual (CI-1 a CI-6 y CE-1 a CE-6).
   - *Quality Assessment Checklist*: las preguntas QA1–QA8, con respuestas Sí (1), Parcial (0.5) y No (0).
   - *Data Extraction Form*: los campos de la Tabla 6 del manuscrito.
3. **Conducting → Search:** en cada fuente, *Import BibTeX file* con su archivo `cribado\salida\parsifal\<Base>.bib`. El número de estudios por fuente debe coincidir con lo que imprimió el script 02.
4. Pueden ejecutar el buscador de duplicados de Parsif.al como control. Si encuentra alguno, márquenlo como *Duplicated* y avísenme para que el script lo considere.
5. Exporten el protocolo de Parsif.al (Planning → *Export*) en PDF: sirve para registrarlo en OSF (Parte 9).

---

## Parte 4. Piloto de calibración (R1 y R2, ~1 hora cada uno)

**R3 ejecuta:**
```bat
python cribado\scripts\03_preparar_cribado_TA.py --piloto 50
```
Esto crea `cribado\revision\piloto_R1.xlsx` y `piloto_R2.xlsx`, con los mismos 50 registros al azar. Luego hay que subirlos con `git add RSL`, `git commit` y `git push`.

**R1 y R2, cada uno por su cuenta:**
1. `git pull`.
2. Abrir **solo su archivo**. **No abran el del otro.**
3. Leer la hoja *Criterios* y el `MANUAL_CRIBADO.md`.
4. En la hoja *Cribado*, para cada registro, elegir en DECISIÓN *Incluir*, *Duda* o *Excluir*. Si es *Excluir*, elegir el CRITERIO según el árbol del manual (el primero que falla).
5. La hoja *Avance* muestra cuántos faltan. Al terminar, «Excluir SIN criterio» debe ser 0.
6. Guardar y subir **solo su archivo**:
   ```bat
   git add cribado\revision\piloto_R1.xlsx
   git commit -m "Piloto R1"
   git pull
   git push
   ```
   R2 hace lo mismo con su archivo. Como son archivos distintos, no hay conflicto.

**R3, cuando ambos terminaron:**
```bat
git pull
python cribado\scripts\04_consolidar.py --etapa piloto
```
- Si **κ ≥ 0,60**, hacen la reunión de consenso (Parte 5) y siguen.
- Si **κ < 0,60**, se reúnen los tres, revisan cada desacuerdo con el manual, **escriben las aclaraciones** en la sección 7 del manual y repiten el piloto con otra muestra:
  ```bat
  python cribado\scripts\03_preparar_cribado_TA.py --piloto 50 --semilla 2027 --forzar
  ```

---

## Parte 5. Reunión de consenso (se repite en piloto, TA y TC)

1. R3 abre `cribado\salida\consolidado_<etapa>.xlsx` (por ejemplo, `consolidado_piloto.xlsx`). Donde los revisores coinciden, la decisión final ya viene llenada.
2. Filtren la columna **ACUERDO** por «NO» (rojo) y por «criterio distinto» (amarillo).
3. Discutan cada caso **con el manual**, no por votación. Escriban la **DECISIÓN FINAL**, el **CRITERIO FINAL** y la **nota**; en texto completo, también la **EVIDENCIA FINAL**. Si no hay acuerdo, decide R3.
4. Guardar y cerrar la etapa:
   ```bat
   python cribado\scripts\04_consolidar.py --etapa piloto --cerrar
   ```
   Si falta algo, el script dice qué registro está incompleto y no cierra.
5. Subir: `git add RSL` → `git commit -m "Consenso piloto"` → `git pull` → `git push`.

---

## Parte 6. Cribado por título y resumen (R1 y R2, varios días)

**R3:**
```bat
python cribado\scripts\03_preparar_cribado_TA.py
```
Esto crea `TA_R1.xlsx` y `TA_R2.xlsx` con **todos** los registros; los del piloto vienen ya decididos. Luego `git add`, `commit` y `push`.

**R1 y R2:** igual que en el piloto, cada uno en su archivo y sin consultarse.
- Consejo: avancen por bloques de 100 y guarden seguido. Pueden subir avances parciales de **su** archivo.
- **Ante la duda, *Duda* (no *Excluir*).**
- Si un registro **no tiene resumen** (la señal lo avisa), búsquenlo por su DOI o en Google Scholar antes de decidir.

**R3, al terminar ambos:**
```bat
git pull
python cribado\scripts\04_consolidar.py --etapa TA
```
Luego la reunión de consenso (Parte 5) y:
```bat
python cribado\scripts\04_consolidar.py --etapa TA --cerrar
```

---

## Parte 7. Cribado a texto completo (R1 y R2)

**R3:**
```bat
python cribado\scripts\05_preparar_texto_completo.py
```
Se generan:
- `TC_R1.xlsx` y `TC_R2.xlsx`;
- `cribado\salida\05_lista_pdf_a_conseguir.csv`, para repartir la descarga de los PDF.

**Conseguir los PDF** (los tres): guarden cada uno como `cribado\pdf\R0123.pdf`, usando el ID del registro. **Esa carpeta no se sube a GitHub** (derechos de autor): compártanla por OneDrive o Drive. Si un PDF no se consigue tras intentarlo con la biblioteca, Google Scholar, ResearchGate y un correo al autor, márquenlo como **«No recuperado»**.

**R1 y R2**, cada uno en su archivo y leyendo el PDF completo:
- *Texto completo*: «Sí» o «No recuperado».
- *DECISIÓN*: Incluir o Excluir, recorriendo el árbol **completo** del manual (incluye CI-6 y CE-6).
- *CRITERIO*: el primero que falla.
- *EVIDENCIA*: **obligatoria si se excluye**. Copien la frase del artículo con página o sección. Por ejemplo: `p. 9, Sec. 5: "the anomaly detection results are illustrated in Figure 7"` → CI-6.

**R3, al terminar ambos:**
```bat
git pull
python cribado\scripts\04_consolidar.py --etapa TC
```
Luego la reunión de consenso (Parte 5) y:
```bat
python cribado\scripts\04_consolidar.py --etapa TC --cerrar
```

---

## Parte 8. Resultados PRISMA y registro en Parsif.al (R3)

```bat
python cribado\scripts\06_resultados_prisma.py
```
**Qué hace:**
- calcula todas las cifras del diagrama PRISMA;
- las escribe en `manuscrito\datos_busqueda.tex`, junto con las fechas y los kappa;
- genera `manuscrito\generado\base_recuperacion.tex`, con la base de cada estudio;
- muestra un resumen (también queda en `salida\06_resumen_prisma.txt`).

**Lean los AVISOS del final**, que pueden ser de dos tipos:
- *«S0X está en el corpus pero el cribado lo dejó como Excluir»*: revisen si la decisión es correcta. Si lo es, **avísenme**: hay que sacarlo del corpus y regenerar las tablas.
- *«NUEVO estudio incluido R0XXX»*: la nueva búsqueda encontró un estudio que no estaba. **Pásenme el PDF**: lo extraigo con el mismo formato, lo agrego a la matriz y regenero todo.

**Registrar en Parsif.al:** con `salida\06_estado_para_parsifal.csv` (ábranlo en Excel), en *Conducting → Study Selection* marquen cada estudio como *Accepted* o *Rejected*. En los rechazados, anoten el criterio (por ejemplo, «CE-3») en el campo de comentarios, o seleccionen el criterio si Parsif.al lo permite. El ID R0XXX aparece en el campo *note* de cada estudio, para encontrarlos rápido.

**Material suplementario (PRISMA 16b):** `salida\06_excluidos_texto_completo.csv` es la lista de excluidos a texto completo con su motivo y evidencia.

---

## Parte 9. Calidad, registro OSF y datos manuales

### 9.1 Evaluación de calidad (R1 y R2)
```bat
python cribado\scripts\07_calidad.py --preparar
```
Cada revisor llena **su** archivo `cribado\revision\calidad_R1.xlsx` o `calidad_R2.xlsx`: QA1–QA8 con 1, 0.5 o 0, leyendo el PDF y sin mirar la matriz ni al otro revisor. Las definiciones están en la hoja *Definiciones*.

Luego R3 ejecuta:
```bat
python cribado\scripts\07_calidad.py --consolidar
```
- Discutan las celdas rojas de `salida\consolidado_calidad.xlsx` y escriban el consenso.
- Apliquen el resultado y regeneren las tablas:
  ```bat
  python cribado\scripts\07_calidad.py --aplicar
  python suplementos\generar_conteos.py
  python cribado\scripts\06_resultados_prisma.py
  ```

### 9.2 Registro del protocolo en OSF (R3)
1. Crear una cuenta en https://osf.io → *Create new project* («RSL detección de anomalías de tráfico con DL»).
2. Subir: el protocolo exportado de Parsif.al, `cadenas_busqueda.txt`, `MANUAL_CRIBADO.md` y las capturas de búsqueda.
3. *Registrations* → *New registration* → plantilla «OSF Preregistration» u «Open-Ended Registration» → enviar.
4. Copiar el DOI que da OSF.

### 9.3 Datos que se escriben a mano
En `manuscrito\datos_busqueda.tex` (o directamente en Overleaf, Parte 10), reemplacen el texto rojo de:
- `\RegistroOSF` → `OSF, DOI 10.17605/OSF.IO/XXXXX`
- `\RevisoresCribado` → iniciales de R1 y R2
- `\RevisorTercero` → iniciales de R3

---

## Parte 10. Overleaf (el manuscrito se trabaja ahí)

### Crear el proyecto (una vez)
1. Ejecutar:
   ```bat
   python cribado\scripts\08_paquete_overleaf.py
   ```
2. En https://www.overleaf.com: *New Project* → *Upload Project* → elegir `cribado\salida\overleaf_proyecto_completo.zip`.
3. *Menu*:
   - **Main document**: `RSL_v2.tex`
   - **Compiler**: `pdfLaTeX`
4. *Recompile*. Overleaf procesa la bibliografía solo.
5. *Share*: inviten a los demás. Revisen el límite de colaboradores de su plan; si la universidad tiene licencia institucional de Overleaf, úsenla.

### Reglas en Overleaf
- **Sí se edita en Overleaf:** `RSL_v2.tex` (redacción) y `referencias.bib`.
- **No se edita en Overleaf:** `datos_busqueda.tex` y la carpeta `generado/`. Los escriben los scripts; si los editan a mano, se pierde el cambio en la próxima actualización. La única excepción son los tres datos manuales de la Parte 9.3, que conviene poner en `datos_busqueda.tex` **del repositorio** para que no se pierdan.

### Actualizar Overleaf cuando cambian los datos
Cada vez que ejecuten `06_resultados_prisma.py`, `07_calidad.py --aplicar` o `generar_conteos.py`:
```bat
python cribado\scripts\08_paquete_overleaf.py
```
Luego, en Overleaf:
1. Descomprimir `cribado\salida\overleaf_actualizar.zip`.
2. Subir (*Upload*) `datos_busqueda.tex` y los archivos de `generado/`, **reemplazando** los existentes.
3. Recompilar.

### Guardar el manuscrito en GitHub
Al final de cada semana, o antes de entregar: en Overleaf, *Menu → Download → Source*. Copien `RSL_v2.tex` y `referencias.bib` a `RSL\manuscrito\` y suban con `git add`, `commit` y `push`. Así el repositorio tiene siempre la última versión.

---

## Parte 11. Cierre

1. Comprueben que en el PDF de Overleaf **no queda nada en rojo**.
2. Avísenme. Reviso la coherencia de todo el documento (resumen, tablas, PRISMA y conclusiones) y actualizo la matriz de respuesta al ingeniero.
3. Se hace un *Pull Request* de la rama hacia `main`.
4. Se entrega al ingeniero:
   - el PDF de Overleaf;
   - la matriz de respuesta;
   - el material suplementario: `matriz_extraccion.xlsx`, los consolidados del cribado, `06_excluidos_texto_completo.csv`, `02_duplicados.csv`, `cadenas_busqueda.txt`, el manual de cribado y el enlace a OSF.

---

## Resumen de comandos

| Parte | Quién | Comando |
|---|---|---|
| 2 | R3 | `python cribado\scripts\01_unificar_exportaciones.py` |
| 2 | R3 | `python cribado\scripts\02_deduplicar.py` |
| 4 | R3 | `python cribado\scripts\03_preparar_cribado_TA.py --piloto 50` |
| 4–5 | R3 | `python cribado\scripts\04_consolidar.py --etapa piloto` → consenso → `... --cerrar` |
| 6 | R3 | `python cribado\scripts\03_preparar_cribado_TA.py` |
| 6 | R3 | `python cribado\scripts\04_consolidar.py --etapa TA` → consenso → `... --cerrar` |
| 7 | R3 | `python cribado\scripts\05_preparar_texto_completo.py` |
| 7 | R3 | `python cribado\scripts\04_consolidar.py --etapa TC` → consenso → `... --cerrar` |
| 8 | R3 | `python cribado\scripts\06_resultados_prisma.py` |
| 9 | R3 | `python cribado\scripts\07_calidad.py --preparar` / `--consolidar` / `--aplicar` |
| 10 | R3 | `python cribado\scripts\08_paquete_overleaf.py` |

Si un script muestra un error, copien el mensaje completo y me lo pasan.
