# Parsif.al desde cero — textos para copiar y pegar

Cada bloque gris se copia completo (Ctrl+C) y se pega (Ctrl+V) en el campo de Parsif.al que indica el título. Sigue el orden de arriba abajo. Los nombres de los menús están en inglés, como aparecen en Parsif.al.

> Si algo de Parsif.al no coincide con lo que dice aquí (un botón con otro nombre, un campo que falta), mándame una captura y lo ajustamos.

---

## 1. Crear la revisión

1. Entra a https://parsif.al e inicia sesión.
2. Botón **«New review»** (o «Create a new review»).
3. **Title:**
```
Detección de anomalías en tráfico vehicular mediante Deep Learning a partir de datos de sensores, trayectorias y video: una revisión sistemática de la literatura (v2)
```
4. **Description:**
```
Revisión sistemática (Kitchenham y Charters, 2007; reporte PRISMA 2020 y PRISMA-S) sobre modelos de Deep Learning para detectar anomalías en tráfico vehicular urbano y de autopista (accidentes e incidentes, congestión no recurrente, conducción peligrosa, cierres y disrupciones), a partir de datos de sensores, trayectorias GPS, movilidad agregada y video. Periodo 2020-2026. Fuentes: Scopus, Web of Science, IEEE Xplore, ScienceDirect y ACM Digital Library. Versión 2 del protocolo, en respuesta al reporte de revisión.
```
5. **Save / Create.** No agregues coautores: eres autor único.

---

## 2. PLANNING

### 2.1 Objectives
```
Objetivo general: sintetizar los modelos de Deep Learning empleados para detectar anomalías en tráfico vehicular urbano y de autopista, junto con las métricas y los protocolos de evaluación, los tipos de anomalía, los conjuntos de datos, las líneas base de comparación y las limitaciones reportadas en estudios primarios publicados entre 2020 y 2026.

Objetivos específicos:
1. Identificar las técnicas de Deep Learning utilizadas y su relación con el tipo de dato (RQ1).
2. Analizar las métricas y los protocolos de evaluación: procedencia de etiquetas, umbral, unidad de evaluación y partición (RQ2).
3. Clasificar los tipos de anomalías de tráfico abordados (RQ3).
4. Examinar los conjuntos de datos utilizados y el tipo de etiquetas (RQ4).
5. Determinar las limitaciones y desafíos reportados (RQ5).
6. Identificar las líneas base de comparación y la ventaja reportada por los modelos de Deep Learning (RQ6).
```

### 2.2 PICOC
**Population:**
```
Tráfico vehicular en redes urbanas y autopistas, observado mediante sensores fijos, trayectorias GPS, datos de movilidad agregada u origen-destino, o video de vigilancia.
```
**Intervention:**
```
Modelos de Deep Learning (recurrentes, convolucionales, autoencoders, redes de grafos, Transformers, generativos o híbridos) usados como método principal para detectar anomalías.
```
**Comparison:**
```
Líneas base reportadas por cada estudio: otros modelos de Deep Learning, aprendizaje automático convencional, métodos estadísticos o reglas (RQ6).
```
**Outcome:**
```
Desempeño de detección y protocolo con que se mide: métricas, procedencia de etiquetas, umbral, unidad de evaluación y partición de los datos.
```
**Context:**
```
Sistemas inteligentes de transporte; estudios primarios revisados por pares publicados entre 2020 y 2026.
```

### 2.3 Research Questions (agrega una por una)
```
RQ1: ¿Qué técnicas de Deep Learning se han utilizado para detectar anomalías en tráfico vehicular urbano y de autopista, y cómo se relacionan con el tipo de dato?
```
```
RQ2: ¿Qué métricas y qué protocolos de evaluación (procedencia de etiquetas, umbral, unidad de evaluación y partición) se emplean para medir el rendimiento de estos modelos?
```
```
RQ3: ¿Qué tipos de anomalías de tráfico se han abordado?
```
```
RQ4: ¿Qué conjuntos de datos se han utilizado y con qué tipo de etiquetas?
```
```
RQ5: ¿Qué limitaciones y desafíos reportan los estudios?
```
```
RQ6: ¿Contra qué líneas base se comparan los modelos de Deep Learning y qué ventaja reportan?
```

### 2.4 Keywords & Synonyms (una fila por palabra clave)

| Keyword (copia esto) | Synonyms (copia esto) |
|---|---|
| `anomaly detection` | `anomal*, abnormal*, outlier detection, incident detection, accident detection, accident prediction, accident anticipation, road closure, dangerous driving, near-accident, near-miss, extreme event` |
| `deep learning` | `deep neural, neural network*, LSTM, GRU, CNN, convolutional, autoencoder*, transformer*, graph neural, self-attention, attention mechanism` |
| `vehicular traffic` | `road traffic, urban traffic, highway traffic, freeway traffic, expressway traffic, traffic flow, traffic speed, traffic volume, traffic data, traffic monitoring, traffic video, traffic surveillance, traffic camera, traffic scene, traffic scenario, traffic event, traffic incident, traffic accident, traffic anomaly, traffic congestion, road accident, road closure, intelligent transportation, transportation network, road network, vehicle trajectory, vehicle behavior, driving behavior, taxi` |

### 2.5 Search String → «Base String» (cadena genérica v2.1)
Si ya habías pegado la anterior, **reemplázala** por esta:
```
(anomal* OR abnormal* OR "outlier detection" OR "incident detection" OR "accident detection" OR "accident prediction" OR "accident anticipation" OR "road closure*" OR "dangerous driving" OR "near-accident*" OR "near-miss*" OR "extreme event*") AND ("deep learning" OR "deep neural" OR "neural network*" OR LSTM OR GRU OR CNN OR convolutional OR autoencoder* OR transformer* OR "graph neural" OR "self-attention" OR "attention mechanism") AND ("road traffic" OR "urban traffic" OR "vehicular traffic" OR "highway traffic" OR "freeway traffic" OR "expressway traffic" OR "traffic flow*" OR "traffic speed" OR "traffic volume*" OR "traffic data" OR "traffic monitoring" OR "traffic video*" OR "traffic surveillance" OR "traffic camera*" OR "traffic scene*" OR "traffic scenario*" OR "traffic event*" OR "traffic incident*" OR "traffic accident*" OR "traffic anomal*" OR "traffic congestion" OR "road accident*" OR "road closure*" OR "intelligent transportation" OR "transportation network*" OR "road network*" OR "vehicle trajector*" OR "vehicle behavio*" OR "driving behavio*" OR taxi*)
```

### 2.5.1 Cadenas específicas por base (botón «Add source-specific search string»)
Pulsa el botón una vez por base, elige la fuente y pega la cadena de su sección en `RSL\suplementos\cadenas_busqueda.txt`:

| Fuente | Sección del archivo |
|---|---|
| Scopus | «## Scopus» (empieza con `TITLE-ABS-KEY`) |
| Web of Science | «## Web of Science» (empieza con `TS=`) |
| IEEE Xplore | «## IEEE Xplore»: pega las **Consultas 1, 2 y 3**, una debajo de otra |
| ScienceDirect | «## ScienceDirect»: pega las **Consultas 1 a 5**, una debajo de otra |
| ACM Digital Library | «## ACM Digital Library» |

> **No uses la búsqueda automática de Parsif.al** (la integración con Scopus y ScienceDirect). Haz cada búsqueda en la web de la base y exporta, como indica la Parte 2 de la guía. Así obtienes el número exacto de resultados, la captura de pantalla y los resúmenes.

### 2.6 Sources
Agrega estas cinco. Si en tu proyecto aparecen MDPI o Taylor & Francis, **quítalos**.

| Nombre | URL |
|---|---|
| `Scopus` | `https://www.scopus.com` |
| `Web of Science` | `https://www.webofscience.com` |
| `IEEE Xplore` | `https://ieeexplore.ieee.org` |
| `ScienceDirect` | `https://www.sciencedirect.com` |
| `ACM Digital Library` | `https://dl.acm.org` |

En cada fuente, en el campo de la cadena (*search string* de la fuente), pega la cadena exacta de esa base. Están en `RSL\suplementos\cadenas_busqueda.txt`, en las secciones «## Scopus», «## Web of Science», etc.

### 2.7 Selection Criteria
**Inclusion criteria** (agrega uno por uno):
```
CI-1: Artículo de revista o de conferencia revisado por pares.
```
```
CI-2: En inglés o español, con acceso al texto completo.
```
```
CI-3: Publicado entre 2020 y 2026.
```
```
CI-4: Aborda la detección de anomalías en tráfico vehicular (urbano o de autopista) a partir de sensores, trayectorias, datos de movilidad o video.
```
```
CI-5: Usa Deep Learning como método principal de la detección; en modelos híbridos, la componente profunda aprende la representación sobre la que se decide la anomalía.
```
```
CI-6: Reporta una evaluación cuantitativa de la tarea de detección (no solo de una tarea auxiliar como pronóstico o reconocimiento de acciones).
```
**Exclusion criteria** (agrega uno por uno):
```
CE-1: Duplicado entre bases, o versión menos completa del mismo estudio; se conserva la más completa.
```
```
CE-2: No trata de tráfico vehicular por carretera (tráfico de red, ciberseguridad del vehículo, peatones, transporte marítimo, aéreo o ferroviario, estado del pavimento, monitoreo del conductor).
```
```
CE-3: Solo pronostica o clasifica tráfico, o estima riesgo a largo plazo, sin detectar ni anticipar anomalías.
```
```
CE-4: La detección no se basa en Deep Learning (SVM, ARIMA, reglas o umbrales sin componente profunda entrenada).
```
```
CE-5: Revisión, survey, capítulo, tesis, resumen, póster, editorial o preprint sin versión revisada por pares.
```
```
CE-6: No describe el modelo, los datos o los resultados de forma suficiente para la extracción.
```

### 2.8 Quality Assessment Checklist
**Answers** (crea estas tres, con su peso):

| Answer | Weight |
|---|---|
| `Sí` | `1` |
| `Parcial` | `0.5` |
| `No` | `0` |

**Questions** (agrega una por una):
```
QA1. ¿Las etiquetas de anomalía provienen de registros reales o de anotación verificada? (Sí: registros reales o anotación verificada; Parcial: mixtas, automáticas o verificación parcial; No: solo inyectadas o no reportado)
```
```
QA2. ¿La partición de los datos evita la fuga de información? (Sí: partición temporal o prueba independiente descrita; Parcial: partición aleatoria o descripción incompleta; No: no reportada)
```
```
QA3. ¿Compara con líneas base bajo el mismo protocolo? (Sí: dos o más, incluida una del estado del arte o no DL; Parcial: una sola o solo ablación; No: ninguna)
```
```
QA4. ¿Reporta la variabilidad de los resultados? (Sí: varias ejecuciones con dispersión, intervalos o pruebas de significancia; Parcial: parcial; No: una sola ejecución)
```
```
QA5. ¿El código y los datos están disponibles? (Sí: ambos públicos; Parcial: uno de los dos; No: ninguno)
```
```
QA6. ¿Valida en más de un escenario independiente? (Sí: dos o más datasets, ciudades o vías; Parcial: varios subconjuntos de un dataset; No: un único escenario)
```
```
QA7. ¿El protocolo de evaluación es explícito? (Sí: reporta la unidad de evaluación y el criterio de umbral o decisión; Parcial: solo uno; No: ninguno)
```
```
QA8. ¿Declara sus limitaciones? (Sí: sección o párrafo explícito; Parcial: mención breve; No: ninguna)
```
**Cutoff score:** `0`. La calidad no se usa para excluir estudios, solo se reporta y se usa en el análisis de sensibilidad.

### 2.9 Data Extraction Form
Agrega cada campo con su tipo. *Select One* y *Select Many* llevan las opciones indicadas, separadas por coma.

| Field (descripción) | Type | Opciones |
|---|---|---|
| `Base(s) de recuperación` | String | |
| `País o región de los datos` | String | |
| `Entorno vial` | Select One | `Urbano, Autopista, Ambos, No especificado` |
| `Tipo de dato` | Select One | `Series de sensores, Movilidad agregada/OD, Trayectorias, Video e imágenes, Multimodal, Simulado` |
| `Datasets utilizados` | String | |
| `Procedencia de las etiquetas` | Select One | `Registros reales de incidentes, Anotación manual o experta, Benchmark anotado por terceros, Anomalías inyectadas o sintéticas, Mixto o automático, Sin etiquetas, No reportado` |
| `Proporción de anomalías` | String | |
| `Familias de arquitectura` | Select Many | `Recurrente, Convolucional, Autoencoder, Grafos, Transformer/atención, Generativo` |
| `Modelo híbrido` | Boolean | |
| `Datos multimodales` | Boolean | |
| `Paradigma` | Select One | `Supervisado, Semisupervisado, No supervisado, Autosupervisado` |
| `Mecanismo de detección` | Select One | `Predicción, Reconstrucción, Clasificación, Similitud/contraste, Otro` |
| `Unidad de evaluación` | Select One | `Punto/instante, Ventana, Frame, Clip/video, Evento, Trayectoria, No reportado` |
| `Criterio de umbral o decisión` | String | |
| `Partición de los datos` | String | |
| `Métricas reportadas` | Select Many | `Accuracy, Precision, Recall, F1-score, AUC-ROC, PR-AUC, Tasa de detección, FAR/FPR, Tiempo medio de detección, MAE/RMSE/MAPE, IoU/mAP, Latencia/FPS/energía` |
| `Resultado principal` | String | |
| `Líneas base` | String | |
| `Incluye línea base no DL` | Boolean | |
| `Ventaja frente a la mejor línea base` | String | |
| `Categoría de anomalía (principal)` | Select One | `Accidentes e incidentes, Congestión o flujo anómalo, Trayectorias o conducción peligrosa, Disrupciones y eventos extremos` |
| `Limitaciones declaradas` | Select Many | `Datos propios o de acceso limitado, Etiquetado de anomalías, Generalización, Métricas no comparables, Costo computacional y despliegue, Interpretabilidad` |
| `Código disponible (URL)` | String | |

> Para los 21 estudios ya incluidos, todos estos datos están en `RSL\suplementos\matriz_extraccion.xlsx`, hoja «Matriz». Puedes copiarlos de ahí a Parsif.al.

---

## 3. CONDUCTING

### 3.1 Search → importar estudios
Esto se hace **después** del paso 2 de la guía (los scripts 01 y 02).
1. Ve a **Conducting → Search** (o *Import studies*).
2. Para cada fuente, botón **«Import BibTeX»**, eligiendo el archivo de esa base en `RSL\cribado\salida\parsifal\`:
   - Scopus → `Scopus.bib`
   - Web of Science → `WoS.bib`
   - IEEE Xplore → `IEEE.bib`
   - ScienceDirect → `ScienceDirect.bib`
   - ACM Digital Library → `ACM.bib`
3. Comprueba que el número de estudios de cada fuente coincida con lo que imprimió el script 02.

Estos archivos ya vienen **sin duplicados**. Cada estudio lleva su ID (R0001…) en el campo *note*, para encontrarlo luego.

### 3.2 Study Selection
Se llena **al final del cribado**, con `RSL\cribado\salida\06_estado_para_parsifal.csv` (ábrelo en Excel):
- `Accepted` → márcalo **Accepted**.
- `Rejected` → márcalo **Rejected**, y en el comentario pega el criterio:
```
Excluido en título y resumen por CE-3 (ver cribado/salida/decision_TA.json)
```
```
Excluido a texto completo por CI-6. Evidencia: [pega aquí la cita de la columna «evidencia»]
```

### 3.3 Quality Assessment
Para cada estudio aceptado, responde QA1–QA8 con el puntaje de `RSL\cribado\revision\calidad.xlsx` (columna «TU PUNTAJE»).

### 3.4 Data Extraction
Copia los datos de `RSL\suplementos\matriz_extraccion.xlsx` (hoja «Matriz»).

---

## 4. REPORTING
En **Reporting** (o *Export*), descarga el protocolo y los resultados en PDF o Word. Ese archivo es el que se sube a OSF (Parte 9 de la guía).
