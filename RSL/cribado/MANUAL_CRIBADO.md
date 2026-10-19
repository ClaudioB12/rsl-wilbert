# Manual de cribado — RSL «Detección de anomalías en tráfico vehicular mediante Deep Learning»

Versión 2.0 del protocolo. Los dos revisores **deben leer este manual completo antes del piloto** y tenerlo abierto durante todo el cribado. Si en la reunión de consenso se precisa una definición, **se anota aquí** (sección 7) y en el historial del protocolo del manuscrito.

---

## 1. De dónde salen los criterios (fundamento)

Los criterios no son arbitrarios: cada uno se deriva de un componente del protocolo (PICOC) o de una pregunta de investigación (RQ). Esa trazabilidad es lo que el revisor del artículo exige (Kitchenham y Charters, 2007, §6.2: los criterios de selección se derivan de las preguntas de investigación; PRISMA 2020, ítem 5).

| Código | Criterio | Fundamento | Se puede juzgar en… |
|---|---|---|---|
| CI-1 / CE-5 | Estudio primario revisado por pares (revista o conferencia). Se excluyen revisiones, surveys, capítulos, tesis, resúmenes, pósteres, editoriales y preprints | Calidad mínima de la evidencia; una RSL sintetiza estudios **primarios** | Título y resumen |
| CI-2 | Inglés o español, con texto completo accesible | Viabilidad: la extracción requiere leer el texto completo | Título y resumen (idioma) / texto completo (acceso) |
| CI-3 | Publicado entre 2020 y 2026 | Contexto (C) del PICOC: periodo del DL reciente, que las revisiones previas no cubren | Título y resumen |
| CI-4 / CE-2 | Tráfico **vehicular por carretera** (urbano o autopista), observado con sensores, trayectorias, datos de movilidad o video | Población (P) del PICOC; RQ3 y RQ4 | Título y resumen |
| CE-3 | Debe **detectar o anticipar anomalías**, no solo pronosticar o clasificar el tráfico | Resultado (O) y objetivo de la RSL | Título y resumen (si es claro) / texto completo |
| CI-5 / CE-4 | El **Deep Learning** es el método principal de la detección | Intervención (I); RQ1 | Título y resumen (si es claro) / texto completo |
| CI-6 | Reporta una **evaluación cuantitativa de la detección** | Resultado (O); RQ2 y RQ6 necesitan métricas | Solo texto completo |
| CE-6 | Describe modelo, datos y resultados lo suficiente para extraerlos | Viabilidad de la extracción (formulario de la Tabla 6) | Solo texto completo |
| CE-1 | Duplicado, o versión menos completa del mismo estudio | Evitar contar dos veces la misma evidencia | Ambas etapas |

---

## 2. Árbol de decisión (aplicar SIEMPRE en este orden)

Se recorre de arriba abajo. **La primera pregunta que se responda «Sí» determina el criterio de exclusión.** Así, dos revisores que excluyen el mismo artículo asignan el mismo código, y el PRISMA reporta motivos coherentes.

```
 1. ¿Es el mismo estudio que otro registro ya visto (o una versión menos completa)? ...... Sí → Excluir CE-1
 2. ¿Es revisión/survey, capítulo, tesis, resumen, póster, editorial o preprint? .......... Sí → Excluir CE-5
 3. ¿Se publicó fuera de 2020-2026? .................................................... Sí → Excluir CI-3
 4. ¿Está en un idioma distinto de inglés o español? .................................... Sí → Excluir CI-2
 5. ¿El objeto de estudio NO es el tráfico vehicular por carretera? ....................... Sí → Excluir CE-2
 6. ¿NO detecta ni anticipa anomalías del tráfico (solo pronóstico, clasificación, riesgo)?  Sí → Excluir CE-3
 7. ¿La detección NO usa Deep Learning como método principal? ............................ Sí → Excluir CE-4
    ───────────── hasta aquí en TÍTULO Y RESUMEN: si pasa todo o hay duda → Incluir / Duda
 8. ¿No se consigue el texto completo? ............................................... Sí → «No recuperado»
 9. ¿No evalúa CUANTITATIVAMENTE la detección? ........................................ Sí → Excluir CI-6
10. ¿No describe modelo, datos o resultados lo suficiente para la extracción? ........... Sí → Excluir CE-6
11. Pasó todo .................................................................................. Incluir
```

### Reglas de oro

- **Título y resumen: ante la duda, NO se excluye.** Se marca **Duda**, que pasa a texto completo igual que *Incluir*. Excluir algo relevante por error es irreversible (se pierde para siempre); incluir de más solo cuesta leer un PDF. Es la práctica recomendada en el *Cochrane Handbook*, cap. 4.
- Se excluye en título y resumen **solo si el incumplimiento es claro en el texto que se lee**. «No menciona Deep Learning en el resumen» **no** es suficiente para CE-4 si el título o el resumen sugieren un modelo aprendido: márquenlo como Duda.
- **Texto completo: toda exclusión lleva una cita.** En la columna EVIDENCIA copien la frase del artículo que justifica la decisión, con página o sección. Por ejemplo: `p. 7, Sec. 5.2: "the detection results are shown qualitatively in Fig. 9"` → CI-6. Esto es lo que da fundamento ante el ingeniero (PRISMA 2020, ítem 16b).
- **Las «señales automáticas» de la hoja son solo un apoyo.** Avisan de palabras clave sospechosas, pero se equivocan: por ejemplo, «vehicle» puede referirse a un vehículo autónomo y «attention» puede no ser un Transformer. **Nunca decidan solo por la señal.**
- **Cada revisor trabaja solo.** No se consulten durante el cribado. Las diferencias se resuelven después, en la reunión de consenso.

---

## 3. Definiciones operativas y ejemplos

### CE-5 / CI-1 — Tipo de documento
**Se incluyen:** artículos de revista y artículos completos de conferencia revisados por pares (por ejemplo, IEEE ITSC, ACM SIGSPATIAL, KDD, AAMAS).
**Se excluyen (CE-5):**
- revisiones, surveys y mapeos sistemáticos (se citan en la introducción, pero no son estudios primarios);
- capítulos de libro, tesis, resúmenes extendidos de una página, pósteres, editoriales, erratas, tutoriales y descripciones de competiciones sin método propio;
- **preprints** (arXiv, SSRN, TechRxiv) **salvo** que exista la versión revisada por pares. En ese caso se incluye y se cita la versión publicada: busquen el título en Google Scholar y revisen «Todas las versiones».

> Caso real: Giasemis y Sopasakis (2025), arXiv → excluido por CE-5 en la v2. La planilla de Parsif.al enlazaba un documento de IEEE Xplore; si es la versión publicada y la búsqueda la recupera, se incluye esa versión.

### CI-3 — Periodo
Se usa el **año de publicación de la versión final** (volumen o número). Si el artículo salió en línea en 2019 y en un número de 2020, cuenta como 2020. El año 2026 se incluye hasta la fecha de búsqueda.

### CI-2 — Idioma y acceso
Inglés o español. La falta de acceso **no** es CI-2 en título y resumen: el artículo pasa y, si a texto completo no se consigue tras intentarlo con la biblioteca UPeU, Google Scholar, ResearchGate y un correo al autor, se marca **«No recuperado»**. PRISMA lo reporta en una casilla aparte.

### CE-2 — No es tráfico vehicular por carretera
**Sí es tráfico vehicular (pasa):**
- flujo, velocidad u ocupación de detectores en vías urbanas o autopistas;
- trayectorias de vehículos (GPS de taxis, flotas, seguimiento en video);
- datos de movilidad agregada u origen-destino de vehículos;
- video de cámaras de tráfico, de dron o de dashcam que observa la vía;
- conducción anómala de **otros** vehículos vista desde un vehículo autónomo (por ejemplo, Chakraborty et al. 2023, incluido).

**No es tráfico vehicular (CE-2):**
- tráfico de **redes informáticas**, detección de intrusiones, ataques al CAN-bus del vehículo o VANET (es ciberseguridad);
- peatones o multitudes sin vehículos;
- transporte marítimo (AIS), aéreo, ferroviario o metro, y bicicletas como único objeto;
- **estado del conductor** (somnolencia, distracción o emociones): es monitoreo del conductor, no anomalía del tráfico;
- **estado del pavimento** (baches, fisuras) o de señales de tránsito (es infraestructura física, no tráfico);
- fallos de **percepción** del vehículo autónomo (objetos fuera de distribución en el detector): es robustez del sensor, no anomalía del tráfico.

### CE-3 — No detecta ni anticipa anomalías
**Pasa** si el objetivo incluye identificar, en datos observados, un evento o patrón anómalo del tráfico:
- accidentes e incidentes;
- congestión **no recurrente**;
- conducción peligrosa (contramano, exceso de velocidad, cambios de carril peligrosos, casi accidentes);
- cierres de vías y disrupciones (eventos extremos, clima, fallos de detectores **observados en los datos de tráfico**);
- trayectorias anómalas;
- la **anticipación** a corto plazo (segundos o minutos) de un accidente en video o en datos.

**CE-3** si:
- solo **pronostica** flujo o velocidad, aunque mencione «robusto a outliers» o use atípicos como paso intermedio (por ejemplo, Choudhary y Hassani 2024, excluido: solo evalúa el RMSE del pronóstico);
- solo **clasifica** estados normales del tráfico (nivel de congestión diario, tipo de vehículo) sin noción de anomalía;
- modela el **riesgo o la frecuencia de accidentes a largo plazo** con datos históricos (análisis de seguridad vial, *crash frequency models*): no detecta un evento en curso;
- solo **imputa** datos faltantes.

> Caso límite: AIP-Urban (Abdallah y Alghamdi 2025) busca el mantenimiento predictivo, pero clasifica ventanas como normales o anómalas y evalúa esa detección con F1. **Pasa.**

### CE-4 / CI-5 — Deep Learning como método principal
**Es DL:** redes neuronales profundas entrenadas por los autores o ajustadas por ellos (*fine-tuning*). Por ejemplo: CNN, 3D-CNN, TCN, RNN, LSTM, GRU, autoencoders y VAE, GNN, GCN, GAT, Transformers, GAN, modelos de difusión y modelos visión-lenguaje (CLIP).
**No es DL (CE-4):**
- SVM, Random Forest, XGBoost, k-NN, Isolation Forest y LOF;
- ARIMA, filtros de Kalman, umbrales estadísticos y reglas;
- un MLP de una sola capa oculta;
- una ELM sola.

**Regla para híbridos:** se incluye si **una componente profunda entrenada aprende la representación sobre la que se decide la anomalía**, aunque la decisión final la tome un umbral o una regla.
- Ejemplo incluido: una CNN cíclica que extrae características y una ELM que clasifica (Fang et al. 2020).
- Ejemplo incluido: CNN+LSTM que predicen el flujo y una regla que compara predicción y observación (Cai et al. 2021).
- Ejemplo incluido: detección, seguimiento y re-identificación con DL más una BiLSTM, con reglas sobre las trayectorias resultantes (Zhao et al. 2024).

**Se excluye (CE-4)** cuando:
- el DL es solo un preprocesamiento estándar no central (por ejemplo, un YOLO preentrenado que solo cuenta vehículos, seguido de un ARIMA que detecta la anomalía);
- el método propuesto no es DL y el DL aparece solo como línea base de comparación (por ejemplo, Taheri Sarteshnizi et al. 2026, excluido).

### CI-6 — Evaluación cuantitativa de la detección (solo texto completo)
**Pasa** si reporta al menos una métrica calculada **sobre la tarea de detección** frente a una referencia:
- accuracy, precision, recall, F1, AUC-ROC, PR-AUC, tasa de detección, falsas alarmas o tiempo de detección;
- conteos de aciertos y errores frente a eventos conocidos, como en Jia et al. 2025, que da 29 de 30 contra una referencia.

**CI-6** si la detección solo se muestra de forma cualitativa (figuras, casos de estudio) o si las únicas métricas son de **otra tarea**:
- RMSE del pronóstico;
- precisión en reconocimiento de acciones de Kinetics (Feng et al. 2021, excluido);
- error de imputación (Nouri e Ilbeigi 2025, excluido).

### CE-6 — Información insuficiente (solo texto completo)
Excluir solo si **no se puede llenar el formulario de extracción**: no se sabe qué modelo se usó, con qué datos ni qué resultados obtuvo. Un artículo con descripciones pobres pero suficientes **se incluye**, y su debilidad se refleja en la evaluación de calidad, no aquí.

### CE-1 — Duplicados y versiones
- El script 02 elimina los duplicados exactos (DOI o título). Si en el cribado ven dos registros del **mismo estudio** que el script no detectó (por ejemplo, el título cambia levemente), excluyan el menos completo con CE-1 e indiquen en el comentario el ID del que se conserva.
- **Conferencia ampliada luego en revista** por los mismos autores, con los mismos datos y el mismo método: se conserva la de revista (más completa) y la otra se excluye con CE-1. Si la versión de revista aporta experimentos nuevos, se usa solo esa.

---

## 4. Procedimiento paso a paso

1. **Piloto (calibración):** ambos revisores criban los mismos 50 registros al azar (script 03 `--piloto 50`).
   - Si κ ≥ 0,60, se sigue.
   - Si κ < 0,60, se discuten los desacuerdos, se precisa este manual (sección 7) y se repite con otra muestra.
2. **Título y resumen:** cada revisor criba todos los registros en su hoja. Los registros del piloto vienen ya decididos.
3. **Consenso TA:** reunión de los dos revisores sobre los registros en rojo. Si no hay acuerdo, decide el tercer revisor. Se anota el porqué en la nota.
4. **Texto completo:** se consiguen los PDF y cada revisor decide con el árbol completo, **con evidencia textual** para cada exclusión.
5. **Consenso TC:** igual que en TA. Cuidado con los registros marcados «criterio distinto»: ambos excluyen, pero hay que acordar **un solo** criterio, el primero que falla en el árbol.
6. **Registro en Parsif.al:** se marca la decisión de consenso de cada registro (archivo `06_estado_para_parsifal.csv`).

### Cómo se mide el acuerdo
Se usa el kappa de Cohen, que corrige el acuerdo que se daría por azar. En título y resumen, *Incluir* y *Duda* cuentan como «pasa». Interpretación (Landis y Koch, 1977):

| κ | Acuerdo |
|---|---|
| < 0,20 | pobre |
| 0,21–0,40 | débil |
| 0,41–0,60 | moderado |
| 0,61–0,80 | bueno |
| > 0,80 | muy bueno |

Se reporta lo que salga, aunque sea bajo; ocultarlo sería peor. Un κ bajo en texto completo suele indicar que un criterio está mal definido: discútanlo y precisen el manual.

---

## 5. Reunión de consenso (cómo se hace bien)

1. Abran `salida/consolidado_<etapa>.xlsx` y filtren la columna ACUERDO por «NO» y por «criterio distinto».
2. Para cada registro, cada revisor explica su decisión **citando el criterio y el texto**. Se busca la regla del manual que aplica, no se vota.
3. Si el caso no está cubierto por el manual, se acuerda una regla, se **escribe en la sección 7** y se aplica a todos los casos parecidos, incluso a los ya decididos. Así se evitan los «criterios aplicados de forma selectiva» que señaló el ingeniero.
4. Si no hay acuerdo, decide el tercer revisor.
5. Se escribe la DECISIÓN FINAL, el CRITERIO FINAL, la EVIDENCIA FINAL (en texto completo) y una nota breve.

---

## 6. Errores frecuentes

| Error | Por qué está mal | Correcto |
|---|---|---|
| Excluir en título y resumen «porque no dice qué red usa» | Falta de información no es incumplimiento | Duda → texto completo |
| Excluir un survey con CE-3 | El primer criterio que falla en el árbol es CE-5 | CE-5 |
| Excluir un artículo de tráfico de redes con CE-4 porque usa SVM | El primer criterio que falla es CE-2 | CE-2 |
| Incluir un pronóstico de flujo «porque menciona outliers» | No evalúa la detección | CE-3 (o CI-6 a texto completo) |
| Excluir a texto completo sin cita | No es verificable ni defendible | Siempre con evidencia |
| Cambiar la regla a mitad del cribado sin anotarla | Aplicación no uniforme de criterios | Anotar en la sección 7 y reaplicar |

---

## 7. Registro de aclaraciones acordadas durante el cribado

| Fecha | Situación | Regla acordada | Aplica a (IDs) |
|---|---|---|---|
| | | | |

---

### Referencias del manual
- Kitchenham, B., y Charters, S. (2007). *Guidelines for performing systematic literature reviews in software engineering* (EBSE 2007-001).
- Page, M. J. et al. (2021). The PRISMA 2020 statement. *BMJ*, 372, n71.
- Lefebvre, C. et al. (2023). Chapter 4: Searching for and selecting studies. En *Cochrane Handbook for Systematic Reviews of Interventions* (v6.4).
- Landis, J. R., y Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics*, 33(1), 159–174.
- Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, 20(1), 37–46.
