# Guía para revisar el cribado por título y resumen

Revisas **151 aceptados** (todos) y **57 rechazados** (los de confianza media). La lista completa, con resumen, DOI, enlace al PDF gratuito y Google Scholar, está en **`RSL/cribado/revision/LISTA_REVISION_TA.xlsx`**. Las tablas del final de esta guía son la misma lista, para verla rápido.

---

## 1. Cómo encontrar cada artículo en Parsif.al

1. Ve a **Conducting → Study Selection → All Sources**.
2. Pulsa **Ctrl + F** (buscar en la página), pega 4 o 5 palabras del título y pulsa Enter. Chrome resalta la fila.
3. Haz clic en la fila. Se abre la ficha (*Article Details*):
   - **Details:** título, resumen, **Status** y **Selection criteria**.
   - **Comments:** el comentario.
4. Decide, escribe el comentario final y pulsa **Save**.

---

## 2. Con qué criterios decides (en este orden; la primera respuesta «sí» manda)

| Paso | Pregunta | Si la respuesta es «sí» |
|---|---|---|
| 1 | ¿Es el mismo estudio que otro de la lista (otra versión)? | Excluir **CE-1** (indica el ID que se conserva) |
| 2 | ¿Es revisión, survey, volumen de actas, capítulo, tesis, editorial, erratum, póster, resumen extendido o preprint? | Excluir **CE-5** |
| 3 | ¿Se publicó fuera de 2020–2026? | Excluir **CI-3** |
| 4 | ¿No está en inglés o español, o no es de acceso abierto? | Excluir **CI-2** |
| 5 | ¿El objeto NO es el tráfico vehicular por carretera? (redes informáticas, ciberseguridad/CAN/VANET, peatones o multitudes sin vehículos, marítimo, aéreo, ferroviario, metro, **estado del conductor** —fatiga, distracción, emociones—, pavimento o señales) | Excluir **CE-2** |
| 6 | ¿NO detecta ni anticipa anomalías del tráfico? (solo pronóstico de flujo/velocidad, solo clasifica estados normales o maniobras, solo cuenta vehículos, riesgo o frecuencia de accidentes a largo plazo, severidad de lesiones con datos históricos, solo imputación) | Excluir **CE-3** |
| 7 | ¿La detección NO usa Deep Learning como método principal? (SVM, Random Forest, XGBoost, Isolation Forest, ARIMA, Kalman, reglas, umbrales, estadística; o DL solo como línea base o preprocesamiento) | Excluir **CE-4** |
| — | Pasa todo | **Incluir** |
| — | No se puede saber con título y resumen | **Duda** (pasa a texto completo) |

**Qué SÍ cuenta como anomalía:** accidentes e incidentes, congestión no recurrente, conducción peligrosa vista desde fuera (contramano, exceso de velocidad, cambios de carril peligrosos, casi accidentes), cierres de vías, eventos extremos, trayectorias anómalas y la anticipación de un accidente a corto plazo en video.

**Regla de oro:** *ante la duda, NO excluir.* Pon **Duda**. Un estudio excluido por error se pierde; uno incluido de más solo cuesta leer un PDF.

**Casos frecuentes:**
- Conducción peligrosa **dentro de la cabina** (cámara al conductor, fatiga, celular) → CE-2. Conducción peligrosa **del vehículo en la vía** (trayectorias, video externo, sensores de dinámica) → pasa.
- **Dataset o benchmark** que evalúa modelos DL de detección → Duda. Si solo describe datos → CE-5.
- **Híbridos:** si una red profunda entrenada aprende la representación con la que se decide la anomalía → pasa, aunque al final haya un umbral o una regla.

---

## 3. Cómo dejar el comentario final

Mantén la etiqueta al inicio, porque el script 10 la lee. Borra «IA (verificar):» y la confianza. Escribe el motivo en una frase:

```
[Incluir] Detecta accidentes en video de cámaras de tráfico con YOLOv8; cumple dominio, anomalía y DL.
[Duda] Sin resumen; detección de anomalías en trayectorias, verificar a texto completo si son vehiculares.
[Excluir CE-2] Detecta fatiga del conductor con cámara de cabina; es estado del conductor, no tráfico.
[Excluir CE-3] Solo pronostica el flujo con GCN; no detecta anomalías.
[Excluir CE-4] El detector es Isolation Forest; el LSTM solo es línea base.
[Excluir CE-5] Es una revisión sistemática, no un estudio primario.
```

En Parsif.al, además del comentario:
- **Incluir** o **Duda** → Status **Accepted** (Selection criteria vacío).
- **Excluir** → Status **Rejected** y elige el **Selection criteria** con el mismo código.

---

## 4. Prompt para pedir ayuda a una IA (ChatGPT, Claude, etc.)

Úsalo cuando dudes de un artículo. Copia todo el bloque, reemplaza lo que está entre [corchetes] con los datos del Excel (título, año y resumen) y pégalo en el chat. **La decisión final es tuya:** la IA solo te da una segunda opinión.

```
Actúa como revisor de una revisión sistemática de literatura (PRISMA 2020) titulada
«Detección de anomalías en tráfico vehicular mediante Deep Learning (2020–2026)».
Evalúa SOLO con el título y el resumen. Aplica estas preguntas EN ORDEN; la primera
que se responda «sí» define el criterio:
1. ¿Es una versión duplicada de otro estudio? → Excluir CE-1
2. ¿Es revisión/survey, volumen de actas, capítulo, tesis, editorial, erratum,
   resumen extendido o preprint? → Excluir CE-5
3. ¿Publicado fuera de 2020–2026? → Excluir CI-3
4. ¿Idioma distinto de inglés/español? → Excluir CI-2
5. ¿El objeto NO es el tráfico vehicular por carretera? (redes informáticas,
   ciberseguridad, CAN, VANET, peatones sin vehículos, marítimo, aéreo, ferroviario,
   metro, estado del conductor —fatiga, distracción, emociones—, pavimento, señales)
   → Excluir CE-2
6. ¿NO detecta ni anticipa anomalías del tráfico? (solo pronóstico, solo clasificación
   de estados normales o maniobras, conteo de vehículos, riesgo o frecuencia de
   accidentes a largo plazo, severidad con datos históricos, imputación) → Excluir CE-3
   Sí cuentan como anomalía: accidentes, incidentes, congestión no recurrente,
   conducción peligrosa vista desde la vía, cierres, eventos extremos, trayectorias
   anómalas y anticipación de accidentes a corto plazo.
7. ¿La detección NO usa Deep Learning como método principal? (SVM, RF, XGBoost,
   Isolation Forest, ARIMA, Kalman, reglas, umbrales; o DL solo como línea base)
   → Excluir CE-4. En híbridos pasa si una red profunda entrenada aprende la
   representación con la que se decide la anomalía.
Si pasa todo → Incluir. Si no se puede saber con el título y el resumen → Duda
(ante la duda, NO excluir).

Artículo:
Título: [pega el título]
Año: [año]
Resumen: [pega el resumen; si no hay, escribe «sin resumen»]

Responde exactamente en este formato:
DECISIÓN: Incluir | Duda | Excluir
CRITERIO: (solo si excluye: CE-1, CE-5, CI-3, CI-2, CE-2, CE-3 o CE-4)
COMENTARIO: [etiqueta] una o dos frases en español que digan qué hace el estudio y
por qué cumple o no cumple. La etiqueta es [Incluir], [Duda] o [Excluir CE-x].
Ejemplo: [Excluir CE-2] Detecta fatiga del conductor con cámara de cabina; es estado
del conductor, no tráfico vehicular.
```

**Si la IA y la propuesta original no coinciden:** decide tú. Si sigues sin estar seguro, pon **Duda**.

---

## 5. Al terminar

1. En Parsif.al: **Export Articles** (pestaña All Sources) y mueve `articles.xls` a `RSL\cribado\salida\parsifal\`.
2. En CMD, desde la carpeta `RSL`:
```bat
python cribado\scripts\10_traer_de_parsifal.py
python cribado\scripts\04_cerrar_etapa.py --etapa TA
```
3. Haz `git add`, `git commit` y `git push`.

---

## Anexo A. Aceptados a revisar (151)

Orden: Duda de confianza baja → Duda media → Incluir media → Incluir alta.

| N° | ID | Título | Propuesta | Confianza |
|---|---|---|---|---|
| 1 | R0032 | A Comparative Analysis of Machine Learning, Deep Learning, and Metaheuristic-Based Ensemble Learning for Driver Behavior Profiling on UAH-DriveSet | Duda | baja |
| 2 | R0187 | A robust deep learning-based system for pedestrian-aware collision prevention in autonomous vehicles | Duda | baja |
| 3 | R0222 | A Time Convolutional Network Based Outlier Detection for Multidimensional Time Series in Cyber-Physical-Social Systems | Duda | baja |
| 4 | R0230 | A-TTC: a multimodal fusion framework for personalized truck forward collision warning via dynamic threshold calibration | Duda | baja |
| 5 | R0025 | Abnormal Vehicle Toll Evasion Detection Based on an Improved Transformer | Duda | baja |
| 6 | R0029 | Accident Prediction and Emergency Management for Expressways Using Big Data and Advanced Intelligent Algorithms | Duda | baja |
| 7 | R0148 | Anomaly detection method applied to vehicle monitoring | Duda | baja |
| 8 | R0190 | Artificial Intelligence Aspect Of Transportation Analysis Using Large Scale Systems | Duda | baja |
| 9 | R0262 | Blurred Encoding for Trajectory Representation Learning | Duda | baja |
| 10 | R0293 | Comparative analysis of machine learning techniques for enhanced vehicle tracking and analysis | Duda | baja |
| 11 | R0294 | Comparing Sparse and Dense Optical Flow Methods to Detect Traffic Anomalies, Based on Orientation | Duda | baja |
| 12 | R0429 | Driving Control in Autonomous Vehicles: An AI-Empowered Safety-Centric Approach | Duda | baja |
| 13 | R0548 | Grounded Anomalies: Towards Causally Grounded Kinematic Anomaly Generation | Duda | baja |
| 14 | R0580 | Improving IoT-Based Network Monitoring Through Integration of Passenger Feedback | Duda | baja |
| 15 | R0604 | Intelligent Truck Driving Safety Assistance Management System | Duda | baja |
| 16 | R0614 | IoT Based Accident Prevention System using Machine Learning techniques | Duda | baja |
| 17 | R0621 | Learning Multimodal Embeddings for Traffic Accident Prediction and Causal Estimation | Duda | baja |
| 18 | R0645 | Machine Learning for Identifying Group Trajectory Outliers | Duda | baja |
| 19 | R0646 | Macroscopic Big Data Analysis and Prediction of Driving Behavior with an Adaptive Fuzzy Recurrent Neural Network on the Internet of Vehicles | Duda | baja |
| 20 | R0658 | MMVAD: A vision–language model for cross-domain video anomaly detection with contrastive learning and scale-adaptive frame segmentation | Duda | baja |
| 21 | R0929 | Real time Alert AI and IoT based accident prevention and detection | Duda | baja |
| 22 | R0970 | Research on bad driving detection based on behavior recognition | Duda | baja |
| 23 | R1025 | Safe Roads: an Integration between Twitter and City Sensing | Duda | baja |
| 24 | R1040 | Self-Supervised Contrastive Learning for Individual and Collective Outlier Detection in Semantic Trajectories | Duda | baja |
| 25 | R1046 | Short-term Driving Style Recognition Based on Improved Deep Clustering in High-speed Scenarios | Duda | baja |
| 26 | R1056 | Smart Road Traffic Monitoring: Unveiling the Synergy of IoT and AI for Enhanced Urban Mobility | Duda | baja |
| 27 | R1066 | Spatial Deep Learning Approach to Older Driver Classification | Duda | baja |
| 28 | R1093 | SVD-BDRL: A trustworthy autonomous driving decision framework based on sparse voxels and blockchain enhancement | Duda | baja |
| 29 | R1124 | Towards Physics-informed Diffusion for Anomaly Detection in Trajectories: A Summary of Results | Duda | baja |
| 30 | R1179 | TrajLM: Transferable Mobility Pattern Distillation for Unified Trajectory Learning in Sparse Road Networks | Duda | baja |
| 31 | R1205 | Unveiling Road Rage Dynamics: Recreating and Modeling Road Rage in Audiovisual and Simulating Environments Based on Real-World Footage | Duda | baja |
| 32 | R0045 | A data-centric weak supervised learning for highway traffic incident detection | Duda | media |
| 33 | R0185 | A Risk Identification and Prediction Model for Intelligent Driving Under Multi-Vehicle Interactions in Mountain Tunnel Environments | Duda | media |
| 34 | R0249 | A variational autoencoder solution for road traffic forecasting systems: Missing data imputation, dimension reduction, model selection and anomaly detection | Duda | media |
| 35 | R0251 | A vision-based system for traffic anomaly detection using deep learning and decision trees | Duda | media |
| 36 | R0121 | An ensemble time-embedded transformer model for traffic conflict prediction at RRFB pedestrian crossings | Duda | media |
| 37 | R0132 | An integrated framework for multiple traffic anomalies detection on highways using vehicle trajectories | Duda | media |
| 38 | R0107 | Analysis and Evaluation of Baseline Models for Highway Traffic Incident Detection | Duda | media |
| 39 | R0138 | Anomalous Trajectory Detection for Automated Traffic Video Surveillance | Duda | media |
| 40 | R0292 | Comparative Analysis of Machine Learning Models for Detecting Abnormal Driving Behaviour in Two-Wheeler Kinematics | Duda | media |
| 41 | R0315 | Cybersecurity-Focused Anomaly Detection in Connected Autonomous Vehicles Using Machine Learning | Duda | media |
| 42 | R0360 | Deformation Gated Recurrent Network for Lane-level Abnormal Driving Behavior Recognition | Duda | media |
| 43 | R0389 | Detection of road traffic anomalies based on computational data science | Duda | media |
| 44 | R0428 | Driving Behaviour Estimation System Considering the Effect of Road Geometry by Means of Deep NN and Hotelling Transform | Duda | media |
| 45 | R0515 | FT-AED: Benchmark Dataset for Early Freeway Traffic Anomalous Event Detection | Duda | media |
| 46 | R0598 | Intelligent multi-sensor fusion and anomaly detection in vehicles via deep learning | Duda | media |
| 47 | R0622 | Learning Representation for Anomaly Detection of Vehicle Trajectories | Duda | media |
| 48 | R0635 | LLM-enhanced causal graph learning for real-time crash risk prediction | Duda | media |
| 49 | R0638 | Low-cost and high-performance abnormal trajectory detection based on the GRU model with deep spatiotemporal sequence analysis in cloud computing | Duda | media |
| 50 | R0664 | MoTIF: An end-to-end multimodal road traffic scene understanding foundation model | Duda | media |
| 51 | R0704 | Online transportation network cyber-attack detection based on stationary sensor data | Duda | media |
| 52 | R1010 | Road Incident Detection System | Duda | media |
| 53 | R1026 | Safe Routes, Safer Rides: A Multi-Tiered Approach to Trajectory Anomaly Detection | Duda | media |
| 54 | R1033 | Scene-dependent video anomaly detection: A benchmark and weakly supervised model | Duda | media |
| 55 | R1126 | Towards Safe Autonomy in Hybrid Traffic: Detecting Unpredictable Abnormal Behaviors of Human Drivers via Information Sharing | Duda | media |
| 56 | R1142 | Traffic Accident Severity Classification Using ResNet-18 | Duda | media |
| 57 | R1166 | Traffic Incident Detection System Based on Video Analysis | Duda | media |
| 58 | R1187 | TU-DAT: A Computer Vision Dataset on Road Traffic Anomalies | Duda | media |
| 59 | R1192 | UIT-ADrone: A Novel Drone Dataset for Traffic Anomaly Detection | Duda | media |
| 60 | R1193 | Uncovering intra- and inter-driver heterogeneity using driving behavior graphs | Duda | media |
| 61 | R1235 | When, Where, and What? A Benchmark for Accident Anticipation and Localization with Large Language Models | Duda | media |
| 62 | R0052 | A deep neural framework for real-time vehicular accident detection based on motion temporal templates | Incluir | media |
| 63 | R0167 | A Personalized Federated Learning Framework for Post-Event Forensic Traffic Analysis in Autonomous Vehicle Systems | Incluir | media |
| 64 | R0106 | An abnormal driving behavior recognition algorithm based on the temporal convolutional network and soft thresholding | Incluir | media |
| 65 | R0307 | Cross-Modality Interaction-Based Traffic Accident Classification | Incluir | media |
| 66 | R0329 | Data-driven traffic incident detection in urban roads based on machine learning algorithms | Incluir | media |
| 67 | R0510 | FPMT: Enhanced Semi-supervised Model for Traffic Incident Detection | Incluir | media |
| 68 | R0537 | GNN-RMNet: Leveraging graph neural networks and GPS analytics for driver behavior and route optimization in logistics | Incluir | media |
| 69 | R0543 | Graph Enhanced Trajectory Anomaly Detection | Incluir | media |
| 70 | R0615 | IRF-HTID-BO-LSTM: Classification Model of Curve Shape Index for Mountainous Highways and Intelligent Traffic Incident Detection Method | Incluir | media |
| 71 | R0618 | Lane-Wise Highway Anomaly Detection | Incluir | media |
| 72 | R0637 | Long short-term memory and convolutional neural network for abnormal driving behaviour recognition | Incluir | media |
| 73 | R0674 | Multi-Scale Detection of Anomalous Spatio-Temporal Trajectories in Evolving Trajectory Datasets | Incluir | media |
| 74 | R0986 | Research on Prediction Model of Expressway Traffic Abnormal Events Based on Nonlinear Internet of Things | Incluir | media |
| 75 | R1014 | Road traffic anomaly monitoring and warning based on DeepWalk algorithm | Incluir | media |
| 76 | R1092 | Suspicious detection in road traffic based on Kd-SLIC-K-means and SBAF-CNN using aerial view surveillance video | Incluir | media |
| 77 | R1094 | SWencoder: a succinct shockwave diagram encoding and interpretable deep learning model design to enhance learning efficiency and assurance | Incluir | media |
| 78 | R1149 | Traffic Anomaly Detection in Intelligent Transport Applications with Time Series Data using Informer | Incluir | media |
| 79 | R1172 | Traffic-Prior-Guided State-Aware Framework for Robust Urban Traffic Anomaly Detection | Incluir | media |
| 80 | R1202 | Unsupervised Scalable Multimodal Driving Anomaly Detection | Incluir | media |
| 81 | R1212 | UTRAND: Unsupervised Anomaly Detection in Traffic Trajectories | Incluir | media |
| 82 | R1213 | VegaEdge: Edge AI confluence for real-time IoT-applications in highway safety | Incluir | media |
| 83 | R0037 | A computer vision-based deep learning model to detect wrong-way driving using pan–tilt–zoom traffic cameras | Incluir | alta |
| 84 | R0049 | A Deep Cycle Limit Learning Machine Method for Urban Expressway Traffic Incident Detection | Incluir | alta |
| 85 | R0050 | A deep encoder-decoder network for anomaly detection in driving trajectory behavior under spatio-temporal context | Incluir | alta |
| 86 | R0051 | A Deep Learning Framework for Traffic Accident Detection Based on Improved YOLO11 | Incluir | alta |
| 87 | R0072 | A framework for detecting and predicting highway traffic anomalies via multimodal fusion and heterogeneous graph neural networks | Incluir | alta |
| 88 | R0080 | A Hybrid Method for Traffic Incident Detection Using Random Forest-Recursive Feature Elimination and Long Short-Term Memory Network with Bayesian Optimization Algorithm | Incluir | alta |
| 89 | R0097 | A memory-augmented multi-task collaborative framework for unsupervised traffic anomaly detection in driving videos | Incluir | alta |
| 90 | R0102 | A multimodal deep fusion framework for highway traffic anomaly detection | Incluir | alta |
| 91 | R0157 | A novel framework for detecting non-recurrent road traffic anomalies by combining a temporal graph convolutional network and hierarchical time memory detector | Incluir | alta |
| 92 | R0175 | A Real-Time Consensus-Free Accident Detection Framework for Internet of Vehicles Using Vision Transformer and EfficientNet | Incluir | alta |
| 93 | R0192 | A Self-Imputing Deep Multitask Sequence Model for Traffic Disruption Detection in Extreme Conditions | Incluir | alta |
| 94 | R0221 | A Three-Stage Anomaly Detection Framework for Traffic Videos | Incluir | alta |
| 95 | R0227 | A trajectory outlier detection method based on variational auto-encoder | Incluir | alta |
| 96 | R0024 | Abnormal Trajectory Detection Based on Geospatial Consistent Modeling | Incluir | alta |
| 97 | R0119 | An efficient computer vision framework for RSU-based accident recognition and V2X communication | Incluir | alta |
| 98 | R0136 | Anomalous Motion Detection on Highway Using Deep Learning | Incluir | alta |
| 99 | R0143 | Anomaly Detection in Multi-Agent Trajectories for Automated Driving | Incluir | alta |
| 100 | R0239 | Automatic detection of traffic accidents from video using deep learning techniques | Incluir | alta |
| 101 | R0243 | Automatic Traffic Anomaly Detection on the Road Network with Spatial-Temporal Graph Neural Network Representation Learning | Incluir | alta |
| 102 | R0244 | Autonomous anomaly detection on traffic flow time series with reinforcement learning | Incluir | alta |
| 103 | R0255 | Backbone-Level Enhancements in YOLOv9 for Traffic Accident Detection from Video Footage | Incluir | alta |
| 104 | R0313 | CVAE-ADS: A Deep Learning Framework for Traffic Accident Detection and Video Summarization | Incluir | alta |
| 105 | R0341 | Deep learning based detection and localization of road accidents from traffic surveillance videos | Incluir | alta |
| 106 | R0349 | Deep Learning-Driven Pattern Recognition for Real-Time Traffic Incident Detection in Complex Urban Environments | Incluir | alta |
| 107 | R0356 | Deep representation of imbalanced spatio-temporal traffic flow data for traffic accident detection | Incluir | alta |
| 108 | R0337 | DeepFlow: Abnormal Traffic Flow Detection Using Siamese Networks | Incluir | alta |
| 109 | R0379 | Detecting Socially Abnormal Highway Driving Behaviors via Recurrent Graph Attention Networks | Incluir | alta |
| 110 | R0380 | Detecting Urban Traffic Anomalies Using Traffic-Monitoring Data | Incluir | alta |
| 111 | R0403 | Domain-enhanced dual-branch model for efficient and interpretable accident anticipation | Incluir | alta |
| 112 | R0438 | DSGF-YOLO: A Lightweight Deep Neural Network for Traffic Accident Detection and Severity Classifications | Incluir | alta |
| 113 | R0444 | Early Detection of Freeway Traffic Anomalies With a Cycle-Consistent Bidirectional Generative Adversarial Network | Incluir | alta |
| 114 | R0465 | Enhancing Freeway Safety: LSTM-Based Detection of Traffic Anomalies | Incluir | alta |
| 115 | R0471 | Enhancing Traffic Accident Detection with YOLOv5 in Smart City Road Monitoring | Incluir | alta |
| 116 | R0501 | Feasibility Analysis of Static-Image-Based Traffic Accident Detection Under Domain Shift for Edge-AI Surveillance Systems | Incluir | alta |
| 117 | R0526 | Generative adversarial network for car following trajectory generation and anomaly detection | Incluir | alta |
| 118 | R0528 | Generative Adversarial Networks (GANs) and Object Tracking (OT) for Vehicle Accident Detection | Incluir | alta |
| 119 | R0539 | Graph autoencoder with mirror temporal convolutional networks for traffic anomaly detection | Incluir | alta |
| 120 | R0545 | Graph Multi-Resolution Transformer for Road Traffic Anomaly Detection | Incluir | alta |
| 121 | R0561 | History-Based Road Traffic Anomaly Detection Using Deep Learning and Real-World Data | Incluir | alta |
| 122 | R0585 | IncidentNet: Traffic Incident Detection, Localization and Severity Estimation with Sparse Sensing | Incluir | alta |
| 123 | R0592 | Integrating Generative Adversarial Networks and Convolutional Neural Networks for Enhanced Traffic Accidents Detection and Analysis | Incluir | alta |
| 124 | R0596 | Intelligent deep fusion network for urban traffic flow anomaly identification | Incluir | alta |
| 125 | R0600 | Intelligent surveillance system for accident detection using machine learning | Incluir | alta |
| 126 | R0601 | Intelligent traffic accident detection system in complex dynamic scenarios based on the dual-stream spatiotemporal-fusion model | Incluir | alta |
| 127 | R0623 | Learning Spatio-Temporal Features via 3D CNNs to Forecast Time-to-Accident | Incluir | alta |
| 128 | R0624 | Learning Traffic Anomalies from Generative Models on Real-Time Observations | Incluir | alta |
| 129 | R0666 | Multi-Adjacent Camera-Based Dangerous Driving Trajectory Recognition for Ultra-Long Highways | Incluir | alta |
| 130 | R0682 | Multi-stage classification of abnormal traffic events using a multi-head + LSTM | Incluir | alta |
| 131 | R0702 | Online Anomalous Subtrajectory Detection on Road Networks with Deep Reinforcement Learning | Incluir | alta |
| 132 | R0716 | Outlier Vehicle Trajectory Detection Using Deep Autoencoders in Santiago, Chile | Incluir | alta |
| 133 | R0721 | Pattern Anomaly Detection based on Sequence-to-Sequence Regularity Learning | Incluir | alta |
| 134 | R0938 | Real-time rapid accident detection for optimizing road safety in Bangladesh | Incluir | alta |
| 135 | R0943 | Real-time traffic accident detection using yolov8 | Incluir | alta |
| 136 | R0958 | Recognition of surrounding vehicle anomalous intent in the vehicle-road-cloud environment for autonomous driving | Incluir | alta |
| 137 | R1000 | RETAD: Vehicle Trajectory Anomaly Detection Based on Reconstruction Error | Incluir | alta |
| 138 | R1003 | Revisiting the Non-recurrent Traffic Incident Identification Problem for Real-Time Applications Using Theory-Aware Unsupervised Learning | Incluir | alta |
| 139 | R1013 | Road Traffic Anomaly Detection by Human-Attention-Assisted Text–Vision Learning | Incluir | alta |
| 140 | R1029 | Safety in Smart Cities—Automatic Recognition of Dangerous Driving Styles | Incluir | alta |
| 141 | R1049 | Simulation-based early detection and classification of severity of traffic incident using deep learning and dynamical reservoir features | Incluir | alta |
| 142 | R1052 | Smart City Transportation: Deep Learning Ensemble Approach for Traffic Accident Detection | Incluir | alta |
| 143 | R1074 | Special Traffic Event Detection: Framework, Dataset Generation, and Deep Neural Network Perspectives | Incluir | alta |
| 144 | R1082 | Structural Attention-Based Recurrent Variational Autoencoder for Highway Vehicle Anomaly Detection | Incluir | alta |
| 145 | R1100 | TempoLearn Network: Leveraging Spatio-Temporal Learning for Traffic Accident Detection | Incluir | alta |
| 146 | R1137 | Traffic Accident Detection Method Using Trajectory Tracking and Influence Maps | Incluir | alta |
| 147 | R1138 | Traffic Accident Detection Using Background Subtraction and CNN Encoder–Transformer Decoder in Video Frames | Incluir | alta |
| 148 | R1140 | Traffic Accident Prediction without Object Detection for Single-Vehicle Accidents | Incluir | alta |
| 149 | R1148 | Traffic anomaly detection by fusing spatiotemporal graphs and visual perception | Incluir | alta |
| 150 | R1185 | TriNet-RTAD: An efficient ensemble-based deep CNN framework for road traffic anomaly detection | Incluir | alta |
| 151 | R1214 | Vehicle Abnormal Behavior Detection Based on Dense Block and Soft Thresholding | Incluir | alta |

## Anexo B. Rechazados a revisar (57)

Exclusiones con confianza media, ordenadas por criterio.

| N° | ID | Título | Propuesta | Confianza |
|---|---|---|---|---|
| 1 | R0437 | Driving style recognition using machine learning and smartphones | Excluir CE-1 | media |
| 2 | R0656 | MmDrive: MmWave Sensing for Live Monitoring and On-Device Inference of Dangerous Driving | Excluir CE-1 | media |
| 3 | R0012 | Abnormal Driving Behavior Detection: A Machine and Deep Learning Based Hybrid Model | Excluir CE-2 | media |
| 4 | R0018 | Abnormal event detection for video surveillance using an enhanced two-stream fusion method | Excluir CE-2 | media |
| 5 | R0291 | Comparative Analysis of Deep Learning-based Anomaly Detection Models for GPS Spoofing Detection | Excluir CE-2 | media |
| 6 | R0386 | Detection of driver health condition by monitoring driving behavior through machine learning from observation | Excluir CE-2 | media |
| 7 | R0407 | Driver abnormal behavior detection based on dual-channel attention mechanism | Excluir CE-2 | media |
| 8 | R0408 | Driver Abnormal Driving Detection Model based on Deep Learning | Excluir CE-2 | media |
| 9 | R0463 | Enhancing anomaly detection with adaptive node inspection in large-scale networks with binary sensors | Excluir CE-2 | media |
| 10 | R0517 | Fuzzy-based driver monitoring system to assess dangerous driving on roads | Excluir CE-2 | media |
| 11 | R0551 | HAR-Net: An Hourglass Attention ResNet Network for Dangerous Driving Behavior Detection | Excluir CE-2 | media |
| 12 | R0657 | MM-LMF: A Low-Rank Multimodal Fusion Dangerous Driving Behavior Recognition Method Based on FMCW Signals | Excluir CE-2 | media |
| 13 | R0676 | Multi-Scene Traffic Light Detection and Fault Identification via Dual-Attention Image Fusion | Excluir CE-2 | media |
| 14 | R0695 | Non-IID data re-balancing at IoT edge with peer-to-peer federated learning for anomaly detection | Excluir CE-2 | media |
| 15 | R0703 | Online anomaly detection in surveillance videos with asymptotic bound on false alarm rate | Excluir CE-2 | media |
| 16 | R0711 | Optimized Binary Neural Networks for Road Anomaly Detection: A TinyML Approach on Edge Devices | Excluir CE-2 | media |
| 17 | R0731 | Prediction of Dangerous Driving Behaviour Based on Vehicle Motion | Excluir CE-2 | media |
| 18 | R0969 | Research on Automotive Data Security Management and Technological Development | Excluir CE-2 | media |
| 19 | R1181 | Transferable Unsupervised Outlier Detection Framework for Human Semantic Trajectories | Excluir CE-2 | media |
| 20 | R1188 | Two-stage vision transformer for fusing global and local features in distracted driving behavior recognition; [融合全局与局部特征的两阶段ViT 分心驾驶行为识别方法] | Excluir CE-2 | media |
| 21 | R0038 | A convergent cross‐mapping approach for unveiling congestion spatial causality in urban traffic networks | Excluir CE-3 | media |
| 22 | R0047 | A data–information–knowledge cycle for modeling driving behavior | Excluir CE-3 | media |
| 23 | R0184 | A Risk Assessment Model for Overtaking Behavior Based on Air-Ground Dual Perspectives | Excluir CE-3 | media |
| 24 | R0308 | Cross-Scenario Maneuver Decision with Adaptive Perception for Autonomous Driving | Excluir CE-3 | media |
| 25 | R0321 | Dangerous Driving Behavior Prediction Study Based on CNN-LSTM-AM and Multi-Source Feature Screening | Excluir CE-3 | media |
| 26 | R0338 | Deep Graph Convolutional Networks for Incident-Driven Traffic Speed Prediction | Excluir CE-3 | media |
| 27 | R0357 | Deep Transfer Learning Based Intersection Trajectory Movement Classification for Big Connected Vehicle Data | Excluir CE-3 | media |
| 28 | R0410 | Driver behavior analysis in diverging area based on driving simulation | Excluir CE-3 | media |
| 29 | R0430 | Driving event recognition using machine learning and smartphones | Excluir CE-3 | media |
| 30 | R0439 | DST-DAN: Dynamic Spatio-Temporal Decoupling and Delay-Aware Network for Traffic Flow Prediction | Excluir CE-3 | media |
| 31 | R0480 | Evaluating drivers’ braking behavior at mid-block pedestrian crosswalks using video data and a mixed logit model with heterogeneity in the means | Excluir CE-3 | media |
| 32 | R0481 | Evaluating impact of remote-access cyber-attack on lane changes for connected automated vehicles | Excluir CE-3 | media |
| 33 | R0485 | Exploiting Multi-modal Contextual Sensing for City-bus’s Stay Location Characterization: Towards Sub-60 Seconds Accurate Arrival Time Prediction | Excluir CE-3 | media |
| 34 | R0487 | Exploring risky events and driver responses in automated driving: Insights from real-world videos | Excluir CE-3 | media |
| 35 | R0488 | Exploring Search Volumes of Terms in Web Portals for Accurate Event-Aware Traffic Prediction | Excluir CE-3 | media |
| 36 | R0496 | Fast and Precise: Parallel Processing of Vehicle Traffic Videos Using Big Data Analytics | Excluir CE-3 | media |
| 37 | R0504 | FedSTGM: A Federated Spatio-Temporal Graph Model for Traffic Flow Prediction | Excluir CE-3 | media |
| 38 | R0512 | From Prediction to Prevention: Leveraging Deep Learning in Traffic Accident Prediction Systems | Excluir CE-3 | media |
| 39 | R0547 | GRIDS: Personalized Guideline Recommendations while Driving Through a New City | Excluir CE-3 | media |
| 40 | R0559 | High-Risk Test Scenario Generation for Autonomous Vehicles at Roundabouts Using Naturalistic Driving Data | Excluir CE-3 | media |
| 41 | R0589 | Instance Space Analysis of Testing of Autonomous Vehicles in Critical Scenarios | Excluir CE-3 | media |
| 42 | R0605 | Intelligent Urban Traffic Congestion Prediction Through Accident-Aware and Time-Dependent Traffic Analytics | Excluir CE-3 | media |
| 43 | R0708 | On the possibility of short-term traffic prediction during disaster with machine learning approaches: An exploratory analysis | Excluir CE-3 | media |
| 44 | R0954 | Real-Time Vehicle Maneuvering Detection With Digital Compass | Excluir CE-3 | media |
| 45 | R0988 | Research on road traffic condition prediction of smart city based on spatio-temporal multi-source information fusion | Excluir CE-3 | media |
| 46 | R1065 | SoVAR: Build Generalizable Scenarios from Accident Reports for Autonomous Driving Testing | Excluir CE-3 | media |
| 47 | R1125 | Towards Resilient Transportation: A Conditional Transformer for Accident-Informed Traffic Forecasting | Excluir CE-3 | media |
| 48 | R0202 | A stacked ensemble model for traffic conflict prediction using emerging sensor data | Excluir CE-4 | media |
| 49 | R0235 | Automated detection of vehicles with anomalous trajectories in traffic surveillance videos | Excluir CE-4 | media |
| 50 | R0286 | Collecting comprehensive traffic information using pavement vibration monitoring data | Excluir CE-4 | media |
| 51 | R0500 | FDM: Effective and efficient incident detection on sparse trajectory data | Excluir CE-4 | media |
| 52 | R0660 | Modeling aggressive driving behavior based on graph construction | Excluir CE-4 | media |
| 53 | R0705 | On the applicability of time series anomaly detection methods to real-world traffic volume data | Excluir CE-4 | media |
| 54 | R0707 | On the Interest of Extending Internet of Behaviors to Internet of Habits: A Preliminary Exploration | Excluir CE-4 | media |
| 55 | R1031 | Scalable Pythagorean Mean-based Incident Detection in Smart Transportation Systems | Excluir CE-4 | media |
| 56 | R1190 | Two-Tier Anomaly Detection for V2I Alerting on IoT Vehicle Counts: A Kuwait Corridor Benchmark | Excluir CE-4 | media |
| 57 | R1230 | Visual extensions and anomaly detection in the pNEUMA experiment with a swarm of drones | Excluir CE-4 | media |
