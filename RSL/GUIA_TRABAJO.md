# Guía de trabajo — RSL v2 (Grupo 4)

Esta guía explica **cómo trabajar en equipo con Git** y **qué hacer, en orden**, para terminar la RSL. Los comandos son para Windows (CMD o PowerShell) dentro de la carpeta del repositorio.

---

## Parte 1. Preparar la computadora (una sola vez)

| Programa | Para qué | Cómo instalar |
|---|---|---|
| Git | Bajar y subir cambios | https://git-scm.com (ya lo tienen) |
| Python 3 | Ejecutar los scripts que generan las cifras | https://www.python.org — al instalar marcar **«Add Python to PATH»** |
| openpyxl | Que Python lea y escriba Excel | En la consola: `pip install openpyxl` |
| MiKTeX | Compilar el PDF desde el `.tex` | https://miktex.org — al compilar por primera vez acepta instalar los paquetes que pida |
| Poppler (`pdftotext`) | Solo para `prueba_sensibilidad_cadena.py` (opcional) | `winget install oschwartz10612.Poppler` |

Configurar su nombre en Git (cada uno en su PC):
```bat
git config --global user.name "Wilbert Mayta"
git config --global user.email "wilbert.mayta@upeu.edu.pe"
```

> **Alternativa sin instalar LaTeX:** suban la carpeta `RSL/manuscrito` a Overleaf (Nuevo proyecto → Subir proyecto → zip de la carpeta) y compilen allí. Los scripts de Python sí se ejecutan en su PC.

---

## Parte 2. Rutina diaria con Git

Todo el equipo trabaja en la rama `claude/loving-volta-papmwq` hasta terminar la v2.

### Al empezar a trabajar (SIEMPRE)
```bat
cd "C:\Users\mayta\OneDrive\Documents\Cursos\2026-2\Investigación IV\rsl-wilbert"
git checkout claude/loving-volta-papmwq
git pull
```

### Al terminar (después de cada avance)
```bat
git status
git add RSL
git commit -m "Describe lo que hiciste, p. ej.: Cribado TA completado por W.M."
git pull
git push
```

### Reglas para no pisarse

1. **Hacer `git pull` antes de empezar y antes de `git push`.**
2. **Los archivos Excel y PDF no se pueden fusionar.** Si dos personas modifican `plantilla_cribado.xlsx` al mismo tiempo, uno pierde su trabajo. Por eso:
   - Avisen en el grupo **«estoy editando la plantilla»** y suban apenas terminen.
   - Para el cribado independiente, **cada revisor trabaja en su propia copia fuera del repositorio** (ver Parte 3, paso 2) y solo uno pega las columnas en la plantilla.
3. **No editen a mano** los archivos de `RSL/manuscrito/generado/`: se regeneran con los scripts.
4. **OneDrive:** la carpeta está dentro de OneDrive. Si OneDrive muestra «conflicto» o crea archivos como `archivo-PC.xlsx`, no los suban. Si les da problemas, muevan el repositorio a una carpeta fuera de OneDrive (p. ej., `C:\repos\rsl-wilbert`).
5. Si `git pull` dice **CONFLICT**, no sigan: copien el mensaje y pídanme ayuda.

### Comandos útiles
| Quiero… | Comando |
|---|---|
| Ver qué cambié | `git status` y `git diff` |
| Deshacer cambios de un archivo que aún no subí | `git restore RSL\ruta\archivo` |
| Ver el historial | `git log --oneline -10` |
| Volver a ver la versión anterior (v1) | `git checkout main` (y luego volver con `git checkout claude/loving-volta-papmwq`) |

---

## Parte 3. Qué hacer, en orden

Reparto sugerido: **R1 = Wilbert**, **R2 = Ender**, **R3 = Wrangler** (tercer revisor, búsqueda y trámites). Ajusten como prefieran, pero que R1 y R2 sean siempre los mismos.

### Paso 1 — Re-ejecutar la búsqueda (R3, 1–2 días)
1. Abrir `RSL\suplementos\cadenas_busqueda.txt`.
2. En cada base (Scopus, Web of Science, IEEE Xplore, ScienceDirect y ACM DL), pegar la cadena en la búsqueda avanzada y aplicar los filtros indicados. Entrar desde la biblioteca virtual UPeU para tener acceso.
3. Por cada base:
   - anotar la **fecha** y el **número de resultados** en la hoja **«Busqueda»** de `RSL\suplementos\plantilla_cribado.xlsx`,
   - guardar una **captura de pantalla** en `RSL\suplementos\capturas_busqueda\`,
   - **exportar** los resultados en formato RIS o BibTeX.
4. En Parsif.al crear un proyecto nuevo «RSL v2», importar los cinco archivos y eliminar duplicados.
5. Exportar de Parsif.al la lista de registros únicos (título, año, DOI) y pegarla en la hoja **«Cribado_TA»** (columnas A–E).
6. Subir: `git add RSL` → `git commit -m "Búsqueda v2 ejecutada"` → `git pull` → `git push`.

> Comprueben que los 21 estudios del corpus aparecen. Si **sale un estudio nuevo** que cumple los criterios, me pasan el PDF y lo extraigo con el mismo formato.

### Paso 2 — Cribado por título y resumen (R1 y R2 por separado, 2–3 días)
1. `git pull`. Cada revisor **copia** `plantilla_cribado.xlsx` a su escritorio (fuera del repositorio) con su nombre, p. ej. `cribado_R1_Wilbert.xlsx`.
2. Cada uno llena **solo su columna** (R1 o R2) con *Incluir* o *Excluir*, **sin ver la del otro**. Criterio práctico: ante la duda, *Incluir* (se decide luego con el texto completo).
3. Al terminar, **una sola persona** pega la columna de R1 y la de R2 en la plantilla del repositorio.
4. La columna **«Acuerdo»** muestra **NO** en rojo donde no coinciden: se discuten juntos y se escribe la **«Decisión final»**. Si no hay acuerdo, decide R3.
5. El kappa aparece en la hoja **«Kappa»**. Guardar en Excel y subir con `git add` / `commit` / `pull` / `push`.

### Paso 3 — Cribado a texto completo (R1 y R2 por separado, 3–4 días)
1. Pegar en **«Cribado_TC»** los registros con Decisión final = *Incluir*.
2. Conseguir los PDF (biblioteca UPeU, Google Scholar, o escribiendo a los autores). Si no se consigue, marcar **«No recuperado»**.
3. Igual que antes: cada revisor en su copia, *Incluir*/*Excluir* y, si excluye, **el criterio** (CE-2…CE-6, CI-6) según la Tabla 5 del manuscrito. Luego se consolida, se discuten los desacuerdos y se escribe la decisión y el criterio final.
4. La hoja **«PRISMA»** debe decir **OK** en la fila de control. Si dice **REVISAR**, falta el criterio en alguna exclusión.

### Paso 4 — Evaluación de calidad (R1 y R2 por separado, 2 días)
1. Abrir `RSL\suplementos\matriz_extraccion.xlsx`, hoja **«Calidad»**: tiene un puntaje propuesto con su **evidencia** para cada ítem de los 21 estudios.
2. Cada revisor, en su copia de la plantilla (hoja **«Calidad»**), pone su propio puntaje QA1–QA8 (1 / 0.5 / 0), leyendo el PDF y la evidencia. La Tabla 7 del manuscrito define cada ítem.
3. Se consolidan, se discuten las celdas marcadas en amarillo y se escribe el **consenso**.
4. **Pásenme los puntajes de consenso que difieran de los propuestos** y actualizo la matriz y el manuscrito.

### Paso 5 — Trámites (R3, en paralelo)
- **Registrar el protocolo en OSF:** crear una cuenta en https://osf.io → *Create project* → subir el protocolo exportado de Parsif.al y `cadenas_busqueda.txt` → *Registrations* → *New registration* (plantilla «OSF Preregistration» o «Open-Ended»). Copiar el DOI.
- Completar a mano en `RSL\manuscrito\datos_busqueda.tex`:
  - `\RegistroOSF` con el DOI de OSF,
  - `\RevisoresCribado` y `\RevisorTercero` con las iniciales,
  - `\BaseRecup` (base donde apareció cada estudio).
- Confirmar el **nombre y correo del tercer autor** y las **fechas reales** de cada versión del protocolo.
- Preguntar al docente si la revista o curso pide un texto específico para la **declaración de uso de IA**.

### Paso 6 — Pasar los resultados al manuscrito (5 minutos)
Con la plantilla ya completa y **guardada en Excel**:
```bat
cd RSL
python suplementos\actualizar_datos_busqueda.py
python suplementos\generar_conteos.py
cd manuscrito
pdflatex RSL_v2
bibtex RSL_v2
pdflatex RSL_v2
pdflatex RSL_v2
```
El primer script copia las fechas, los conteos PRISMA y los kappa de la plantilla a `datos_busqueda.tex`, y avisa de lo que siga pendiente. Revisen que en el PDF **no quede nada en rojo**. Luego `git add RSL` → `commit` → `pull` → `push`.

### Paso 7 — Revisión final y entrega
1. Avísenme: reviso la coherencia de todo el documento (resumen, tablas y conclusiones) y actualizo la **matriz de respuesta** (`RSL\respuesta_revision.docx`) con lo que hicieron en los pasos 1–5.
2. Se crea un *Pull Request* de la rama hacia `main` en GitHub para dejar la v2 como versión oficial.
3. Se envía al ingeniero: `RSL_v2.pdf`, `respuesta_revision.docx` y el material suplementario (`matriz_extraccion.xlsx`, `plantilla_cribado.xlsx`, `cadenas_busqueda.txt`, la lista PRISMA y el enlace a OSF).

> **No publiquen el repositorio** con la carpeta `Articulos evaluados por calidad` (los PDF tienen derechos de autor). Para compartir datos, usen OSF o un repositorio solo con `RSL/suplementos` y el manuscrito.

---

## Parte 4. Si quieren modificar algo del análisis

| Quiero cambiar… | Dónde | Luego ejecutar |
|---|---|---|
| Un dato de un estudio (dataset, etiqueta, puntaje de calidad…) | `RSL\suplementos\extraccion_individual\Exx.json` | `generar_conteos.py` + compilar |
| El texto corto que sale en las tablas, o incluir/excluir un estudio | `RSL\suplementos\curacion.json` | `generar_conteos.py` + compilar |
| Fechas, conteos PRISMA, kappa | `plantilla_cribado.xlsx` | `actualizar_datos_busqueda.py` + compilar |
| Redacción | `RSL\manuscrito\RSL_v2.tex` | compilar |
| Referencias | `RSL\manuscrito\referencias.bib` | compilar (con `bibtex`) |

Si algo no les cuadra o un script da error, copien el mensaje completo y me lo pasan.
