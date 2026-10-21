# Prompt para la lectura a texto completo (un PDF por vez)

Uso: abre un chat nuevo con la IA, adjunta **un** PDF (por ejemplo `R0024.pdf`), pega el prompt de abajo
cambiando `R0024` por el ID del PDF y envía. Luego verifica la respuesta contra el PDF y pega cada línea en
su hoja de `cribado/revision/REVISION_TEXTO_COMPLETO.xlsx` (ver «Cómo pegar» al final).

---

```text
Eres asistente de una revisión sistemática de la literatura (PRISMA 2020) titulada «Detección de
anomalías en tráfico vehicular mediante Deep Learning». Te adjunto el texto completo del estudio con
ID R0024. Léelo entero (incluidas tablas y figuras) y haz tres cosas: decidir su elegibilidad,
extraer los datos y evaluar su calidad. No inventes nada: si un dato no aparece en el PDF escribe
«No reportado». Toda evidencia es una frase corta copiada del PDF, en su idioma original, entre
comillas y con su página, p. ej. "we split the data chronologically" (p. 6).

=== PARTE 1. ELEGIBILIDAD A TEXTO COMPLETO ===
Aplica los criterios en este orden fijo y detente en el PRIMERO que no se cumpla:
1. CE-5: es revisión, survey, capítulo, tesis, resumen extendido, póster, editorial o preprint
   (arXiv, SSRN, TechRxiv…) sin versión revisada por pares.
2. CE-2: no trata de tráfico vehicular por carretera (excluye tráfico de red/ciberseguridad,
   intrusión en CAN-bus, peatones, tren, barco, avión, estado del pavimento, monitoreo del conductor
   dentro de la cabina).
3. CE-3: solo pronostica o clasifica el tráfico, o estima riesgo a largo plazo, sin detectar ni
   anticipar anomalías (accidentes, incidentes, congestión atípica, trayectorias o conductas
   anómalas, fallos de sensor).
4. CE-4: la detección no se basa en Deep Learning (SVM, ARIMA, reglas o umbrales sin una red
   profunda entrenada). En modelos híbridos se incluye si la red profunda aprende la representación
   sobre la que se decide la anomalía.
5. CI-6: no reporta una evaluación cuantitativa de la DETECCIÓN (p. ej., solo mide error de
   pronóstico MAE/RMSE, exactitud de reconocimiento de acciones o solo muestra ejemplos cualitativos).
6. CE-6: no describe el modelo, los datos o los resultados con detalle suficiente para extraerlos.
Si cumple todo: Incluir.

=== PARTE 2. EXTRACCIÓN (solo si es Incluir) ===
Usa EXACTAMENTE una de las opciones cuando se indican entre llaves:
- Tipo de dato {Sensores/detectores | Trayectorias GPS | Movilidad agregada | Video | Multimodal}
- Entorno {Urbano | Autopista | Ambos | No reportado}
- Datasets (nombre, país) — texto, p. ej. «PeMS (EE. UU.); NGSIM (EE. UU.)»
- Origen de etiquetas {Reales/registros | Anotación manual | Inyectadas/sintéticas |
  Pseudo-etiquetas | Sin etiquetas | No reportado}
- Tasa de anomalías — proporción de anomalías en los datos de evaluación, o «No reportada»
- Paradigma {Supervisado | Semi-supervisado | No supervisado | Auto-supervisado}
- Familia DL principal {Recurrente (RNN/LSTM/GRU) | Convolucional (CNN) | Grafos (GNN) |
  Atención/Transformer | Autoencoder/VAE | Generativo (GAN/difusión) | Otra}
- Arquitectura (nombre) — texto, p. ej. «ST-GCN + LSTM-AE»
- ¿Híbrido? {Sí | No} — Sí si combina dos o más familias
- Categoría de anomalía {Accidentes/incidentes | Congestión atípica | Trayectoria anómala |
  Comportamiento de conducción | Fallo de sensor/datos | Evento/otro}
- Métricas de detección — texto, p. ej. «F1, AUC-ROC, DR, FAR»
- Resultado principal — el mejor valor del modelo propuesto, p. ej. «F1 = 0.94 en PeMS»
- Unidad de evaluación — punto, ventana, evento, trayectoria, fotograma, video…
- Criterio de umbral — cómo decide que algo es anomalía (umbral fijo, percentil, clasificador…)
- Partición {Temporal | Aleatoria | Por ubicación | Prueba independiente | No reportada}
- Líneas base (cuántas y cuáles) — texto, p. ej. «5: LSTM, GRU, iForest, OCSVM, STGAN»
- ¿Línea base no DL? {Sí | No}
- Ventaja vs. mejor línea base — p. ej. «+3.2 puntos de F1 frente a STGAN», o «No reportada»
- Limitaciones que reportan — resumen en una frase, o «No reportadas»
- Código público (URL) — el enlace, o «No»

=== PARTE 3. CALIDAD QA1–QA8 (solo si es Incluir) ===
Cada ítem vale 1, 0.5 o 0 (usa punto decimal). La calidad no excluye el estudio.
- QA1 Etiquetas: 1 = registros reales o anotación verificada; 0.5 = mixtas, automáticas o
  verificación parcial; 0 = solo inyectadas o no reportado.
- QA2 Partición: 1 = temporal o prueba independiente descrita; 0.5 = aleatoria o descripción
  incompleta; 0 = no reportada.
- QA3 Líneas base: 1 = dos o más con el mismo protocolo, incluida una del estado del arte o no DL;
  0.5 = una sola o solo ablación; 0 = ninguna.
- QA4 Variabilidad: 1 = varias ejecuciones con desviación, intervalos o pruebas de significancia;
  0.5 = parcial; 0 = una sola ejecución.
- QA5 Código y datos: 1 = ambos públicos; 0.5 = uno de los dos; 0 = ninguno.
- QA6 Escenarios: 1 = dos o más datasets, ciudades o vías independientes; 0.5 = varios
  subconjuntos de un dataset; 0 = un único escenario.
- QA7 Protocolo: 1 = reporta la unidad de evaluación y el criterio de umbral o decisión;
  0.5 = solo uno; 0 = ninguno.
- QA8 Limitaciones: 1 = sección o párrafo explícito; 0.5 = mención breve; 0 = ninguna.

=== FORMATO DE RESPUESTA (obligatorio) ===
A) Primero, en 3–6 viñetas en español: qué propone el estudio y por qué decides Incluir o Excluir.

B) Después, TRES bloques de código, cada uno con UNA sola línea de valores separados por
   TABULADOR (sin encabezados, sin saltos de línea dentro de los valores, sin tabuladores dentro de
   un valor):

LINEA_HOJA1 (4 valores):
DECISIÓN TC | CRITERIO | EVIDENCIA (cita y página) | Comentario
  - Si es Incluir: CRITERIO vacío y EVIDENCIA con la cita que muestra la evaluación de la detección.
  - Si es Excluir: el código del criterio (CE-5, CE-2, CE-3, CE-4, CI-6 o CE-6) y la cita que lo prueba.
  - Comentario: tu motivo en una frase en español, empezando por «[Incluir]» o «[Excluir CE-x]».

LINEA_HOJA2 (20 valores, en el orden de la Parte 2). Si es Excluir, escribe solo: EXCLUIDO

LINEA_HOJA3 (16 valores: QA1, evidencia QA1, QA2, evidencia QA2, … QA8, evidencia QA8).
  Si es Excluir, escribe solo: EXCLUIDO

C) Al final, una línea «Dudas para el autor:» con lo que no pudiste confirmar en el PDF (o «Ninguna»).
```

---

## Qué tiene que devolverte

1. **Viñetas** con el resumen y el motivo de la decisión.
2. **Tres bloques**, cada uno con una línea:
   - **Hoja 1** (4 valores): `Incluir ⇥ ⇥ "…we report F1…" (p. 7) ⇥ [Incluir] Detecta incidentes en PeMS con LSTM-AE y F1.`
   - **Hoja 2** (20 valores) o `EXCLUIDO`.
   - **Hoja 3** (16 valores: puntaje y evidencia de QA1…QA8) o `EXCLUIDO`.
3. **Dudas para el autor**.

## Cómo pegar en el Excel

1. Abre `REVISION_TEXTO_COMPLETO.xlsx` y busca la fila del ID (p. ej. R0024).
2. **Hoja 1_TextoCompleto**: clic en la celda de la columna **E (DECISIÓN TC)** de esa fila → copia la línea del
   bloque «Hoja 1» → Ctrl+V. Los 4 valores se reparten solos en E, F, G, H.
3. **Hoja 2_Extraccion**: clic en la columna **E** de la misma fila → pega la línea de la «Hoja 2» (E a X).
4. **Hoja 3_Calidad**: clic en la columna **E** → pega la línea de la «Hoja 3» (E a T). El TOTAL se calcula solo.
5. Si se pega todo en una sola celda, la IA no usó tabuladores: pídele «repite los bloques B separados por
   tabulador».

## Antes de pegar, verifica tú (2–3 minutos por artículo)

- Abre el PDF en la página de cada cita y comprueba que la frase existe y dice eso.
- Si es Excluir: ¿es de verdad el **primer** criterio del orden que falla?
- QA4 y QA5 son los que más se equivocan: busca «runs», «standard deviation», «github», «code is available».
- Si cambias algo, cámbialo en el Excel directamente. La IA solo propone; la decisión es tuya.
