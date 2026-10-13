---
title: "Matriz de respuesta al reporte de revisión"
subtitle: "Manuscrito: Detección de anomalías en tráfico vehicular mediante Deep Learning (versión 2)"
---

**Versión revisada:** `RSL/manuscrito/RSL_v2.tex` (PDF: `RSL/manuscrito/RSL_v2.pdf`).
**Material suplementario:** `RSL/suplementos/` (matriz de extracción, evaluación de calidad por ítem, cadenas de búsqueda y scripts).

Todas las cifras del resumen, el texto y las tablas se generan con `python3 RSL/suplementos/generar_conteos.py` a partir de la matriz de extracción. Ninguna se escribe a mano. Los datos que solo los autores pueden aportar (fechas de búsqueda, conteos por base, kappa, registro OSF) aparecen en rojo en el PDF y se centralizan en `RSL/manuscrito/datos_busqueda.tex`.

## Cambio en el corpus

La versión 1 tenía 25 estudios; la versión 2 tiene **21**. Al aplicar los criterios de forma uniforme se excluyeron cinco estudios y no se añadió ninguno:

| ID v1 | Estudio | Criterio | Motivo |
|---|---|---|---|
| E23 | Giasemis y Sopasakis (2025) | CE-5 | Preprint de arXiv. La v1 lo incluía como excepción ad hoc. |
| E01 | Taheri Sarteshnizi et al. (2026) | CE-4 | El método propuesto (Si-TDD) no es DL. Se usa en la discusión como evidencia externa. |
| E15 | Nouri e Ilbeigi (2025) | CI-6 | La detección solo se evalúa de forma cualitativa. |
| E24 | Feng et al. (2021) | CI-6 | Solo evalúa reconocimiento de acciones en Kinetics, no la detección. |
| — | Choudhary y Hassani (2024), estaba en Parsif.al | CE-3 | Solo evalúa el pronóstico (RMSE). |

Los identificadores cambian de E01–E25 a S01–S21, ordenados por año y autor. La correspondencia está en el Anexo B (columna «ID v1»).

## Respuesta por observación

| N.º | Observación | Posición | Qué se hizo y por qué | Ubicación en la v2 | Evidencia |
|---|---|---|---|---|---|
| 1 | No se discuten revisiones previas | Acepto | Se buscaron y verificaron 11 revisiones (2019–2025), incluidas las 5 sugeridas. Tres de ellas se publicaron después en revista: Darban et al. en *ACM Comput. Surv.* 2024, Razi et al. en *IET ITS* 2023 y Fang et al. en *IEEE TCSVT* 2024. Se añadió una tabla con el vacío que deja cada una y se redactó la diferencia de esta RSL: es sistemática, integra sensores, trayectorias y video, y analiza etiquetas y protocolo. Estas revisiones se retoman en la discusión. | §1.1, Tabla 1; §5.1 | `suplementos/revisiones_previas.json` |
| 2 | Síntesis no trazable; la Tabla 6 contradice el texto | Acepto | Se construyó la matriz estudio × variable (21 filas) verificada contra cada PDF. Todos los conteos, porcentajes y tablas se generan con un script. Se eliminó la columna RQ de la Tabla 6. La media de calidad ya no es 5.74 ni 5.76: con el nuevo instrumento es 4.38/8. | §4; todas las tablas `generado/*.tex` | `generar_conteos.py`, `matriz_extraccion.xlsx` |
| 3 | Estudios de fuentes no buscadas; preprint pese a CE-5 | Acepto | Se añadió IEEE Xplore como base, lo que cubre E11 y E15. Se adoptó una regla general para preprints (CE-5), por la que E23 queda excluido. E17 se corrige a AAMAS 2023, pp. 1125–1134. E25 se corrige a *Computers, Materials & Continua* 79(3), 5051–5066. Los dos estudios que la cadena v2 no recupera (S03 y S14 no mencionan DL en su resumen) se declaran en la rama «otros métodos» del PRISMA 2020. La columna «Fuente» pasa a ser «Base de recuperación». | §3.3, §3.4, Fig. 1, Anexo B | `prueba_sensibilidad_cadena.py` |
| 4 | El alcance no coincide con el corpus | Acepto (ruta b) | Se amplió explícitamente el alcance a video y autopistas. Cambian el título, RQ1, el PICOC, la cadena (se quita el bloque «time series» y se añaden términos de video, autopista y vehículo) y CI-4. Se añadió una tabla de alineamiento y se retiró la nota al pie sobre PeMS-D4. | Título; §1; Tablas 2–3; §3.3 | Tabla 3 |
| 5 | El CQI repite la elegibilidad | Acepto | Nuevo instrumento de 8 ítems adaptado de Kitchenham y REFORMS: etiquetas, partición sin fuga, líneas base, variabilidad, código y datos, más de un escenario, protocolo y limitaciones. Se reporta por ítem y por estudio con su evidencia. No se usa para excluir. Se usa en un análisis de sensibilidad con los estudios de calidad ≥ 5. | §3.7, Tabla 7; §4.3, Tabla 9; §4.9 | Hoja «Calidad» del xlsx |
| 6 | No se declaran los revisores, el kappa ni los motivos de exclusión | Acepto | Se describe el cribado por dos revisores independientes con un tercero para desempates y se reporta el kappa de Cohen. El PRISMA incluye los motivos de exclusión por criterio. **Las cifras dependen del re-cribado** (pendiente de los autores). | §3.5; Fig. 1 | `datos_busqueda.tex` |
| 7 | Búsqueda no reproducible | Acepto | Las cadenas van en verbatim, con campos y filtros por base. Se justifica la incorporación de IEEE Xplore y el retiro de MDPI y T&F: son editoriales y sus revistas están indexadas en Scopus y WoS. Se usa TITLE-ABS-KEY en Scopus. La cadena se validó con un conjunto de control: recupera 19 de 21 estudios. **La fecha y los conteos dependen de la re-ejecución.** | §3.3, Tabla 4; Anexo A | `cadenas_busqueda.txt` |
| 8 | La comparación del PICOC no tiene RQ | Acepto | La C del PICOC se convierte en RQ6 (líneas base y ventaja reportada), con su columna en la extracción y una tabla de resultados. | Tabla 2; §4.9, Tabla 20 | Matriz: `baselines`, `ventaja_vs_mejor_baseline` |
| 9 | Síntesis solo por conteos | Acepto | Se añadió una tabla de características (21 estudios) y cruces de tipo de dato × familia, anomalía × familia y periodo × familia. La tendencia temporal ahora se apoya en el cruce: ningún estudio usa Transformers en 2020–2021, frente a 8 de 11 en 2024–2026. Se eliminó el Cuadro 12. | §4.2, §4.4, §4.6 | Tablas 8, 11, 12 y 17 |
| 10 | RQ2 solo enumera métricas | Acepto | RQ2 se reformuló para incluir el protocolo. Se extrajeron, por estudio, la procedencia de las etiquetas, la tasa de anomalías, la unidad de evaluación, el umbral y la partición. Se cuenta PR-AUC (2 estudios) y se comparan los resultados en datasets compartidos (PeMS, NYC taxi). | §4.5, Tablas 13–15 | Matriz: columnas de protocolo |
| 11 | La discusión no contrasta con otra evidencia y las amenazas son incompletas | Acepto | La discusión contrasta los hallazgos con las revisiones previas y con Taheri Sarteshnizi et al. Las amenazas se reescribieron: cadena sin validación externa, estudios solo recuperables a texto completo, aplicación no uniforme de criterios en la v1 y errores corregidos en las fichas. Se matizó la «madurez técnica». | §5 | — |
| 12 | Inclusiones límite sin justificar (E07, E02) | Acepto | CI-5 y CI-6 se precisaron con una cláusula para modelos híbridos y la exigencia de evaluar la detección misma. Se documenta la decisión de cada caso límite: 7 incluidos con justificación y 5 excluidos. | Tabla 5; Anexo C (Tabla 23) | `curacion.json` |
| 13 | Referencias incompletas | Acepto | Las referencias se rehicieron desde la primera página de cada PDF. Todas llevan DOI salvo AAMAS, que no tiene DOI y lleva URL de IFAAMAS. Correcciones principales: [Lu 2024] pp. 5051–5066; [Jadhav] vol. 16 (2026), art. 1516, título «multi-head + LSTM»; [Duan] art. 33573 (el título citado es el correcto); [Ren] art. 1247; [Chakraborty] pp. 1125–1134. | Referencias | `referencias.bib` |
| 14 | Restos de plantilla y autoría inconsistente | Acepto en parte | Se eliminó la afiliación 2 inexistente y se unificó el nombre del tercer autor como «Ender Prieto Quispe». **Pendiente:** el correo del tercer autor y las fechas reales del historial del protocolo. | Portada; Tabla 21 | — |
| 15 | Patrones de forma | Acepto | Se usa `es-tabla` (leyendas «Tabla»), se corrigió «la presente RSL» y se eliminaron los comentarios del proceso. «Crecimiento sostenido» se reemplazó por la distribución exacta por año, indicando que 2026 es parcial. Las cadenas van en verbatim. Se retiró la Fig. 1 de fases de Kitchenham. | Todo el texto | — |
| 16 | Sin registro, sin lista PRISMA, sin declaración de IA | Acepto | Se añadió la lista PRISMA 2020 con la ubicación de cada ítem (Anexo D, Tabla 24), un espacio para el registro OSF y una declaración de uso de IA generativa (a completar). La disponibilidad de datos apunta al repositorio de la RSL. **Pendiente:** registrar el protocolo en OSF. | Declaraciones; Anexo D | — |

## Correcciones detectadas durante la verificación contra los PDF

Al rehacer la extracción se encontraron errores en las fichas y en la versión 1 que conviene conocer:

- **Fichas duplicadas:** el artículo 10 y el 12 eran el mismo estudio (Mao et al.), y lo mismo ocurría con el 15 y el 16 (Giasemis). No había fichas de Zhao et al. (Multi-Adjacent) ni de Mehrannia et al.; se elaboraron desde el PDF.
- **E03 (Mao) y E13 (Cai):** sí reportan métricas cuantitativas de detección. Mao las da en la Tabla 2 y Cai precision, recall y F1 en la Fig. 8 y la Tabla 1. La observación 2(e) del revisor no se sostiene para estos dos estudios, aunque las definiciones de métricas de Mao no son estándar.
- **Datos reclasificados:**
  - Hu et al. usa matrices OD agregadas, no GPS.
  - En Huang et al., los resultados de casi-accidentes son sobre videos simulados.
  - En Lu et al., el 89,3 % corresponde solo a la categoría «road accidents»; la accuracy global es 85,4 %.
  - Choudhary y Hassani tiene DOI 10.1145/3605098.3636162, pp. 218–220.
- **Posibles problemas en estudios incluidos**, registrados en la matriz (campo `notas`) y considerados en la calidad:
  - AUC = 1,000 con anomalías inyectadas (Ren et al.).
  - Fuente de los datos multimodales no identificada (Duan et al.).
  - Inconsistencias entre texto y tablas (Fang, Jadhav, Khan, Abdallah).
