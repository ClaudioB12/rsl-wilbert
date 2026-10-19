# Cargar el cribado en Parsif.al y revisarlo allí (paso a paso)

**Qué vas a hacer:** colocar automáticamente en Parsif.al la propuesta de cribado por título y resumen de los 1240 estudios. Para cada uno se cargan tres cosas:

- el estado: *Accepted* o *Rejected*;
- el criterio de selección: CE-2, CE-3, etc.;
- un comentario que explica por qué.

Después tú **revisas** cada estudio en Parsif.al y cambias lo que no te convenza. Al final traes tus decisiones de vuelta a `TA.xlsx` para cerrar la etapa y calcular las cifras del PRISMA.

> **Por qué así:** Parsif.al no tiene un botón para importar decisiones. El script se pega en la consola del navegador y usa **tu propia sesión**: hace lo mismo que harías tú abriendo cada estudio, eligiendo el estado y pulsando *Save*, pero en un minuto. No pide tu contraseña ni la envía a ningún sitio.
>
> El script **se probó** en una copia de Parsif.al con los mismos 1240 estudios. Se actualizaron los 1240 sin errores, se conservaron los resúmenes y la vuelta a `TA.xlsx` dio 0 diferencias.

Tiempo: unos 20 minutos para cargar. La revisión depende de ti; prioriza lo indicado en el Paso 5.

---

## Paso 0. Actualizar el repositorio (git pull)

Abre **CMD** (tecla Windows → escribe `cmd` → Enter) y copia línea por línea:

```bat
cd "C:\Users\mayta\OneDrive\Documents\Cursos\2026-2\Investigación IV\rsl-wilbert"
git checkout claude/loving-volta-papmwq
git pull origin claude/loving-volta-papmwq
```

Comprueba que existan estos archivos (los vas a usar):

```bat
dir RSL\cribado\salida\parsifal
```

Deben aparecer `Scopus.bib`, `WoS.bib`, `IEEE.bib`, `ScienceDirect.bib`, `ACM.bib` y **`cargar_en_parsifal.js`**.

> Si `git pull` dice que tienes cambios locales que se perderían, ejecuta primero `git stash`, luego el `git pull` y después `git stash pop`.

---

## Paso 1. Quitar de Parsif.al lo que importaste antes

Lo que importaste antes (1124 estudios) se hizo con el filtro *Open Access*, que **no** es un criterio del protocolo. Por eso hay que reemplazarlo.

1. En Parsif.al abre tu revisión → **Conducting → Study Selection**.
2. Haz clic en **All Sources** (la primera pestaña).
3. Marca la casilla del encabezado de la tabla (selecciona todos los estudios).
4. En **Action** elige **Remove selected** → **Go** → confirma.
5. Debe quedar «No articles».

---

## Paso 2. Importar los estudios nuevos (ya sin duplicados)

1. Ve a **Conducting → Import Studies**.
2. En cada fuente, pulsa **Import BibTeX** y elige el archivo de `RSL\cribado\salida\parsifal\`:

| Fuente en Parsif.al | Archivo | Estudios |
|---|---|---|
| Scopus | `Scopus.bib` | 497 |
| ISI Web of Science | `WoS.bib` | 9 |
| IEEE Digital Library | `IEEE.bib` | 53 |
| Science@Direct | `ScienceDirect.bib` | 303 |
| ACM Digital Library | `ACM.bib` | 378 |
| **Total** | | **1240** |

Que WoS tenga solo 9 e IEEE 53 es normal. Los demás estudios de esas bases **también** estaban en Scopus o ScienceDirect, y cada estudio se importa una sola vez, en la primera base donde apareció. Esto es la deduplicación.

---

## Paso 3. Revisar los criterios de selección

Ve a **Planning → Selection criteria**. Cada criterio debe **empezar por su código**, tal como está en `PARSIFAL_COPIAR_PEGAR.md`. Por ejemplo:

```
CE-2: No trata de tráfico vehicular por carretera (tráfico de red, ...)
```

El script elige el criterio por ese código (CE-1, CE-2, CE-3, CE-4, CE-5, CI-2…). Si a un criterio le falta el código, añádeselo. Si no, ese criterio solo quedará escrito en el comentario.

---

## Paso 4. Cargar las decisiones con el script (≈ 1 minuto)

1. Usa **Google Chrome** o **Microsoft Edge**.
2. En Parsif.al abre tu revisión → **Conducting → Study Selection** y deja esa pestaña abierta.
3. En el Explorador de Windows abre la carpeta `RSL\cribado\salida\parsifal\`. Haz clic derecho en **`cargar_en_parsifal.js`** → *Abrir con* → **Bloc de notas**.
4. En el Bloc de notas pulsa **Ctrl + A** y luego **Ctrl + C**. Así copias todo el archivo.
5. Vuelve a Parsif.al y pulsa **F12**. Se abren las herramientas de desarrollador; ve a la pestaña **Console**.
6. Pega con **Ctrl + V** y pulsa **Enter**.
   - **La primera vez** Chrome no deja pegar y muestra un aviso: escribe a mano `allow pasting` (en Edge, `permitir pegar`), pulsa Enter y vuelve a pegar con Ctrl + V y Enter.
7. Aparece el mensaje *«Se van a actualizar 1240 estudios… ¿Continuar?»* → **Aceptar**.
8. Espera. En la consola verás `… 50 de 1240`, `… 100 de 1240`, etc. Al final sale *«Listo: 1240 estudios actualizados»*.
9. Recarga la página con **F5**. Ahora cada estudio aparece como *Accepted* o *Rejected*.

**Si algo sale mal:**

| Mensaje | Qué hacer |
|---|---|
| «Abre primero tu revisión…» | No estabas en la página de la revisión. Ve a Conducting → Study Selection y pega otra vez. |
| «Ningún estudio coincide por título» | No importaste los archivos del Paso 2. Repite el Paso 2. |
| «X con error» | Vuelve a pegar el script. Solo se reescriben las decisiones, así que no se duplica nada. |
| «Criterios que no existen en Parsif.al…» | Falta el código en algún criterio. Ve al Paso 3, corrígelo y vuelve a pegar el script. |

---

## Paso 5. Revisar en Parsif.al (esta es tu parte)

Cada comentario empieza con una etiqueta y luego dice por qué. Por ejemplo:

```
[Excluir CE-2 · confianza IA media] IA (verificar): Detecta intrusiones en redes informáticas, no tráfico vehicular → CE-2.
[Duda · confianza IA baja] IA (verificar): (solo título; sin resumen) ...
[Incluir · confianza IA alta] IA (verificar): Detecta accidentes en video de cámaras de tráfico con CNN-LSTM; ...
```

**Cómo revisar:**

1. En Study Selection, haz clic en un estudio. Se abre su ficha con el título, el resumen, **Status**, **Selection criteria** y **Comments**.
2. Lee el título y el resumen, y después el comentario.
3. **Si estás de acuerdo:** pulsa **Next**. No hace falta guardar porque no cambiaste nada.
4. **Si no estás de acuerdo:**
   - Cambia el **Status** (Accepted o Rejected) y, si lo rechazas, el **Selection criteria**.
   - En el comentario cambia la etiqueta del inicio. Por ejemplo, `[Excluir CE-3 · …]` pasa a `[Incluir]`.
   - Borra «IA (verificar):» y escribe tu motivo en una frase.
   - Pulsa **Save** y luego **Next**.
   - No marques la casilla *«Automatically save the status on change and move next»*: guardaría el estado antes de que alcances a corregir el criterio y el comentario.
5. Un estudio en **Duda** se deja en **Accepted** y con la etiqueta `[Duda…]`, porque pasa a texto completo. Cuando dudes, no lo rechaces; es la regla del protocolo.

**En qué orden revisar** (usa *Show: Rejected / Accepted* encima de la tabla):

1. Los que dicen **«confianza IA baja»** (69) y **«media»** (351). Es donde la IA puede equivocarse.
2. Todos los **Rejected** que **no** sean volúmenes de actas: CE-2, CE-3 y CE-4. Una exclusión equivocada es irreversible.
3. Los **Accepted**: confirma que de verdad hablan de tráfico vehicular, anomalías y Deep Learning.
4. Los volúmenes de actas de ACM («Proceedings of …», CE-5) basta con mirarlos por encima.

**Casos conocidos a mirar:**

- **Revistas chinas o japonesas con título bilingüe:** R0016, R0242, R0296, R0306, R1131, R1158, R1207, R1211, R1221, R1222 y R1225. Si el texto completo no está en inglés ni en español, en la etapa de texto completo van por CI-2.
- **R0072 y R0102:** parecen el mismo estudio publicado en dos revistas. Compáralos en el texto completo.
- **ACM sin resumen:** se decidieron solo por el título. Cuando tengas la exportación oficial de ACM, con resúmenes, se revisan de nuevo.

> Puedes revisar también en Excel (`RSL\cribado\revision\TA.xlsx`) en vez de en Parsif.al. Elige **un solo** lugar para no mezclar. Si eliges Excel, al terminar ejecuta `python cribado\scripts\09_generar_script_parsifal.py` y repite el Paso 4 para que Parsif.al quede igual que el Excel.

---

## Paso 6. Traer tus decisiones de vuelta y cerrar la etapa

Cuando termines de revisar en Parsif.al:

1. En Study Selection → **All Sources** → botón **Export Articles**. Se descarga `articles.xls`.
2. Mueve ese archivo a `RSL\cribado\salida\parsifal\articles.xls`.
3. En CMD:

```bat
cd "C:\Users\mayta\OneDrive\Documents\Cursos\2026-2\Investigación IV\rsl-wilbert\RSL"
pip install xlrd
python cribado\scripts\10_traer_de_parsifal.py
```

El script te dice cuántos estudios encontró (deben ser 1240), cuántas decisiones cambiaste y si alguno quedó sin decidir o rechazado sin criterio. Corrige esos en Parsif.al y repite los pasos 1 a 3 de esta sección.

4. Cierra la etapa:

```bat
python cribado\scripts\04_cerrar_etapa.py --etapa TA
```

Muestra cuántos incluiste y excluiste y el **acuerdo entre tú y la IA** (cuántas propuestas cambiaste). Esa cifra va al artículo.

5. Guarda todo en GitHub:

```bat
cd ..
git add RSL
git commit -m "Cribado TA verificado por el autor"
git push
```

Avísame cuando hayas hecho el push. El siguiente paso es el texto completo: la lista de PDF a descargar y la lectura de los PDF con el asistente.
