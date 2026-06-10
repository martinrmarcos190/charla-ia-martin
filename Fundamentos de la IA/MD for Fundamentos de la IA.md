# Fundamentos de IA — Material de clase completo (75 min)

> Curso: IA Aplicada · Módulo 1, Clase 1 · Duración: 75 min · Modalidad: presencial · Audiencia: MLOps senior (Docker, IaC, CI/CD, pipelines, ML clásico) que recién empiezan con agentes y usan Claude Code a nivel básico.
> Registro: Rioplatense (voseo).

---

## TL;DR para el instructor

- El objetivo de esta clase es **construir el puente** desde el ML clásico que ya manejan hasta los LLMs y agentes modernos, usando analogías de DevOps/MLOps (imagen de Docker, artefacto compilado, IaC, deploy).
- NO se explica qué es un modelo, un deploy o un pipeline. SÍ se explican: backprop intuitivo, embeddings como "coordenadas GPS del significado", atención como mecanismo que rompe la secuencialidad, LLMs como autocomplete masivo no determinístico, y agentes como el salto de "generar texto" a "ejecutar acciones".
- Cuatro demos en vivo en un único notebook: tokenización con `tiktoken`, embeddings + similitud coseno con `sentence-transformers`, mini-visualización de atención (mapa de calor) y descenso de gradiente 2D animado.

---

## 1) Cronograma minuto a minuto

| Minuto | Bloque | Tema | Actividad |
|---|---|---|---|
| 00:00–00:03 | Apertura | Presentación + objetivo de la clase | Hablado |
| 00:03–00:10 | 1.1 | Cambio de paradigma: de reglas a patrones | Hablado + slide línea de tiempo |
| 00:10–00:20 | 1.2 | ¿Qué es un modelo de ML? | Hablado + analogía Docker |
| 00:20–00:30 | 1.3 | Redes neuronales y backpropagation | Hablado + **Demo 1: gradient descent 2D** |
| 00:30–00:42 | 1.4 | Embeddings: coordenadas GPS del significado | Hablado + **Demo 2: embeddings + coseno** |
| 00:42–00:54 | 1.5 | Transformers y atención: la revolución | Hablado + **Demo 3: mapa de atención** |
| 00:54–01:04 | 1.6 | De transformers a LLMs | Hablado + **Demo 4: tokenización con tiktoken** |
| 01:04–01:12 | 1.7 | Agentes de IA: de predecir texto a ejecutar acciones | Hablado + diagrama loop agéntico |
| 01:12–01:15 | Cierre | Anclaje y puente a la próxima clase | Hablado |

---

## 2) Guion hablado (minuto a minuto)

### 00:00–00:03 · Apertura

> "Buenas. Bienvenidos a **Fundamentos de IA**. Antes de arrancar, una aclaración importante: a vos no te tengo que explicar qué es un modelo, qué es un deploy, ni qué es un pipeline. Vos eso lo venís haciendo hace años. Lo que vamos a hacer en estos 75 minutos es **tender un puente**: desde el ML clásico que ya conocés — entrenar un modelo, serializarlo, servirlo detrás de una API — hasta lo que está pasando hoy con los LLMs y los agentes. La tesis de la clase es simple: **no es magia, es ingeniería**, y casi todo tiene un análogo en el mundo DevOps que ya manejás. Vamos a usar esos análogos como muletas durante toda la clase."

---

### 00:03–00:10 · 1.1 El cambio de paradigma: de reglas a patrones

> "Arranquemos por el principio conceptual. Durante 40 años el software fue, esencialmente, **reglas explícitas**: vos escribís un `if`, una validación, una regla de negocio. El programador es el que sabe, y le dicta al sistema. Eso funciona bárbaro mientras el dominio sea acotado y las reglas sean enumerables.
>
> El problema aparece cuando querés que un sistema reconozca un gato en una foto, o entienda si un mail es spam, o traduzca del inglés al castellano. Ahí las reglas no escalan: nadie puede enumerarlas. Y ahí entra el machine learning con la idea opuesta: **en vez de programar las reglas, le doy ejemplos al sistema y que las reglas las descubra él**. Pasamos de programar el *qué hacer* a programar el *cómo aprender*.
>
> Décadas en una transparencia, rapidito:
>
> - **2000–2010:** ML clásico — árboles, random forest, SVM, regresión logística. La estrella era el *feature engineering* manual. El data scientist se rompía la cabeza extrayendo features a mano.
> - **2012:** AlexNet en ImageNet. Deep learning sale del laboratorio. La GPU pasa a ser commodity. El feature engineering empieza a delegarse a la red.
> - **2017:** sale el paper *Attention Is All You Need* de Vaswani y compañía en Google. Aparecen los Transformers. Casi nadie se dio cuenta de lo que acababa de pasar.
> - **2018–2020:** BERT, GPT-2, GPT-3. Escala bestial — GPT-3 tiene 175 mil millones de parámetros. Aparece el *few-shot learning*: el modelo resuelve tareas que nunca vio, sólo con ejemplos en el prompt.
> - **2022–2023:** ChatGPT estalla. El paper de ReAct (Yao et al., 2022) mete la idea de combinar razonamiento + acción, y el ecosistema arranca con los agentes.
> - **2024–2026:** Año de los agentes y del *agentic coding*. Anthropic publica "Building Effective Agents" en diciembre 2024. Claude Code sale en research preview en febrero 2025 y GA en mayo 2025. Anthropic comunicó oficialmente el 3 de diciembre 2025: *'In November, Claude Code achieved a significant milestone: just six months after becoming available to the public, it reached $1 billion in run-rate revenue.'*
>
> Hoy estamos parados acá: el LLM dejó de ser un chatbot de demo y se convirtió en un componente más del stack, que en muchos casos **escribe, ejecuta y verifica código solo**. Eso te cambia el laburo, y por eso este curso existe."

---

### 00:10–00:20 · 1.2 ¿Qué es un modelo de machine learning?

> "Bueno, conceptualmente: ¿de dónde sale un modelo de ML? Salió, literal, de la estadística aplicada. Si tomás una regresión lineal o logística — que es lo que usás cuando hacés `LogisticRegression()` en scikit-learn — eso es estadística pura de los años 50–60. Lo que cambió con el ML moderno fue la escala de los datos y la potencia de cómputo, no la idea de fondo: **encontrar la función que mejor explica los datos**.
>
> Repaso veloz porque esto ya lo saben:
>
> - **Regresión lineal/logística:** la base. Una combinación lineal de features. Interpretable, rápida, todavía sirve para un montón de cosas.
> - **Árboles de decisión:** una secuencia de `if`s aprendidos de los datos.
> - **Random Forest (Breiman, 2001):** muchos árboles entrenados sobre subsets distintos de datos y features, y se vota. Es el caballito de batalla de tabular hasta hoy.
> - **Gradient boosting (XGBoost, LightGBM, CatBoost):** árboles que aprenden de los errores de los árboles anteriores. Sigue ganando competencias de Kaggle en datos tabulares.
> - **SVM, KNN, Naïve Bayes:** los clásicos del clásico.
>
> Ahora, acá viene el análogo que me importa que se lleven. **Un modelo entrenado es un artefacto compilado a partir de datos.** Piénsenlo así:
>
> | Mundo DevOps | Mundo ML |
> |---|---|
> | Código fuente | Dataset de entrenamiento |
> | `Dockerfile` / build pipeline | Script de training (algoritmo + hiperparámetros) |
> | `docker build` | `model.fit()` |
> | Imagen de Docker | Modelo serializado (`.pkl`, `.joblib`, `.pt`, `.safetensors`) |
> | Registry (ECR, Harbor) | Model registry (MLflow, SageMaker) |
> | `docker run` | `model.predict()` / inference server |
> | Logs y métricas de runtime | Métricas de inferencia + drift |
>
> Cuando vos hacés `model.fit(X, y)` y después `joblib.dump(model, 'modelo.pkl')`, lo que estás haciendo es **compilar un binario a partir de datos**. Ese binario después lo subís a un registry, lo bajás, lo ponés detrás de un endpoint, y le pegás predicciones. Es un deploy igual al que ya hacés. La diferencia es que el "código fuente" son los datos, y el "compilador" es el algoritmo de entrenamiento. Y como cualquier binario, **es opaco**: vos no leés un Random Forest entrenado igual que leés un `.py`. Esa opacidad — la falta de interpretabilidad — es uno de los costos del paradigma."

---

### 00:20–00:30 · 1.3 Redes neuronales y backpropagation

> "Saltamos un escalón. Las redes neuronales son, en el fondo, una generalización: en vez de una combinación lineal de features, **encadeno muchas combinaciones lineales con no-linealidades en el medio**. Eso es todo. Cada 'neurona' es: `output = activación(W·x + b)`. Las apilás en capas, y tenés una red profunda.
>
> ¿Por qué funcionan tan bien? Por un teorema (el *universal approximation theorem*) que dice que con suficiente capacidad pueden aproximar cualquier función continua. Y por algo más práctico: aprenden las features solas. No necesitás el feature engineering manual del ML clásico.
>
> Ahora, la pregunta clave: **¿cómo se entrena una red?** Con backpropagation, que se publicó como técnica práctica en 1986 por Rumelhart, Hinton y Williams en *Nature* (paper 'Learning representations by back-propagating errors'). La idea, intuitiva, sin matemática:
>
> 1. La red tiene un montón de parámetros (pesos, `W`). Empiezan en valores random.
> 2. Le paso un ejemplo (entrada → predicción). La predicción va a ser pésima al principio.
> 3. Mido cuán pésima fue (loss function: cuánto se equivocó).
> 4. **Acá está la magia:** propago ese error hacia atrás por la red, calculando para cada parámetro 'cuánto contribuyó a equivocarse'. Eso es la derivada parcial de la loss respecto a cada peso — el gradiente.
> 5. Ajusto cada parámetro un poquito en la dirección que reduce el error (descenso de gradiente).
> 6. Repito millones de veces.
>
> La analogía que les sirve: es un **CI loop infinito**, donde el test es 'qué tan lejos estuvo la predicción del label', y el `git commit --amend` automático ajusta los pesos. El modelo se equivoca, se corrige, se equivoca, se corrige. Por eso entrenar es caro: son millones de iteraciones de forward + backward.
>
> [**Acá corremos la Demo 1: descenso de gradiente 2D.** Mostrar la superficie de loss, el punto rojo bajando hacia el mínimo, paso a paso. Decir mientras corre: 'esto es lo que está pasando, multiplicado por millones de parámetros y millones de ejemplos, dentro de cada red neuronal que entrenan'.]"

---

### 00:30–00:42 · 1.4 Embeddings: coordenadas GPS del significado

> "Ahora viene el concepto que más me importa que se lleven, porque es el puente conceptual hacia los LLMs: **embeddings**.
>
> Pregunta: ¿cómo le hago tragar a una red neuronal la palabra 'perro'? La red espera números, no strings. La primera idea ingenua es *one-hot encoding*: tengo un vocabulario de, digamos, 50.000 palabras, y a cada una le asigno un vector de 50.000 dimensiones con un 1 en su posición y ceros en el resto. Funciona, pero es horrible: cada palabra es ortogonal a las demás, 'perro' y 'gato' están tan lejos entre sí como 'perro' y 'factura'. No hay noción de significado.
>
> La idea de los embeddings es la opuesta: **represento cada palabra como un vector denso de unas pocas dimensiones (típicamente 100, 300, 768, 1536, 3072 según el modelo), y entreno la red para que palabras con significados parecidos terminen cerca en ese espacio vectorial.**
>
> El paper canónico es Word2Vec de Mikolov y compañía en Google, 2013 ('Efficient Estimation of Word Representations in Vector Space', arXiv:1301.3781). Después vino GloVe de Pennington, Socher y Manning en Stanford, 2014. La intuición de los dos: *"una palabra se define por la compañía que mantiene"* (la hipótesis distribucional de Firth). Si 'perro' y 'gato' aparecen en contextos parecidos ('mi ___ ladra', 'mi ___ duerme', 'compré comida para mi ___'), el algoritmo los acerca en el espacio.
>
> El resultado famoso: `vector('rey') - vector('hombre') + vector('mujer') ≈ vector('reina')`. **Aritmética sobre significado.** Eso, en 2013, voló cabezas.
>
> La analogía que les sirve: pensálo como **coordenadas GPS del significado**. Buenos Aires está cerca de Montevideo y lejos de Tokio en el mapa físico. 'perro' está cerca de 'gato' y lejos de 'factura' en el mapa semántico. Y la métrica que usamos para medir distancia es la **similitud coseno** — el coseno del ángulo entre los vectores. Cerca de 1: muy parecidos. Cerca de 0: no tienen nada que ver. Negativo: opuestos.
>
> Esto es la base de **RAG** (Retrieval-Augmented Generation), de los buscadores semánticos, de los recomendadores modernos, de la deduplicación de tickets, de la detección de fraude — de medio stack moderno.
>
> [**Acá corremos la Demo 2: embeddings y similitud coseno con `sentence-transformers`.** Mostrar que 'perro' y 'gato' tienen similitud ~0.5, 'perro' y 'factura' ~0.05, y dos paráfrasis del mismo concepto ~0.85. Mientras corre el `.encode()`, decir: 'fíjense que esto está corriendo localmente, sin API key. El modelo `all-MiniLM-L6-v2` pesa 80 megas y mete cada frase en 384 dimensiones'.]"

---

### 00:42–00:54 · 1.5 Transformers y atención: la revolución

> "Bueno, ya tenemos embeddings: palabras → vectores. Ahora la pregunta es cómo procesamos una **secuencia** de esos vectores. Hasta 2017 la respuesta era: redes recurrentes (RNN, LSTM, GRU). Procesabas la oración palabra por palabra, manteniendo un estado oculto. Problema 1: la dependencia entre palabras lejanas se diluía. Problema 2: era inherentemente secuencial — no podías paralelizar el entrenamiento, lo cual con datasets grandes era la muerte.
>
> En junio de 2017 se publica *Attention Is All You Need* (Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser y Polosukhin — Google). Proponen una arquitectura nueva, el **Transformer**, que tira las RNN a la basura y se queda sólo con el mecanismo de atención.
>
> La idea de la atención, en lenguaje humano: cuando estás procesando una palabra de la oración, en vez de tener un estado oculto que arrastraste palabra por palabra, **cada palabra mira a todas las otras palabras de la oración simultáneamente** y decide a cuáles 'prestarle atención' para entenderse a sí misma.
>
> Ejemplo: 'El gato que vi ayer en el parque estaba durmiendo.' Cuando el modelo procesa 'estaba', necesita saber que el sujeto es 'gato' (que está 6 palabras atrás). La atención le permite ir directo, en un solo paso, a 'gato', sin tener que arrastrar información a través de 'que', 'vi', 'ayer', 'en', 'el', 'parque'.
>
> Mecánicamente: cada token genera tres vectores — **Query** ('qué estoy buscando'), **Key** ('qué ofrezco') y **Value** ('qué información tengo'). El producto punto Query·Key entre dos tokens te dice cuánta atención el primero le presta al segundo. Se aplica un softmax para que las atenciones sumen 1, y se pondera la suma de los Values. *Scaled dot-product attention*, fórmula 1 del paper.
>
> Encima de eso, **multi-head attention**: hacés esto varias veces en paralelo con cabezales distintos, cada uno aprende a mirar relaciones diferentes (sintácticas, semánticas, de correferencia).
>
> ¿Por qué fue una revolución? Por dos razones combinadas:
>
> 1. **Paraleliza.** Como cada token se computa con todos los demás simultáneamente, podés tirarle todas las GPUs que tengas. Eso destrabó la escala.
> 2. **Captura contexto largo.** No hay 'pérdida de señal' por distancia.
>
> Sin Transformers no había GPT, no había BERT, no había Claude, no había Gemini. **Toda la IA generativa moderna está parada arriba de ese paper de 2017.**
>
> Análogo MLOps: si las RNN eran un build secuencial (un step espera al anterior, como Jenkins viejo), los Transformers son un build masivamente paralelo (todos los steps en paralelo en un cluster, como Buildkite o Bazel bien armado). Misma diferencia de orden de magnitud en performance.
>
> [**Acá corremos la Demo 3: mapa de atención.** Una oración corta, el heatmap muestra qué token mira a cuál. Decir: 'fíjense cómo 'gato' atrae la atención de 'durmiendo' — el modelo aprendió solo, sin que nadie le dijera explícitamente qué es el sujeto'.]"

---

### 00:54–01:04 · 1.6 De transformers a LLMs: la conexión completa

> "Bueno, ya tenemos la arquitectura. ¿Cómo se llega de un Transformer a un LLM como GPT, Claude o Llama?
>
> La receta — sorprendentemente simple en concepto — es:
>
> 1. **Tomá un Transformer decoder-only** (sólo la mitad derecha del paper original, la que genera).
> 2. **Escalalo bestialmente:** miles de millones de parámetros. GPT-3 tuvo 175B; los frontier de 2025 son bastante más grandes y muchos no publican el número.
> 3. **Entrenalo con una tarea tonta:** predecir la siguiente palabra (en realidad, el siguiente *token* — que es un trozo de palabra) sobre una porción enorme de internet. Trillions de tokens.
> 4. Después fine-tuning con instrucciones humanas y RLHF/RLAIF para alinearlo.
>
> Eso es todo. **Un LLM es, fundamentalmente, un autocomplete cósmico.** Le das un prompt, y va prediciendo token por token cuál es la continuación más probable según lo que vio en entrenamiento.
>
> Dos consecuencias técnicas que les importan a ustedes como MLOps:
>
> **Primera: tokenización.** El LLM no ve strings. Ve enteros. El tokenizador parte el texto en pedacitos (típicamente BPE — Byte Pair Encoding) y cada pedacito tiene un ID en un vocabulario fijo. Para los modelos de OpenAI:
>
> - `cl100k_base` — GPT-3.5, GPT-4 (vocabulario ~100k).
> - `o200k_base` — GPT-4o, GPT-4.1, GPT-5, la familia o1/o3/o4 (vocabulario ~200k, mejor para multilingüe y código). Esto está documentado en `tiktoken/model.py` del repo oficial de OpenAI.
>
> Cuando facturás por tokens, cuando calculás context windows, cuando hacés batching — todo es a nivel token. Hay que pensarlo así.
>
> **Segunda: NO ES DETERMINÍSTICO.** Y esto es lo que más les va a chocar. Un Random Forest, dado el mismo input, te da siempre el mismo output. **Un LLM, no.** En cada paso de generación, en vez de elegir el token de probabilidad más alta, **muestrea** de la distribución (controlada por hiperparámetros como `temperature`, `top_p`, `top_k`). Eso quiere decir:
>
> - **Mismo prompt → outputs diferentes.** El testing tradicional (assert igualdad) se rompe.
> - **No podés hacer regression testing sobre el output literal.** Hay que evaluar por propiedades, por LLM-as-judge, por golden sets con tolerancia semántica.
> - **El monitoreo de drift se complica.** No es sólo distribución de inputs, también de outputs.
> - **Reproducibilidad parcial:** podés fijar `temperature=0` y `seed`, pero igual no es totalmente determinístico en ambientes con paralelismo de hardware. Y, fundamentalmente, el modelo subyacente cambia: el proveedor te actualiza el modelo y tu test 'flaky' aparece de la nada. Hay que versionar el modelo explícitamente.
>
> Análogo: pensálo como una API externa que devuelve **respuestas similares pero no idénticas** y que el proveedor puede actualizar sin avisar. Hay que diseñar el sistema asumiendo eso desde el día cero — caching agresivo, idempotencia donde puedas, validación de schema en outputs, retries con backoff, y observability fuerte.
>
> [**Acá corremos la Demo 4: tokenización con `tiktoken`.** Mostrar cómo 'Hola, ¿cómo andás che?' se parte en tokens; comparar `cl100k_base` vs `o200k_base`; mostrar que el español 'gasta' más tokens que el inglés. Decir: 'cada uno de estos enteros es lo que el modelo realmente ve; cuando OpenAI te factura por tokens, te factura por estos numeritos'.]"

---

### 01:04–01:12 · 1.7 Agentes de IA: de predecir texto a ejecutar acciones

> "Último bloque, y el más importante para el resto del curso. Hasta acá tenemos un LLM, que dado un prompt, **genera texto.** Punto. Es un autocomplete muy bueno, pero sigue siendo un autocomplete. ¿Qué le falta para ser útil de verdad en un sistema productivo?
>
> Le falta poder **hacer cosas en el mundo**. Llamar APIs, leer archivos, ejecutar comandos, consultar bases de datos, escribir código, correr tests. Ahí entra el concepto de **agente**.
>
> Anthropic, en su artículo *'Building Effective Agents'* (diciembre 2024), lo define así, textual: *'Workflows are systems where LLMs and tools are orchestrated through predefined code paths. Agents, on the other hand, are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks.'*
>
> Más en concreto, en la página oficial de Claude Code definen un sistema agéntico así, textual: *'An agentic system acts toward a goal with a degree of autonomy, rather than responding to one prompt at a time. Claude Code reads a codebase, plans a sequence of actions, executes them using real development tools, evaluates the result, and adjusts its approach.'*
>
> El loop conceptual — formalizado por Yao et al. en el paper **ReAct** (2022, arXiv:2210.03629) — es:
>
> ```
>     ┌──────────────────────────────────────┐
>     │                                      │
>     ▼                                      │
>  PENSAR (reasoning) ──► ACTUAR (tool call) ──► OBSERVAR (resultado)
>                                              │
>                                              └──► ¿terminé? sí → fin / no → loop
> ```
>
> El LLM piensa qué hacer, llama a una herramienta (una función, una API, un comando de shell), recibe el resultado, lo incorpora al contexto, y vuelve a pensar. Itera hasta que considera que cumplió el objetivo. Anthropic lo describe textual así: *'Agents begin their work with either a command from, or interactive discussion with, the human user. Once the task is clear, agents plan and operate independently, potentially returning to the human for further information or judgement. During execution, it's crucial for the agents to gain ground truth from the environment at each step (such as tool call results or code execution) to assess its progress.'*
>
> El bloque mínimo, según Anthropic, es el **'augmented LLM'**: un LLM con tres aumentos — *retrieval* (buscar info externa, típicamente con RAG), *tools* (llamar funciones) y *memory* (recordar entre pasos). Sobre ese bloque se construyen patrones más complejos: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer loops.
>
> En el post *Building agents with the Claude Agent SDK* (septiembre 2025), Anthropic resume el principio de diseño: *'The key design principle behind the Claude Agent SDK is to give your agents a computer, allowing them to work like humans do.'* Bash, edición de archivos, búsqueda, ejecución de código — las mismas herramientas que usás vos.
>
> **Impacto concreto en desarrollo de software (2025–2026):**
>
> Esto ya no es teoría. Claude Code (Anthropic), Cursor, GitHub Copilot Agent Mode, Codex CLI, Devin — todos son agentes que **escriben, ejecutan y verifican código**. Los números que están saliendo son inéditos. Cito de la página oficial de Claude Code:
>
> - Anthropic comunicó oficialmente (3 de diciembre 2025): *'In November, Claude Code achieved a significant milestone: just six months after becoming available to the public, it reached $1 billion in run-rate revenue.'*
> - **Stripe:** *'Stripe deployed Claude Code across 1,370 engineers of all levels through a zero-configuration enterprise binary. One team completed a 10,000-line Scala-to-Java migration in four days, work estimated at ten engineer-weeks.'*
> - **Ramp:** *'Ramp integrated Claude Code into their development workflow and cut incident investigation time by 80%.'*
> - **Wiz:** *'Wiz migrated a 50,000-line Python library to Go in roughly 20 hours of active development, a project the team estimated at two to three months of manual work.'*
> - **Rakuten:** *'Rakuten reduced the average delivery time for new features from 24 working days to 5.'*
>
> El paradigma del rol del desarrollador está cambiando. **Vos pasás de tipear cada línea a diseñar la fábrica, configurar las máquinas, y revisar el output.**
>
> Hay que ser honestos con los datos: no es todo color de rosa.
>
> - El estudio **METR** (Becker, Rush, Barnes & Rein, *'Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity'*, arXiv:2507.09089, julio 2025), un ensayo aleatorizado con 16 devs experimentados usando principalmente Cursor Pro con Claude 3.5/3.7 Sonnet, encontró que los devs **se hicieron un 19% más lentos** con la herramienta, aunque ellos mismos esperaban un 24% de speedup antes de empezar y se autopercibieron 20% más rápidos después.
> - El **2025 GenAI Code Security Report de Veracode** (basado en 100+ LLMs evaluados en 80 tareas de coding en Java, JS, Python y C#) encontró, citando textual: *'when given a choice between a secure and insecure method to write code, GenAI models chose the insecure option 45 percent of the time.'*
> - **Gartner** (press release del 25 de junio 2025, vocera Anushree Verma) predice que **más del 40% de los proyectos de IA agéntica van a ser cancelados** antes de fin de 2027, con el argumento de que *'most agentic AI projects right now are early stage experiments or proof of concepts that are mostly driven by hype and are often misapplied.'*
> - El reporte **DORA 2025** (*State of AI-assisted Software Development*, Google Cloud/DORA, ~5.000 profesionales encuestados) resume así su hallazgo central, textual: *'It magnifies the strengths of high-performing organizations and the dysfunctions of struggling ones.'*
>
> La fábrica automatizada produce más, pero también produce defectos más rápido si no hay control de calidad. Esto es justamente por lo que están haciendo este curso, y por lo que el módulo siguiente entra a fondo en **tools y skills**: porque saber prendar el agente no alcanza — hay que saber armarlo bien, darle el contexto correcto, las herramientas correctas, los guardrails correctos.
>
> Hoy no entramos en eso. Hoy quería que se llevaran **la imagen mental** del agente: un loop donde el LLM piensa, actúa, observa, e itera. Esa imagen es la que va a estar atrás de todo el resto del curso."

---

### 01:12–01:15 · Cierre y puente

> "Cerremos. En 75 minutos cruzamos el puente entero:
>
> 1. ML clásico es estadística aplicada que produce **artefactos compilados** desde datos.
> 2. Las redes neuronales y backprop generalizan eso: aprenden las features solas mediante un loop de error/corrección.
> 3. Los **embeddings** convierten significado en coordenadas geométricas: la base del NLP moderno y de RAG.
> 4. Los **Transformers** rompen la secuencialidad con atención, destrabando la escala.
> 5. Los **LLMs** son Transformers gigantes entrenados para autocompletar — potentes pero **no determinísticos** y caros de operar.
> 6. Los **agentes** convierten al LLM en un sistema que **actúa**: piensa, llama tools, observa, itera.
>
> El gran cambio que ya está ocurriendo en su carrera es: **van a dejar de implementar y empezar a orquestar**. Y para orquestar bien necesitan entender qué hay adentro de la caja. Eso fue esto. La próxima clase entramos a tools, skills y patrones de diseño de agentes, ahora sí con las manos en la masa. ¿Preguntas?"

---

## 3) Outline de slides

> Diapositivas pensadas para proyectar. Cada bullet es una línea de la slide. El instructor expande oralmente con el guion.

### Slide 0 — Portada
- **Fundamentos de IA**
- Módulo 1 · Clase 1 · 75 min
- Curso de IA Aplicada para MLOps
- Subtítulo: *De random forests a agentes — el puente conceptual*

### Slide 1 — Hoja de ruta
- Lo que vos ya sabés: Docker, IaC, CI/CD, pipelines, training, serving
- Lo que vamos a tender hoy: el puente hacia LLMs y agentes
- Regla: no explicamos lo que ya sabés; sí lo usamos como analogía
- 4 demos en vivo, 1 notebook, todo local

### Slide 2 — Línea de tiempo (ancla)
- 2001 · Random Forest (Breiman) — tabular sigue acá hoy
- 2012 · AlexNet — deep learning sale del lab
- 2013 · Word2Vec (Mikolov) — embeddings
- 2017 · Attention Is All You Need (Vaswani et al.) — Transformers
- 2018–2020 · BERT, GPT-2, GPT-3 — escala
- 2022 · ReAct (Yao et al.) + ChatGPT
- 2024 · Anthropic "Building Effective Agents"
- 2025 · Claude Code GA · $1B run-rate revenue en noviembre (Anthropic, dic 2025)

### Slide 3 — 1.1 De reglas a patrones
- Software tradicional: programás *qué hacer*
- ML: programás *cómo aprender*
- El programador escribe el algoritmo; los datos definen el comportamiento
- Costo: opacidad, no determinismo, dependencia de los datos

### Slide 4 — 1.2 Modelo de ML = artefacto compilado
- `fit(X, y)` ≈ `docker build`
- `.pkl` / `.safetensors` ≈ imagen de Docker
- Model registry ≈ container registry
- `predict()` ≈ `docker run`
- Random Forest, gradient boosting, regresión: clásicos vigentes
- Breiman 2001 — *Random Forests*, *Machine Learning* 45(1):5–32

### Slide 5 — 1.3 Redes neuronales en una transparencia
- Apilamiento de `activación(W·x + b)`
- Aprenden features solas → adiós feature engineering manual
- Backprop (Rumelhart, Hinton, Williams · *Nature* 323:533–536, 1986)
- Loop: predecir → medir error → propagar error → ajustar pesos → repetir
- Analogía: CI loop infinito con auto-fix

### Slide 6 — Demo 1
- Descenso de gradiente 2D
- Una superficie de loss, un punto rojo bajando al mínimo
- "Esto, multiplicado por millones de parámetros"

### Slide 7 — 1.4 Embeddings: coordenadas GPS del significado
- One-hot encoding: cada palabra ortogonal → no captura significado
- Embedding: vector denso (100–3072 dim) donde proximidad = similitud semántica
- `rey - hombre + mujer ≈ reina`
- Word2Vec (Mikolov et al. 2013, arXiv:1301.3781)
- GloVe (Pennington, Socher, Manning · EMNLP 2014, pp. 1532–1543)
- Métrica: similitud coseno
- Base de: RAG, búsqueda semántica, recomendadores, deduplicación

### Slide 8 — Demo 2
- `sentence-transformers` · modelo `all-MiniLM-L6-v2` · 384 dim, ~80 MB, local
- "perro" ↔ "gato" vs "perro" ↔ "factura"
- Paráfrasis vs cosas no relacionadas

### Slide 9 — 1.5 Transformers y atención
- Pre-2017: RNN/LSTM secuenciales, pérdida de contexto largo, no paralelizables
- 2017: *Attention Is All You Need* — Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin (Google) — arXiv:1706.03762
- Idea: cada token mira a todos los demás simultáneamente
- Query · Key · Value; scaled dot-product attention; multi-head
- Resultado: paraleliza + captura contexto largo → escala sin techo

### Slide 10 — Demo 3
- Mapa de calor de atención sobre una oración
- "Fíjense qué token mira a cuál"

### Slide 11 — 1.6 De Transformers a LLMs
- LLM = Transformer decoder-only escalado + entrenado para predecir el próximo token
- GPT-3 (Brown et al. 2020, arXiv:2005.14165): 175B parámetros, *few-shot learning*
- BERT (Devlin et al. 2018, arXiv:1810.04805): encoder, fundacional para embeddings y NLU
- Tokenización: `cl100k_base` (GPT-4) · `o200k_base` (GPT-4o, GPT-5, o1/o3/o4)
- **NO determinístico** → testing y observability se replantean

### Slide 12 — Implicancias MLOps del no-determinismo
- Mismo input → outputs diferentes
- Adiós a `assert output == "..."` en tests
- Hola a: LLM-as-judge, golden sets semánticos, eval datasets
- Versioná el modelo explícitamente (el proveedor lo actualiza)
- `temperature=0` ayuda pero no es garantía total
- Caching, idempotencia, schema validation, retries

### Slide 13 — Demo 4
- `tiktoken` · `cl100k_base` vs `o200k_base`
- "Hola, ¿cómo andás che?"
- El español gasta más tokens que el inglés ($$ y context window)

### Slide 14 — 1.7 De LLM a Agente
- LLM solo: genera texto
- Agente: **planifica, usa tools, ejecuta acciones, observa, itera**
- Loop ReAct (Yao et al. 2022, arXiv:2210.03629): Reasoning + Acting
- Bloque mínimo: *augmented LLM* = LLM + retrieval + tools + memory
- Anthropic (2024): workflows (camino predefinido) vs agents (autónomos)

### Slide 15 — Impacto en software (2025–2026)
- Claude Code GA mayo 2025; $1B run-rate revenue en noviembre 2025 (Anthropic, 3-dic-2025)
- Stripe: 1.370 ingenieros, 10k LOC Scala→Java en 4 días (vs 10 engineer-weeks estimadas)
- Ramp: -80% en tiempo de investigación de incidentes
- Wiz: 50k LOC Python→Go en ~20 horas (vs 2-3 meses estimados)
- Rakuten: delivery de features de 24 a 5 días hábiles
- Contraste: METR 2025 (arXiv:2507.09089) → devs experimentados 19% más lentos
- Veracode 2025 GenAI Code Security Report → modelos eligen método inseguro en 45% de los casos
- Gartner (jun-2025): >40% de proyectos agénticos cancelados antes de fin de 2027
- DORA 2025: *"It magnifies the strengths of high-performing organizations and the dysfunctions of struggling ones."*

### Slide 16 — Tu rol está cambiando
- De *"write code, run tests, fix, repeat"*
- A *"set goal, review changes, approve implementation"*
- Diseñás la fábrica, no atornillás cada pieza
- Próxima clase: tools, skills, patrones de diseño de agentes

### Slide 17 — Cierre
- 6 ideas en una transparencia (recap)
- Preguntas

---

## 4) Apéndice — Notebook ejecutable

> **Archivo:** `fundamentos_ia.ipynb` (Jupyter / Colab compatible)
> **Probado contra:** Python 3.10+, `tiktoken>=0.7`, `sentence-transformers>=3.0` (probado también con 5.x), `numpy`, `matplotlib`, `torch>=1.11`
> **Tiempo total estimado de ejecución en una notebook moderna sin GPU:** ~2 minutos (la primera vez baja el modelo MiniLM, ~80 MB).

### Celda 0 — Instalación

```python
# === Instalación de dependencias ===
# En Colab descomentá la línea siguiente. En un entorno local con venv,
# ejecutalo una vez fuera del notebook (más limpio).
# !pip install -q tiktoken sentence-transformers matplotlib numpy

# Verificamos versiones
import importlib, sys
for pkg in ["tiktoken", "sentence_transformers", "numpy", "matplotlib", "torch"]:
    try:
        m = importlib.import_module(pkg)
        print(f"{pkg:25s} {getattr(m, '__version__', '?')}")
    except ImportError:
        print(f"{pkg:25s} NO INSTALADO")
```

**Qué decir mientras corre:** "Cero API keys, cero secretos, cero costos. Todo corre local. El modelo de embeddings se descarga la primera vez de Hugging Face — son 80 MB."

---

### Celda 1 — Demo 1: descenso de gradiente 2D (1.3 Backprop)

```python
"""
Demo 1 — Descenso de gradiente 2D.
Objetivo: visualizar 'el modelo se equivoca y se ajusta'.
Una loss function simple en R² (paraboloide elíptico) y un punto que
baja al mínimo siguiendo el gradiente negativo.
"""
import numpy as np
import matplotlib.pyplot as plt

# 1) Definimos una "loss function" 2D — un paraboloide elíptico.
#    Imaginá que w1 y w2 son dos parámetros (pesos) de un modelo y
#    L(w1,w2) es el error en el dataset de entrenamiento.
def loss(w1, w2):
    return (w1 - 3)**2 + 4 * (w2 + 2)**2

def grad(w1, w2):
    # Gradiente analítico: derivadas parciales.
    return np.array([2 * (w1 - 3), 8 * (w2 + 2)])

# 2) Descenso de gradiente: arrancamos lejos del mínimo (que está en (3, -2)).
lr = 0.1            # learning rate
w = np.array([-4.0, 3.0])  # punto inicial
trayectoria = [w.copy()]
for step in range(40):
    w = w - lr * grad(*w)
    trayectoria.append(w.copy())
trayectoria = np.array(trayectoria)

# 3) Visualización: contornos de la loss + trayectoria.
w1g, w2g = np.meshgrid(np.linspace(-6, 6, 200), np.linspace(-6, 6, 200))
Lg = loss(w1g, w2g)

fig, ax = plt.subplots(figsize=(8, 6))
cs = ax.contour(w1g, w2g, Lg, levels=20, cmap="viridis")
ax.clabel(cs, inline=True, fontsize=8)
ax.plot(trayectoria[:, 0], trayectoria[:, 1], "ro-", markersize=5, linewidth=1.5,
        label="Trayectoria del optimizador")
ax.scatter([3], [-2], c="gold", s=200, marker="*",
           edgecolors="black", label="Mínimo (parámetros óptimos)")
ax.scatter([trayectoria[0, 0]], [trayectoria[0, 1]], c="red", s=120,
           edgecolors="black", label="Inicio (pesos random)")
ax.set_xlabel("w₁ (peso 1)")
ax.set_ylabel("w₂ (peso 2)")
ax.set_title("Descenso de gradiente: el modelo se equivoca y se ajusta")
ax.legend()
plt.tight_layout()
plt.show()

print(f"Loss inicial: {loss(*trayectoria[0]):.4f}")
print(f"Loss final:   {loss(*trayectoria[-1]):.4f}")
print(f"Pasos: {len(trayectoria) - 1}")
```

**Qué decir mientras corre:**
> "El punto rojo es el estado de los parámetros. La estrella dorada es el óptimo. Cada paso de descenso es: 'medí cuánto te equivocaste, calculá el gradiente — la dirección de mayor subida — y movete en la dirección opuesta'. Esto es backprop: lo mismo pero en miles de millones de dimensiones, no en dos. Y el `learning_rate` es exactamente el `lr` que escribimos arriba: si lo subís mucho, el punto pega saltos y diverge; si lo bajás mucho, tarda una eternidad."

---

### Celda 2 — Demo 2: embeddings y similitud coseno (1.4 Embeddings)

```python
"""
Demo 2 — Embeddings y similitud coseno con sentence-transformers (LOCAL).
Modelo: all-MiniLM-L6-v2 (384 dim, ~80 MB, sin API key, CPU OK).
Doc oficial: https://www.sbert.net/
"""
from sentence_transformers import SentenceTransformer
import numpy as np

# 1) Cargamos el modelo. La primera vez se baja de Hugging Face.
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print(f"Modelo cargado. Dimensión de embedding: {model.get_sentence_embedding_dimension()}")

# 2) Frases de prueba — mezcla de español rioplatense y conceptos diversos.
frases = [
    "El perro corre por el parque",       # 0
    "Mi gato duerme arriba del sillón",   # 1 — animal doméstico, similar a 0
    "El cachorro persigue una pelota",    # 2 — paráfrasis de 0
    "Pagué la factura de la luz ayer",    # 3 — tema totalmente distinto
    "Tengo que abonar el servicio eléctrico",  # 4 — paráfrasis de 3
    "La inflación de Argentina en 2025",  # 5 — otro tema más
]

# 3) Codificamos. El método .encode() devuelve un np.ndarray (N, 384).
embeddings = model.encode(frases, convert_to_numpy=True, normalize_embeddings=True)
print(f"Shape de la matriz de embeddings: {embeddings.shape}")

# 4) Como normalizamos (norma L2 = 1), el producto interno = similitud coseno.
sim = embeddings @ embeddings.T

# 5) Mostramos la matriz formateada.
print("\nMatriz de similitud coseno (1.00 = idéntico, 0.00 = no relacionado):")
print("       ", " ".join(f"f{i:>4}" for i in range(len(frases))))
for i, fila in enumerate(sim):
    print(f"f{i:>2}    ", " ".join(f"{v: .2f}" for v in fila))

# 6) Casos puntuales que queremos resaltar en clase.
def comparar(i, j):
    print(f"sim('{frases[i]}',\n    '{frases[j]}') = {sim[i, j]:.3f}")

print("\n--- Casos puntuales ---")
comparar(0, 1)  # perro vs gato — animales domésticos
comparar(0, 2)  # perro vs cachorro persigue pelota — paráfrasis
comparar(0, 3)  # perro vs factura — sin relación
comparar(3, 4)  # factura vs abonar servicio — paráfrasis administrativa
comparar(0, 5)  # perro vs inflación — sin relación
```

**Qué decir mientras corre:**
> "Fíjense en tres cosas. Uno: 'perro corre por el parque' y 'gato duerme en el sillón' tienen similitud relativamente alta porque comparten el espacio semántico de 'animal doméstico'. Dos: 'perro corre' y 'cachorro persigue pelota' son paráfrasis y van a estar todavía más cerca. Tres: 'perro' vs 'factura de la luz' están casi en cero. Esto es lo que está atrás de **RAG**, de la búsqueda semántica de Notion o Google Drive, de los recomendadores de Spotify. Y el modelo pesa 80 megas, corre en una laptop sin GPU."

**Resultados típicos (orden de magnitud):**
- perro/gato ≈ 0.50
- perro/cachorro persigue pelota ≈ 0.65
- perro/factura ≈ 0.05
- factura/abonar servicio ≈ 0.65
- perro/inflación ≈ 0.00

---

### Celda 3 — Demo 3: mini-visualización de atención (1.5 Transformers)

```python
"""
Demo 3 — Mini-visualización del mecanismo de atención.
Calculamos manualmente *scaled dot-product attention* sobre una oración corta,
usando los embeddings de all-MiniLM-L6-v2 como Q, K y V (simplificación didáctica).
Mostramos un heatmap: qué token le presta atención a cuál.

Fórmula (Vaswani et al. 2017, ec. 1):
    Attention(Q, K, V) = softmax( Q · Kᵀ / sqrt(d_k) ) · V
"""
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 1) Oración y tokenización palabra-por-palabra (didáctico — el tokenizador
#    real parte en subwords, pero esto se entiende mejor visualmente).
oracion = "El gato que vi ayer en el parque estaba durmiendo"
tokens = oracion.split()
print(f"Tokens: {tokens}")

# 2) Embeddings por token (cada palabra, sola, codificada).
#    Esto es una simplificación: en un Transformer real Q, K, V son
#    proyecciones lineales del embedding contextual, no el embedding crudo.
emb = model.encode(tokens, convert_to_numpy=True, normalize_embeddings=False)
d_k = emb.shape[1]
print(f"Embeddings shape: {emb.shape}  (n_tokens={emb.shape[0]}, d_k={d_k})")

# 3) Scaled dot-product attention con Q = K = V = embeddings (self-attention).
scores = emb @ emb.T / np.sqrt(d_k)
# Softmax por fila (cada token distribuye 1.0 de "atención" entre todos).
exp_scores = np.exp(scores - scores.max(axis=1, keepdims=True))
attn = exp_scores / exp_scores.sum(axis=1, keepdims=True)

# 4) Heatmap.
fig, ax = plt.subplots(figsize=(9, 7))
im = ax.imshow(attn, cmap="viridis", aspect="auto")
ax.set_xticks(range(len(tokens)))
ax.set_yticks(range(len(tokens)))
ax.set_xticklabels(tokens, rotation=45, ha="right")
ax.set_yticklabels(tokens)
ax.set_xlabel("Token clave (a quién se mira)")
ax.set_ylabel("Token query (quién mira)")
ax.set_title("Self-attention: ¿quién mira a quién?")
for i in range(len(tokens)):
    for j in range(len(tokens)):
        ax.text(j, i, f"{attn[i, j]:.2f}", ha="center", va="center",
                color="white" if attn[i, j] < 0.15 else "black", fontsize=8)
plt.colorbar(im, ax=ax)
plt.tight_layout()
plt.show()
```

**Qué decir mientras corre:**
> "Esto es una simplificación didáctica — en un Transformer real, Q, K y V son proyecciones lineales aprendidas, no el embedding crudo, y hay múltiples cabezales (multi-head). Pero la mecánica visual es ésta: cada fila es un token preguntando 'a quién tengo que prestar atención para entenderme'. En una red real, después de entrenar trillones de tokens, distintos cabezales se especializan: uno aprende correferencia sujeto-verbo, otro aprende sintaxis, otro semántica. **Si quieren la visualización en un modelo real entrenado, miren `BertViz`** de Jesse Vig — está en `pip install bertviz`. La opción adicional, por si querés mostrar también la atención real de un BERT, está al pie de esta sección."

**Variante opcional con BertViz (modelo real entrenado):**

```python
# Opcional: visualización con un modelo Transformer real.
# Requiere: pip install bertviz transformers
# from transformers import AutoTokenizer, AutoModel, utils
# from bertviz import head_view
# utils.logging.set_verbosity_error()
# model_name = "distilbert-base-multilingual-cased"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# m = AutoModel.from_pretrained(model_name, output_attentions=True)
# inputs = tokenizer("El gato que vi ayer estaba durmiendo", return_tensors="pt")
# outputs = m(**inputs)
# tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
# head_view(outputs.attentions, tokens)
```

---

### Celda 4 — Demo 4: tokenización con `tiktoken` (1.6 LLMs)

```python
"""
Demo 4 — Tokenización con tiktoken (OpenAI).
Doc oficial: https://github.com/openai/tiktoken
Encodings principales (ver tiktoken/model.py en el repo):
    cl100k_base — GPT-3.5, GPT-4
    o200k_base  — GPT-4o, GPT-4.1, GPT-5, o1/o3/o4
"""
import tiktoken

# 1) Cargamos dos encodings para comparar.
enc_cl = tiktoken.get_encoding("cl100k_base")   # GPT-4
enc_o2 = tiktoken.get_encoding("o200k_base")    # GPT-4o, GPT-5, o-family

# Alternativa equivalente:
# enc_o2 = tiktoken.encoding_for_model("gpt-4o")

textos = [
    "Hello, how are you today?",
    "Hola, ¿cómo andás che?",
    "El gato corre por el parque y persigue una pelota roja.",
    "import numpy as np\nx = np.zeros((10, 10))",
    "🚀 La IA está cambiando todo en 2026 🤖",
]

def mostrar(enc, texto, nombre):
    ids = enc.encode(texto)
    piezas = [enc.decode_single_token_bytes(t).decode("utf-8", errors="replace")
              for t in ids]
    print(f"\n[{nombre}] {texto!r}")
    print(f"  {len(ids)} tokens")
    print(f"  IDs:    {ids}")
    print(f"  Pieces: {piezas}")

for t in textos:
    mostrar(enc_cl, t, "cl100k_base (GPT-4)")
    mostrar(enc_o2, t, "o200k_base  (GPT-4o/5)")
    print("-" * 70)

# 2) Round-trip de verificación (encode → decode da el original).
ejemplo = "Hola che, ¿probamos los agentes hoy?"
assert enc_o2.decode(enc_o2.encode(ejemplo)) == ejemplo
print("\nRound-trip OK ✓")

# 3) Utilidad: contar tokens (lo que te factura el proveedor).
def contar_tokens(texto, modelo="gpt-4o"):
    enc = tiktoken.encoding_for_model(modelo)
    return len(enc.encode(texto))

print(f"\nTokens en castellano vs inglés (mismo significado):")
print(f"  EN: {contar_tokens('Hello, how are you today?')} tokens")
print(f"  ES: {contar_tokens('Hola, ¿cómo andás che?')} tokens")
```

**Qué decir mientras corre:**
> "Tres observaciones. Una: el español 'gasta' más tokens que el inglés para el mismo significado — eso impacta directo el costo de API y el uso del context window. Dos: el código y los emojis se tokenizan distinto que el texto plano. Tres: `o200k_base` (el de GPT-4o y GPT-5) suele usar menos tokens que `cl100k_base` para texto multilingüe — por eso OpenAI lo introdujo. Cuando estimen costos de un sistema con LLM, **no estimen por caracteres ni por palabras, estimen por tokens** — son entre 0,75 y 4 caracteres por token según el idioma."

---

### Celda 5 — Cierre: anclaje conceptual

```python
"""
Recap conceptual del notebook:
1) Backprop = optimizador que ajusta parámetros minimizando una loss.
2) Embeddings = significado convertido en coordenadas geométricas.
3) Atención = cada token mira a todos los demás para entenderse.
4) Tokenización = la unidad real con la que opera el LLM.
+ El agente = LLM + tools + memoria + retrieval, iterando en loop.
"""
print(__doc__)
```

---

## 5) Notas finales para el instructor

**Fuentes primarias citadas en la clase (para Q&A o backup):**

- Breiman, L. (2001). *Random Forests*. **Machine Learning** 45(1):5–32. DOI: 10.1023/A:1010933404324.
- Rumelhart, D. E., Hinton, G. E., Williams, R. J. (1986). *Learning representations by back-propagating errors*. **Nature** 323:533–536. DOI: 10.1038/323533a0.
- Mikolov, T., Chen, K., Corrado, G., Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. **arXiv:1301.3781**.
- Pennington, J., Socher, R., Manning, C. D. (2014). *GloVe: Global Vectors for Word Representation*. **EMNLP 2014**, pp. 1532–1543. DOI: 10.3115/v1/D14-1162.
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., Polosukhin, I. (2017). *Attention Is All You Need*. **arXiv:1706.03762** (NeurIPS 2017).
- Devlin, J., Chang, M.-W., Lee, K., Toutanova, K. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. **arXiv:1810.04805**.
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners* (GPT-3). **arXiv:2005.14165** (NeurIPS 2020).
- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., Cao, Y. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. **arXiv:2210.03629** (ICLR 2023).
- Anthropic (dic 2024). *Building Effective Agents*. https://www.anthropic.com/engineering/building-effective-agents
- Anthropic (sep 2025). *Building agents with the Claude Agent SDK*. https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
- Anthropic (2025). *Claude Code* (product page, casos Stripe/Ramp/Wiz/Rakuten). https://www.anthropic.com/product/claude-code
- Anthropic (3 dic 2025). *Anthropic acquires Bun as Claude Code reaches $1B milestone*. https://www.anthropic.com/news/anthropic-acquires-bun-as-claude-code-reaches-usd1b-milestone
- Becker, M., Rush, N., Barnes, E., Rein, D. (jul 2025). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*. **arXiv:2507.09089** (METR).
- Veracode (2025). *2025 GenAI Code Security Report*.
- Gartner (25 jun 2025). *Gartner Predicts Over 40% of Agentic AI Projects Will Be Canceled by End of 2027* (press release, Anushree Verma).
- Google Cloud / DORA (2025). *2025 DORA State of AI-assisted Software Development*. https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/

**Documentación oficial de las librerías usadas:**

- `tiktoken`: https://github.com/openai/tiktoken — `pip install tiktoken` — encodings `cl100k_base` y `o200k_base` documentados en `tiktoken/model.py`.
- `sentence-transformers`: https://sbert.net/ — `pip install sentence-transformers` — versión 5.x al 2025-11; requiere Python ≥3.9, PyTorch ≥1.11, transformers ≥4.41. Modelo recomendado para demo: `sentence-transformers/all-MiniLM-L6-v2` (384 dim, ~80 MB, sin API, ~200M descargas/mes en Hugging Face).
- `bertviz` (opcional para attention real): https://github.com/jessevig/bertviz — `pip install bertviz`.

**Si te falla el timing:** los bloques 1.5 (Transformers) y 1.7 (Agentes) son los más comprimibles; si te quedás corto de tiempo, recortá la sección de números de impacto (METR/Veracode/Gartner/DORA) y dejá solo los enterprise wins de Anthropic.

**Si te sobra tiempo:** podés extender la demo 3 cambiando la oración para mostrar cómo cambian los patrones de atención, o agregar una demo de aritmética de embeddings (`rey - hombre + mujer ≈ reina`, aunque esto funciona mejor con word2vec/GloVe puros que con sentence-transformers).

**Errata a evitar en clase:** la cifra "2,74x más vulnerabilidades en código IA" aparece mucho en blogs pero proviene de un análisis de **CodeRabbit** sobre 470 pull requests, no de Veracode. El dato verificable de Veracode (2025 GenAI Code Security Report) es el de los **45% de elecciones inseguras** cuando el modelo tiene que elegir entre método seguro o inseguro. Citá ese.