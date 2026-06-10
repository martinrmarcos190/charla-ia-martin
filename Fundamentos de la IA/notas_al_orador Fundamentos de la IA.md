# Fundamentos de IA — Notas al orador (guion diapositiva por diapositiva)

> Curso: IA Aplicada · Módulo 1, Clase 1 · 75 min · Audiencia: MLOps senior · Registro: rioplatense
> Este archivo es el **teleprompter**: qué decir en cada slide, cuánto tiempo, y cuándo disparar cada demo.
> Va de la mano del archivo `02_presentacion.md` (mismo orden de slides).

---

## Convenciones

- ⏱️ = marca de tiempo acumulada (arranca en 00:00).
- 🎬 = momento de disparar una demo en vivo.
- 💬 = lo que decís (en bullets, no leído palabra por palabra).
- 🎯 = el punto que NO se pueden ir sin entender.

---

## Slide 0 — Portada · ⏱️ 00:00–00:01

💬
- Bienvenida corta. "Fundamentos de IA, primera de las clases del módulo."
- Setear la regla del juego: "a vos no te explico qué es un modelo, un deploy ni un pipeline."
- Tesis: **no es magia, es ingeniería**, y casi todo tiene análogo en DevOps.

---

## Slide 1 — Hoja de ruta · ⏱️ 00:01–00:03

💬
- "Hoy tendemos un puente: del ML clásico que ya manejás hacia LLMs y agentes."
- Lo que ya saben lo usamos como **analogía** (Docker, IaC, CI/CD), no lo explicamos.
- Adelanto: 4 demos en vivo, todo embebido en la presentación, nada de notebooks.

🎯 Que entiendan que el hilo conductor es la analogía DevOps/MLOps.

---

## Slide 2 — Línea de tiempo (ancla) · ⏱️ 00:03–00:06

💬
- Recorrer la década rapidísimo, sin frenar en cada hito.
- Marcar tres quiebres: **2012** (AlexNet, deep learning sale del lab), **2017** (Transformers), **2022-2025** (LLMs → agentes).
- Cerrar con el dato fuerte: Claude Code llegó a **$1B run-rate revenue en noviembre 2025**, seis meses después de su lanzamiento público (Anthropic, comunicado 3-dic-2025).
- "Esta slide queda de ancla; vamos a volver a ella mentalmente toda la clase."

🎯 Ubicar la IA generativa actual como punto de llegada de una evolución, no como ruptura mágica.

---

## Slide 3 — 1.1 De reglas a patrones · ⏱️ 00:06–00:10

💬
- 40 años de software = **reglas explícitas** (`if`, validaciones, reglas de negocio). El programador sabe y le dicta a la máquina.
- Funciona mientras el dominio sea enumerable. Se rompe con "reconocé un gato", "esto es spam", "traducí esto".
- ML invierte la lógica: **le doy ejemplos y que descubra las reglas solo**.
- Pasamos de programar el *qué hacer* a programar el *cómo aprender*.
- Costo del paradigma: opacidad, no determinismo, dependencia total de los datos.

🎯 El cambio mental: de dictar reglas a curar datos.

---

## Slide 4 — 1.2 Modelo = artefacto compilado · ⏱️ 00:10–00:20

💬
- De dónde sale el ML: estadística aplicada (regresión lineal/logística = años 50-60). Cambió la escala y el cómputo, no la idea.
- Repaso veloz (ya lo saben): regresión, árboles, **Random Forest (Breiman 2001)**, gradient boosting (XGBoost/LightGBM), SVM/KNN/Naïve Bayes. Tabular sigue siendo de ellos hoy.
- **El análogo clave** (mostrar la tabla de la slide): un modelo entrenado es **un artefacto compilado a partir de datos**.
  - dataset ≈ código fuente
  - `model.fit()` ≈ `docker build`
  - `.pkl`/`.safetensors` ≈ imagen de Docker
  - model registry ≈ container registry
  - `model.predict()` ≈ `docker run`
- Igual que un binario, es **opaco**: no leés un Random Forest entrenado como leés un `.py`.

🎯 "Un modelo es un binario que compilás desde datos." Esta es la idea ancla del bloque.

---

## Slide 5 — 1.3 Redes neuronales y backprop · ⏱️ 00:20–00:23

💬
- Una red es la generalización: encadenás muchas combinaciones lineales con no-linealidades. Cada neurona = `activación(W·x + b)`.
- Funcionan por capacidad (universal approximation) y porque **aprenden las features solas** → adiós feature engineering manual.
- Backprop (**Rumelhart, Hinton, Williams, Nature 1986**) en 6 pasos intuitivos:
  1. pesos random
  2. predigo (mal)
  3. mido el error (loss)
  4. propago el error hacia atrás → gradiente por parámetro
  5. ajusto cada peso un poquito (descenso de gradiente)
  6. repito millones de veces
- Analogía: **un CI loop infinito** donde el test es "cuánto te equivocaste" y el auto-fix ajusta los pesos.

🎯 El modelo se equivoca → se corrige. Millones de veces. Por eso entrenar es caro.

---

## Slide 6 — 🎬 Demo 1: descenso de gradiente · ⏱️ 00:23–00:30

🎬 **Disparar la animación de la slide** (punto rojo bajando al mínimo).

💬 (mientras corre)
- "El punto rojo es el estado de los parámetros; la estrella es el óptimo."
- Cada paso: medí el error, calculá el gradiente, movete en la dirección opuesta.
- "Esto es backprop, pero en miles de millones de dimensiones en vez de dos."
- Tocar el **slider de learning rate**: muy alto → diverge y pega saltos; muy bajo → tarda una eternidad. Es el mismo `lr` que ponés cuando entrenás.

🎯 Visualizar físicamente "se equivoca y se ajusta".

---

## Slide 7 — 1.4 Embeddings: coordenadas GPS del significado · ⏱️ 00:30–00:38

💬
- Pregunta disparadora: "¿cómo le hago tragar la palabra 'perro' a una red que sólo entiende números?"
- Idea ingenua: **one-hot** (vector de 50.000 dims, un 1 y el resto ceros). Problema: 'perro' y 'gato' tan lejos como 'perro' y 'factura'. Cero significado.
- Idea embeddings: **vector denso de pocas dims (100–3072)**, entrenado para que significados parecidos queden cerca.
- Papers: **Word2Vec (Mikolov 2013)** y **GloVe (Pennington/Socher/Manning 2014)**. Intuición de Firth: "una palabra se define por la compañía que mantiene".
- El resultado que voló cabezas: `rey - hombre + mujer ≈ reina`. **Aritmética sobre significado.**
- Analogía: **coordenadas GPS del significado**. BA cerca de Montevideo, lejos de Tokio. 'perro' cerca de 'gato', lejos de 'factura'.
- Métrica de cercanía: **similitud coseno**.
- Esto es la base de **RAG, búsqueda semántica, recomendadores, deduplicación, detección de fraude** → medio stack moderno.

🎯 Que se vayan con la imagen: una palabra/token = un punto en un espacio vectorial donde la cercanía es significado. (Es el puente hacia LLMs.)

---

## Slide 8 — 🎬 Demo 2: embeddings + coseno · ⏱️ 00:38–00:42

🎬 **Disparar la matriz de similitud interactiva.**

💬 (mientras se muestra)
- Tres cosas para resaltar:
  1. 'perro corre por el parque' vs 'gato duerme en el sillón' → similitud media-alta (comparten "animal doméstico").
  2. 'perro corre' vs 'cachorro persigue pelota' → paráfrasis, todavía más cerca.
  3. 'perro' vs 'factura de la luz' → casi cero.
- "El modelo que genera esto pesa 80 megas y corre en una laptop sin GPU."
- "Esto es exactamente lo que hay atrás de la búsqueda semántica de Notion o Drive, y de RAG."

🎯 Confirmar visualmente: cercanía numérica = similitud de significado.

---

## Slide 9 — 1.5 Transformers y atención · ⏱️ 00:42–00:50

💬
- Pre-2017: RNN/LSTM. Procesabas palabra por palabra con un estado oculto. Dos problemas: se diluye el contexto largo y **no paraleliza** (muerte con datasets grandes).
- Junio 2017: **Attention Is All You Need (Vaswani et al., Google)**. Tiran las RNN, se quedan sólo con atención.
- Idea en humano: al procesar una palabra, **mira a todas las demás simultáneamente** y decide a cuáles prestar atención.
- Ejemplo: "El gato que vi ayer en el parque estaba durmiendo" → al procesar 'estaba', va directo a 'gato' (6 palabras atrás) en un solo paso.
- Mecánica mínima: **Query** (qué busco) · **Key** (qué ofrezco) · **Value** (qué información tengo). Q·K = cuánta atención; softmax; pondero los Values. Multi-head = varios en paralelo, cada uno aprende relaciones distintas.
- Por qué fue LA revolución (dos cosas juntas):
  1. **Paraleliza** → destrabó la escala (tirale todas las GPUs).
  2. **Captura contexto largo** sin pérdida de señal.
- Analogía: RNN = build secuencial (Jenkins viejo). Transformer = build masivamente paralelo (Bazel/Buildkite bien armado).
- "Sin esto no hay GPT, BERT, Claude ni Gemini. Toda la IA generativa está parada sobre este paper."

🎯 La atención rompe la secuencialidad → desbloquea la escala.

---

## Slide 10 — 🎬 Demo 3: mapa de atención · ⏱️ 00:50–00:54

🎬 **Disparar el heatmap interactivo** (cambiar entre las 2-3 oraciones precargadas).

💬 (mientras se muestra)
- Aclarar que es simplificación didáctica (en un Transformer real Q/K/V son proyecciones aprendidas y hay multi-head).
- "Cada fila es un token preguntando: ¿a quién tengo que prestarle atención para entenderme?"
- Señalar cómo un token de verbo "atrae" hacia su sujeto.
- "En una red entrenada con trillones de tokens, distintos cabezales se especializan: correferencia, sintaxis, semántica."

🎯 Ver, literalmente, "quién mira a quién".

---

## Slide 11 — 1.6 De Transformers a LLMs · ⏱️ 00:54–01:00

💬
- Receta para llegar a un LLM:
  1. Transformer **decoder-only** (la mitad que genera).
  2. Escalalo bestialmente (GPT-3 = 175B; los frontier de 2025 más grandes, muchos sin número público).
  3. Entrenalo con una tarea tonta: **predecir el próximo token** sobre medio internet (trillions de tokens).
  4. Fine-tuning + RLHF para alinearlo.
- **Un LLM es un autocomplete cósmico.** Predice token por token la continuación más probable.
- Dato MLOps 1 — **tokenización**: el LLM ve enteros, no strings. BPE. `cl100k_base` (GPT-4) vs `o200k_base` (GPT-4o, GPT-5, o1/o3/o4). Facturás, contás context window y batcheás **por token**.
- Dato MLOps 2 — **NO ES DETERMINÍSTICO** (este es el que les choca):
  - Muestrea de una distribución (`temperature`, `top_p`, `top_k`).
  - Mismo prompt → outputs distintos.
  - Se rompe el `assert output == "..."`. Hay que evaluar por propiedades, LLM-as-judge, golden sets semánticos.
  - `temperature=0` + seed ayuda pero no garantiza; y el proveedor te cambia el modelo sin avisar → versionalo explícito.
- Analogía: una API externa que devuelve respuestas **similares pero no idénticas** y que se actualiza sola. Diseñá asumiendo eso: caching, idempotencia, schema validation, retries, observability.

🎯 LLM = autocomplete gigante, potente pero no determinístico y caro de operar.

---

## Slide 12 — Implicancias del no-determinismo · ⏱️ (incluido en 1.6)

💬
- Reforzar los puntos de la slide: testing, eval, versionado, caching.
- "Esto es lo que más les va a cambiar el día a día como MLOps."

---

## Slide 13 — 🎬 Demo 4: tokenización · ⏱️ 01:00–01:04

🎬 **Disparar el tokenizador en vivo** (tipear texto y ver los tokens; switch `cl100k_base` / `o200k_base`).

💬 (mientras se muestra)
- Tres observaciones:
  1. El **español gasta más tokens** que el inglés para el mismo significado → impacta costo y context window.
  2. Código y emojis se tokenizan distinto.
  3. `o200k_base` suele usar menos tokens en multilingüe → por eso OpenAI lo introdujo.
- "Cuando estimen costos, no estimen por caracteres ni palabras: **por tokens**."

🎯 El token es la unidad real con la que opera y factura el modelo.

---

## Slide 14 — 1.7 De LLM a Agente · ⏱️ 01:04–01:08

💬
- Hasta acá: el LLM **genera texto**. Punto. Le falta **hacer cosas**.
- Definición Anthropic (Building Effective Agents, dic 2024): *workflows* = caminos de código predefinidos; *agents* = el LLM **dirige dinámicamente su propio proceso y uso de herramientas**.
- Definición de la página de Claude Code: un sistema agéntico **actúa hacia un objetivo con autonomía**: lee, planifica, ejecuta con herramientas reales, evalúa el resultado y ajusta.
- El loop (**ReAct, Yao et al. 2022**): **PENSAR → ACTUAR (tool) → OBSERVAR → ¿terminé? → loop**.
- Bloque mínimo (Anthropic): **augmented LLM** = LLM + retrieval + tools + memory.

🎯 La imagen mental del agente: un loop donde el LLM piensa, actúa, observa e itera. (Esta imagen sostiene el resto del curso.)

---

## Slide 15 — Impacto en software 2025-2026 · ⏱️ 01:08–01:11

💬 (es la slide de "esto ya no es teoría")
- Enterprise wins (página oficial de Claude Code):
  - **Stripe**: 1.370 ingenieros; migración Scala→Java de 10k líneas en 4 días (vs 10 engineer-weeks).
  - **Ramp**: −80% en tiempo de investigación de incidentes.
  - **Wiz**: 50k líneas Python→Go en ~20 horas (vs 2-3 meses).
  - **Rakuten**: delivery de features de 24 a 5 días hábiles.
- **Ser honesto con el contraste** (no es todo color de rosa):
  - **METR 2025** (arXiv:2507.09089): devs open-source experimentados resultaron **19% más lentos** con la herramienta, aunque se autopercibían más rápidos.
  - **Veracode 2025**: cuando el modelo puede elegir, eligió el método **inseguro el 45% de las veces**.
  - **Gartner (jun 2025)**: predicen que **>40% de los proyectos agénticos se cancelan** antes de fin de 2027 (mucho hype, PoCs mal aplicados).
  - **DORA 2025**: la IA *"magnifica las fortalezas de las organizaciones de alto rendimiento y las disfunciones de las que luchan"*.
- Conectar con el curso: "por esto el módulo que sigue entra a fondo en **tools y skills** — prender el agente no alcanza, hay que armarlo bien."

🎯 El impacto es real y enorme, pero amplifica lo bueno y lo malo. El control de calidad es responsabilidad de ustedes.

---

## Slide 16 — Tu rol está cambiando · ⏱️ 01:11–01:12

💬
- De "write code, run tests, fix, repeat" a "set goal, review, approve".
- **Diseñás la fábrica, no atornillás cada pieza.**
- Puente: "la próxima clase, tools y skills, ahora con las manos en la masa."

---

## Slide 17 — Cierre y recap · ⏱️ 01:12–01:15

💬 (recap de las 6 ideas)
1. ML clásico = estadística que compila **artefactos** desde datos.
2. Redes + backprop = aprenden features solas vía loop error/corrección.
3. Embeddings = significado convertido en **coordenadas geométricas**.
4. Transformers = atención rompe la secuencialidad → escala.
5. LLMs = Transformers gigantes que autocompletan, **no determinísticos**.
6. Agentes = el LLM que **actúa**: piensa, usa tools, observa, itera.
- "Van a dejar de implementar y empezar a orquestar. Para orquestar bien, hay que saber qué hay en la caja. Eso fue hoy."
- Abrir a **preguntas**.

---

## Plan B de timing

- **Si te quedás corto:** comprimí 1.5 y 1.7; recortá los números de impacto (METR/Veracode/Gartner/DORA) y dejá sólo los enterprise wins.
- **Si te sobra:** extendé la Demo 3 cambiando oraciones, o mostrá aritmética de embeddings (`rey - hombre + mujer`).
- **Bloques más comprimibles:** 1.5 (Transformers) y 1.7 (Agentes).
- **Bloques intocables:** 1.4 (Embeddings) y la idea de no-determinismo en 1.6 — son los puentes conceptuales.

## Errata a evitar

- La cifra "2,74x más vulnerabilidades en código IA" es de **CodeRabbit** (470 PRs), NO de Veracode. El dato citable de Veracode es el **45% de elecciones inseguras**.
