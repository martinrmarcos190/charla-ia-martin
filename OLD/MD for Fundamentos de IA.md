# Fundamentos de IA — Material didáctico (clase presencial, 75 min)

**Audiencia:** desarrolladores MLOps "vieja escuela" (Docker, IaC, CI/CD, ML clásico). Saben qué es un modelo, un deploy, un pipeline; recién arrancan con agentes y manejan Claude Code de forma básica. Objetivo: tender el puente desde el ML que ya conocen hasta los LLMs y los agentes actuales.

**Registro:** español rioplatense, voseo, técnico pero cercano.

**Distribución temporal:** 7 bloques que suman 75 min (2 + 8 + 10 + 12 + 12 + 13 + 8 + 10).

---

## PARTE 1 — GUION DE CLASE MINUTO A MINUTO

### Bloque 0 (00:00 – 02:00) — Apertura (2 min)

**Guion hablado:**
> "Buenas, arrancamos. Esta clase es el puente. Ustedes ya saben mover modelos: los entrenan, los containerizan, los deployan, los monitorean. Lo que vamos a hacer en los próximos 75 minutos es agarrar todo eso que ya saben y usarlo como andamiaje para entender qué cambió con los LLMs y por qué hoy estamos hablando de agentes. No les voy a explicar qué es un modelo ni qué es un pipeline. Lo que sí vamos a ver es por qué el modelo dejó de ser sólo un `.pkl` que sirve predicciones, y empezó a ser una cosa que planifica, llama herramientas y abre pull requests. Vamos."

**Slide:** Título + roadmap de 7 bloques.

---

### Bloque 1 (02:00 – 10:00) — Cambio de paradigma: de reglas a patrones (8 min)

**Guion hablado:**
> "Pensemos cómo escribíamos software los últimos 40 años. Vos tenés un problema, lo descomponés en reglas, las codificás en `if/else`, las testeás. El programa hace exactamente lo que vos le dijiste. Determinista, auditable, debuggeable. Esto funciona perfecto cuando podés escribir las reglas. El tema es que hay un montón de problemas donde no sabés escribir las reglas. ¿Cómo le explicás a una computadora con `if/else` qué hace que una imagen tenga un gato? ¿Cuáles son las reglas para detectar fraude en una transacción? No sabés. Nadie sabe escribirlas a mano.

> Ahí entra el paradigma de Machine Learning. En vez de escribir las reglas, le mostrás miles o millones de ejemplos —entrada, salida deseada— y dejás que la máquina descubra las reglas sola. Vos no programás la solución; programás un procedimiento que, a partir de los datos, infiere la solución. El código que escribís es el optimizador y la arquitectura del modelo. La 'lógica de negocio' real, las reglas, terminan codificadas como números —pesos, parámetros— dentro del modelo.

> Para ustedes la analogía concreta es: en programación tradicional el código fuente es la verdad, lo compilás y obtenés un binario que ejecuta tus reglas. En ML el código fuente no contiene las reglas: contiene la receta de cómo descubrirlas. Las reglas viven en el dataset, y el 'compilador' es el proceso de entrenamiento. El artefacto compilado son los pesos. Esto es lo que vamos a desarrollar en el siguiente bloque."

**Puntos clave para slide:**
- Programación clásica: humano escribe reglas → código → ejecuta.
- ML: humano provee datos + arquitectura → entrenamiento descubre las reglas → pesos.
- El "código fuente" del comportamiento ya no es texto: son números.
- Implicancia: testing, debugging y versionado cambian radicalmente.

**Sin demo en este bloque.**

---

### Bloque 2 (10:00 – 20:00) — Modelo de ML como artefacto compilado (10 min)

**Guion hablado:**
> "Llevemos esto a su mundo. Para ustedes una imagen de Docker es un artefacto inmutable: la construís con un `Dockerfile` + contexto de build, le ponés un tag, la pushcheás a un registry, la deployás. Reproducible si fijaste bien las versiones. Bueno: un modelo entrenado es exactamente eso, pero con otros insumos.

> El Dockerfile equivale a tu código de entrenamiento: la arquitectura del modelo, los hiperparámetros, el loop de training. El contexto de build equivale al dataset. El proceso de `docker build` equivale a la corrida de entrenamiento, que en vez de minutos puede tardar días o semanas y costar millones de dólares de GPU. Y el output —la imagen taggeada, el blob inmutable que vas a servir— equivale a los pesos del modelo: un archivo binario, un tensor gigante de números de punto flotante, que es lo que efectivamente ejecuta inferencia cuando entra un request.

> ¿Por qué esta analogía les sirve? Porque les ordena mentalmente todo el lifecycle. El entrenamiento es CI: producís un artefacto. El serving es CD: corrés el artefacto en producción detrás de un endpoint. El versionado de modelos es versionado de artefactos. La reproducibilidad de un experimento es el equivalente de que tu build sea hermético: mismas versiones de librerías, mismo dataset, misma seed. El A/B testing entre modelos es shadow traffic entre dos imágenes. Todo lo que ustedes saben de MLOps tradicional se mapea uno a uno.

> El quiebre que viene después es que los LLMs son artefactos como cualquier otro modelo —son pesos, son tensores, los servís detrás de un endpoint—, pero el artefacto pesa cientos de gigabytes y costó del orden de cien millones de dólares entrenarlo: el propio Sam Altman confirmó que GPT-4 costó 'más de cien millones de dólares', y el AI Index Report 2025 de Epoch AI estima el compute de GPT-4 en aproximadamente 79 millones de dólares. Nadie en su sano juicio lo va a re-entrenar desde cero. Lo que vas a hacer es consumirlo como dependencia: o vía API, o lo bajás de Hugging Face y lo servís vos. Pero el ciclo de 'yo entreno mi modelo' deja de aplicar para la mayoría de los casos. Se parece más a 'bajar Postgres' que a 'compilar tu app'."

**Puntos clave para slide:**
- Dockerfile ≈ código de entrenamiento + arquitectura
- Contexto de build ≈ dataset
- `docker build` ≈ training run (días/semanas, decenas a cientos de millones de USD en cómputo para frontier)
- Imagen taggeada ≈ pesos del modelo (artefacto inmutable)
- `docker run` ≈ inferencia / serving
- Cambio con LLMs: el artefacto es "infraestructura externa", no algo que vos compilás.

**Sin demo en este bloque.**

---

### Bloque 3 (20:00 – 32:00) — Redes neuronales y backpropagation, intuitivo (12 min)

**Guion hablado:**
> "Una red neuronal, en el fondo, es una función matemática gigante con un montón de perillas regulables. Ponéle: una caja con miles de millones de potenciómetros. Vos le metés una entrada —un vector de números— y sale otro vector. El valor de cada perilla determina cuánto contribuye cada conexión interna. Si las perillas están en una configuración random, la salida es basura. Si están en la configuración correcta, la salida es la predicción que querés.

> La pregunta es: ¿cómo encontrás la configuración correcta de miles de millones de perillas? Acá entra backpropagation, que es la idea clave de 1986 —Rumelhart, Hinton, Williams, paper 'Learning representations by back-propagating errors', publicado en *Nature*, volumen 323, páginas 533-536. La idea, contada simple:
>
> 1. Le pasás un ejemplo a la red con las perillas como están.
> 2. La red predice algo. Comparás con la respuesta correcta y calculás un error (la 'loss').
> 3. Acá viene la magia: usando regla de la cadena del cálculo diferencial, podés calcular, para cada perilla, en qué dirección moverla para que el error baje un poquito. Eso es el gradiente.
> 4. Movés todas las perillas un pasito en esa dirección. Le llaman 'descenso por gradiente'.
> 5. Repetís con el siguiente ejemplo. Y otro. Y otro. Miles de millones de veces.

> Lo que dice textual el abstract del paper de Rumelhart es: 'el procedimiento ajusta repetidamente los pesos de las conexiones de la red para minimizar una medida de la diferencia entre el vector de salida real y el deseado'. Cuarenta años después seguimos haciendo lo mismo.

> Lo loco es que esto funciona. No tenés que entender qué representa cada perilla. La red 'aprende' representaciones internas útiles por sí sola. Y a medida que escalás la cantidad de perillas y la cantidad de datos, las cosas que la red puede aprender se vuelven sorprendentemente complejas.

> Para ustedes la analogía DevOps es: imaginate que tu CI corre una suite de tests gigante, mide el error agregado, y un sistema automático va ajustando flags de configuración de tu app para minimizar ese error. No estás programando, estás dejando que el sistema se auto-tunee. Backprop es eso, pero con cálculo diferencial en lugar de búsqueda heurística, lo cual lo hace mucho más eficiente.

> [DEMO en vivo: `gradient_descent.py` — ver apéndice] Acá lo vemos en 2D. Tengo una función cuadrática con un mínimo, y voy a soltar una pelotita en un punto random, calcular el gradiente, y moverla un pasito en la dirección opuesta. Miren la trayectoria: converge al mínimo. Esto, en miles de millones de dimensiones, es entrenar una red neuronal."

**Puntos clave para slide:**
- Red neuronal = función matemática con N parámetros ajustables ("perillas").
- Frontier hoy: 10⁹ – 10¹² parámetros.
- Backpropagation (Rumelhart, Hinton & Williams, *Nature* 323:533-536, 1986).
- Descenso por gradiente: mover cada parámetro un pasito en la dirección que reduce el error.
- Repetir millones de veces con millones de ejemplos.

**Demo:** `gradient_descent.py` (apéndice).

---

### Bloque 4 (32:00 – 44:00) — Embeddings: coordenadas GPS del significado (12 min)

**Guion hablado:**
> "Ok, las redes operan con números. Pero el texto no es número. ¿Cómo le metés 'gato' a una red? La idea, que se llama embedding, es asignarle a cada palabra —o más en general, a cada pedazo de texto— un vector de cientos de números. Coordenadas en un espacio de alta dimensión.

> La gracia, y esto es lo que tienen que llevarse del bloque, es que estas coordenadas se aprenden de tal forma que la cercanía geométrica equivale a similitud de significado. 'Gato' y 'perro' caen cerca. 'Gato' y 'factura' caen lejos. Y aún más loco: hay relaciones algebraicas. El ejemplo famoso de Mikolov en 2013: `vector('rey') - vector('hombre') + vector('mujer') ≈ vector('reina')`. La geometría del espacio captura semántica.

> Los papers fundacionales son dos. Primero Word2Vec —Mikolov, Sutskever, Chen, Corrado y Dean, 'Distributed Representations of Words and Phrases and their Compositionality', NeurIPS 2013— precedido por 'Efficient Estimation of Word Representations in Vector Space' (arXiv:1301.3781, enero 2013). Y después GloVe —Pennington, Socher, Manning, EMNLP 2014, Doha. Eso fue la primera ola: embeddings estáticos, una palabra = un vector fijo. Hoy con los Transformers tenemos embeddings contextuales: la misma palabra en distintos contextos tiene distintas coordenadas, lo cual resuelve el problema de la polisemia ('banco' como asiento vs 'banco' como institución).

> Analogía DevOps: pensá los embeddings como un hash semántico. Un hash criptográfico te garantiza que strings parecidos den hashes totalmente distintos —es lo que querés para integridad. Un embedding te garantiza lo contrario: strings semánticamente parecidos dan vectores parecidos. Es el primitivo de búsqueda semántica, de RAG, de deduplicación inteligente, de clustering. Todo el tooling moderno de 'vector database' —Pinecone, Weaviate, pgvector, Milvus, Qdrant— existe porque embeddings son la representación que el LLM entiende, y necesitás poder indexar y buscar por similitud coseno a escala.

> [DEMO en vivo: `embeddings_similarity.py` — ver apéndice] Acá uso `sentence-transformers` con un modelo chiquito que corre en CPU, `all-MiniLM-L6-v2`. Es de 22 MB, produce embeddings de 384 dimensiones. Convierto tres frases en vectores, y mido similitud coseno entre pares. Van a ver que 'el perro corre por el parque' y 'el gato duerme en el sillón' dan score alto entre sí —son frases de mascotas—, mientras que cualquiera de las dos contra 'factura electrónica AFIP' da score bajo. La geometría refleja el significado."

**Puntos clave para slide:**
- Embedding: texto → vector de N dimensiones (típicamente 384, 768, 1536, 3072).
- Propiedad clave: cercanía en el espacio ≈ similitud semántica.
- Word2Vec (Mikolov et al., NeurIPS 2013, arXiv:1301.3781); GloVe (Pennington et al., EMNLP 2014).
- Embeddings contextuales (vienen de los Transformers) resuelven polisemia.
- Habilita: búsqueda semántica, RAG, clustering, dedup, recomendación.
- Stack típico: modelo de embeddings + vector DB.

**Demo:** `embeddings_similarity.py` (apéndice).

---

### Bloque 5 (44:00 – 57:00) — Transformers y atención (13 min)

**Guion hablado:**
> "Llegamos al hito de 2017. Hasta ese momento, para procesar secuencias —texto, audio, lo que sea— se usaban RNNs y LSTMs: arquitecturas que leen token por token, manteniendo un 'estado oculto' que se actualiza con cada nuevo input. Funcionaban, pero tenían dos problemas grandes: uno, son inherentemente secuenciales —no podés paralelizar el procesamiento de una secuencia—; dos, se olvidan de tokens lejanos, el famoso problema de las dependencias largas.

> En junio de 2017, ocho autores de Google publican 'Attention Is All You Need' —Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin— en NeurIPS, arXiv:1706.03762. La propuesta, en sus propias palabras: 'una nueva arquitectura de red simple, el Transformer, basada únicamente en mecanismos de atención, prescindiendo enteramente de recurrencia y convoluciones'. El modelo original tenía 100M de parámetros y batió el estado del arte de traducción inglés-francés con 41.8 BLEU entrenando 3.5 días en ocho GPUs. Lo notable no es el resultado: es la receta.

> La idea central, en una línea: cada palabra en una secuencia puede 'mirar' simultáneamente a todas las demás palabras, y decidir a cuáles prestarles atención y cuánto.

> Concretamente: para cada token se calculan tres vectores —query, key, value—. Pensálo como un sistema de búsqueda interno. El query del token 'la' pregunta 'qué información necesito de los demás tokens'. Los keys de los demás tokens dicen 'esto es lo que yo ofrezco'. Hacés el producto punto entre query y todos los keys —similitud—, normalizás con softmax, y eso te da los pesos con los que combinás los values. El resultado: una nueva representación del token 'la' que ya incorpora contexto de toda la oración. Hacés esto en paralelo para todos los tokens, en múltiples 'cabezas' que aprenden a mirar distintas relaciones —sintáctica, semántica, posicional—, y lo apilás en muchas capas. Eso es un Transformer.

> ¿Por qué fue la revolución? Por dos razones que a ustedes les van a sonar muy familiares: paralelización y escalabilidad. RNN: secuencial, no aprovechás bien la GPU. Transformer: todas las posiciones se procesan en paralelo en un solo matmul gigante. GPU happy. Y al ser paralelizable, podés entrenar modelos mucho más grandes en mucho menos tiempo. Sin Transformers no había GPT.

> Una cosa más antes de la demo: dependencias largas. En un Transformer, el token 1 puede atender directamente al token 1000 en una sola operación. En una RNN, esa información tenía que sobrevivir 999 pasos de actualización del estado oculto, y mucho se perdía en el camino. La atención resuelve eso de cuajo.

> [DEMO en vivo 1: `tokenization.py`] Antes de meternos con atención, miremos cómo el texto entra al modelo. Acá tomo una frase en castellano y la paso por `tiktoken`, el tokenizador BPE oficial de OpenAI. Van a ver que no es 'una palabra = un token'. Palabras comunes son un token; palabras raras o en otros idiomas se parten en subwords. Esto importa para costos —cobran por token—, para context windows —están medidos en tokens—, y para entender por qué a veces el modelo se confunde con palabras inusuales.

> [DEMO en vivo 2: `attention_viz.py`] Y acá una matriz de atención simulada sobre una frase corta. Cada celda muestra cuánto un token mira a otro. Van a ver patrones: los pronombres miran al sustantivo al que se refieren, los verbos miran al sujeto. No es magia: emerge del entrenamiento."

**Puntos clave para slide:**
- 2017: "Attention Is All You Need" (Vaswani et al., NeurIPS, arXiv:1706.03762).
- Reemplaza recurrencia/convolución por self-attention pura.
- Self-attention: cada token computa query/key/value y "atiende" a todos los demás simultáneamente.
- Ventajas vs RNN: paralelizable en GPU + maneja dependencias largas en O(1) hops.
- Multi-head attention: varias atenciones en paralelo capturan distintas relaciones.
- Es la base arquitectónica de TODO el deep learning moderno de lenguaje (y de mucho más allá del lenguaje).

**Demos:** `tokenization.py` y `attention_viz.py` (apéndice).

---

### Bloque 6 (57:00 – 65:00) — De Transformers a LLMs (8 min)

**Guion hablado:**
> "Receta para hacer un LLM, simple: tomá un Transformer decoder, escalalo a miles de millones de parámetros, entrenalo a predecir el siguiente token sobre, básicamente, todo el internet. Eso es todo. No hay magia adicional en la receta base. La magia está en la escala.

> Cronología rápida. GPT-1 en 2018, 117M de parámetros. BERT en octubre 2018 (Devlin et al., arXiv:1810.04805), BERT-Large 340M. GPT-2 anunciado el 14 de febrero de 2019 con 1.5B de parámetros, aunque OpenAI hizo un 'staged release' por riesgos de uso malicioso y recién liberó el modelo completo de 1.5B en noviembre. GPT-3 en mayo 2020 (arXiv:2005.14165, 28 de mayo): el paper de Brown et al., 'Language Models are Few-Shot Learners'. Cito textual el abstract: 'entrenamos GPT-3, un modelo de lenguaje autorregresivo con 175 mil millones de parámetros, 10x más que cualquier modelo de lenguaje no-sparse previo'. Es el primer momento en que el mundo ve que escalar produce capacidades emergentes que no estaban en modelos más chicos: few-shot learning, razonamiento básico, traducción sin entrenamiento explícito.

> En 2020 sale otro paper crítico: 'Scaling Laws for Neural Language Models' —Kaplan et al., arXiv:2001.08361, enero 2020. Demuestran empíricamente que la loss del modelo escala como ley de potencia con tres variables: cantidad de parámetros, cantidad de datos, cantidad de cómputo. No es magia: si tirás más de los tres, mejora predeciblemente. El paper lo dice así: 'la loss escala como ley de potencia con el tamaño del modelo, el tamaño del dataset y la cantidad de cómputo usado en entrenamiento, con algunas tendencias que abarcan más de siete órdenes de magnitud'. Eso convirtió el problema de 'cómo hacemos un mejor modelo' en un problema de 'cuánta plata tenés y cómo la asignás'.

> Después en marzo 2022, DeepMind publica Chinchilla —Hoffmann et al., 'Training Compute-Optimal Large Language Models', arXiv:2203.15556. Corrige a Kaplan: muestra que los modelos previos estaban subentrenados, y que para un budget de cómputo fijo el óptimo es escalar parámetros y datos en proporción aproximada 20 tokens por parámetro. Entrenaron un modelo de 70B parámetros sobre 1.4 billones de tokens (mismo cómputo que Gopher de 280B) y le ganó en todos los benchmarks. Eso explica por qué Llama, Mistral, los modelos open source modernos, entrenan modelos más chicos en muchísimos más datos. Llama 3.1 405B, por ejemplo, fue entrenado por Meta sobre más de 15 billones de tokens en 16 mil GPUs H100.

> Y de ahí en adelante es escala, datos curados, y técnicas de alineamiento: RLHF, instruction tuning, constitutional AI. ChatGPT, lanzado el 30 de noviembre de 2022 basado en GPT-3.5, es el momento donde esto se vuelve producto masivo. GPT-4 el 14 de marzo de 2023. Y hoy, junio de 2026, los modelos frontier —Claude Opus 4.8, GPT-5.1-Codex-Max, Gemini 3 Pro— tienen context windows de cientos de miles a un millón de tokens, capacidades multimodales nativas, y razonamiento extendido. Pero la arquitectura base sigue siendo, en lo esencial, el Transformer de 2017.

> Para que cierre la analogía DevOps: un LLM moderno es como un sistema operativo. Es infraestructura. Lo construye un puñado de organizaciones con capacidad para gastar cientos de millones en cómputo. Vos lo consumís. Lo configurás con prompts, system messages, herramientas, contexto. No lo recompilás."

**Puntos clave para slide:**
- Receta: Transformer decoder + escala de parámetros + corpus masivo + pre-entrenamiento autoregresivo.
- Hitos verificados: GPT-3 (175B, mayo 2020); ChatGPT (30 nov 2022, basado en GPT-3.5); GPT-4 (14 mar 2023); Claude Opus 4.8 (mayo 2026); GPT-5.1, Gemini 3 Pro (2025-2026).
- Scaling laws (Kaplan et al. 2020): loss escala como ley de potencia en params, datos y cómputo.
- Chinchilla (Hoffmann et al. 2022): el óptimo compute-optimal es ~20 tokens por parámetro (Chinchilla 70B sobre 1.4T tokens superó a Gopher 280B).
- Capacidades emergentes a escala: few-shot learning, razonamiento, instruction-following.
- Post-training: RLHF, instruction tuning, alineamiento.

**Sin demo (la demo de tokenización del bloque anterior alcanza para conectar).**

---

### Bloque 7 (65:00 – 75:00) — Agentes: de predecir texto a actuar (10 min)

**Guion hablado:**
> "Llegamos al presente. Un LLM puro es una función `texto → texto`. Vos le mandás un prompt, te devuelve tokens. Útil, pero limitado: no puede correr código, no puede leer tu base de datos, no puede abrir un PR, no puede iterar si se equivoca.

> Un agente es un patrón arquitectónico que pone un LLM en un loop con herramientas y un objetivo. El paper canónico es ReAct —Yao, Zhao, Yu, Du, Shafran, Narasimhan y Cao, 'ReAct: Synergizing Reasoning and Acting in Language Models', arXiv:2210.03629, publicado en ICLR 2023. La idea es alternar pasos de razonamiento ('thought') con pasos de acción ('action') y observación ('observation') del resultado. El abstract lo describe así: 'los rastros de razonamiento ayudan al modelo a inducir, rastrear y actualizar planes de acción, así como manejar excepciones, mientras que las acciones le permiten interactuar con fuentes externas para reunir información adicional'. Loop: pensar, decidir qué herramienta usar, ejecutarla, observar el output, volver a pensar. Repetir hasta resolver la tarea.

> Toolformer —Schick, Dwivedi-Yu, Dessì, Raileanu, Lomeli, Zettlemoyer, Cancedda, Scialom; arXiv:2302.04761, presentado oralmente en NeurIPS 2023— mostró que los modelos pueden aprender a llamar APIs por sí solos, de forma self-supervised. Después vino el patrón de tool use vía function calling, que hoy es estándar en todos los APIs de modelos.

> Y el 25 de noviembre de 2024, Anthropic publicó el Model Context Protocol —MCP—, un estándar abierto creado por David Soria Parra y Justin Spahr-Summers para que cualquier LLM pueda conectarse a cualquier fuente de datos o herramienta a través de una interfaz uniforme. Lo describen como 'un puerto USB-C para AI'. El 9 de diciembre de 2025, Anthropic donó MCP al Linux Foundation bajo la nueva Agentic AI Foundation, con co-fundadores Anthropic, Block y OpenAI, y miembros platino que incluyen AWS, Bloomberg, Cloudflare, Google y Microsoft. Para esa fecha el ecosistema ya tenía más de 97 millones de descargas mensuales de SDKs y más de 10.000 servidores MCP públicos activos, integrados nativamente por ChatGPT, Cursor, Gemini, Microsoft Copilot y VS Code. Es el primer estándar real de interoperabilidad en este espacio.

> En diciembre 2024 Anthropic también publicó 'Building Effective Agents'. La definición operativa que dan es la más limpia que circula: distinguen workflows —donde los LLMs y las herramientas se orquestan a través de caminos predefinidos en código— de agents —donde el LLM 'dirige dinámicamente sus propios procesos y uso de herramientas, manteniendo control sobre cómo cumple las tareas'. Es un gradiente de autonomía. Y la recomendación que dan, que vale repetir, es: empezá simple. La mayoría de los problemas se resuelven con un workflow de prompt chaining, routing o parallelization, no necesitás un agente completo.

> ¿Por qué impacta tanto al desarrollo de software? Porque el desarrollo de software es el dominio ideal para agentes: el feedback es objetivo (los tests pasan o no), el espacio está bien definido (un repo), y la calidad es medible. Por eso explotaron los coding agents. Claude Code de Anthropic (en general availability desde el 22 de mayo de 2025), Devin de Cognition (anunciado el 12 de marzo de 2024), Cursor (de Anysphere, lanzado en marzo 2023), Aider, Codex CLI de OpenAI.

> El benchmark estándar es SWE-bench Verified: 500 issues reales de GitHub curados por humanos en colaboración con OpenAI. En el paper original de SWE-bench (Jimenez et al., octubre 2023) el mejor modelo, Claude 2 con retrieval BM25, resolvía apenas el 1.96%. Devin en marzo 2024 saltó a 13.86%. Hoy, junio de 2026, Claude Opus 4.5 fue el primer modelo en superar el 80% (80.9%) en noviembre 2025, y Claude Mythos Preview lidera el leaderboard con 93.9%. De 2% a 94% en dos años y medio. Es un salto vertical.

> El cambio práctico para ustedes: el agente no completa autocomplete, encara una tarea entera. Le decís 'arreglá este bug', lee el repo, planifica, edita varios archivos, corre los tests, ve que fallan, ajusta, vuelve a correr, abre el PR. Ustedes pasan de escribir línea por línea a revisar diffs y dirigir a varios agentes en paralelo.

> Esto no quiere decir que el rol de ustedes desaparece. Quiere decir que se mueve hacia arriba en el stack. Los agentes necesitan infra: sandboxing, observabilidad, control de permisos, gates de seguridad, evaluación continua. Necesitan CI/CD para sus propios prompts y herramientas. Necesitan rate limiting y cost management de tokens. Necesitan IaC para definir qué herramientas tiene disponible cada agente. Todo lo que ustedes saben de MLOps clásico se vuelve a aplicar, pero con un actor nuevo —el agente— que es no determinista y que actúa. El próximo módulo del curso lo dedicamos a esto."

**Puntos clave para slide:**
- LLM puro: `texto → texto`. Agente: LLM en loop con herramientas y objetivo.
- ReAct (Yao et al., arXiv:2210.03629, ICLR 2023): patrón Thought-Action-Observation.
- Toolformer (Schick et al., NeurIPS 2023 oral): modelos que aprenden a invocar APIs.
- Model Context Protocol (Anthropic, 25-nov-2024 → Linux Foundation, 9-dic-2025): estándar abierto adoptado por OpenAI, Microsoft, Google, AWS.
- Anthropic "Building Effective Agents" (dic 2024): workflows vs agents, recomendación de empezar simple.
- Coding agents: Claude Code (GA 22-may-2025), Devin (12-mar-2024), Cursor (mar 2023), Codex CLI, Aider.
- SWE-bench Verified: 1.96% (Claude 2, oct 2023) → 13.86% (Devin, mar 2024) → 80.9% (Claude Opus 4.5, nov 2025) → 93.9% (Claude Mythos Preview, jun 2026).
- El rol MLOps se traslada hacia arriba: sandboxing, observabilidad, cost mgmt, IaC para tools.

**Cierre (74:00 – 75:00):**
> "Resumen: pasamos de escribir reglas a entrenar modelos. Los modelos son artefactos compilados desde datos. Las redes neuronales son funciones gigantes con perillas que se ajustan por backprop. Los embeddings convierten texto en geometría. Los Transformers paralelizaron eso y desbloquearon la escala. Los LLMs son Transformers a escala extrema entrenados con todo internet. Y los agentes son LLMs en loop con herramientas. Próxima clase: cómo se construyen agentes en serio. Gracias."

---

## PARTE 2 — ESQUEMA DE SLIDES

**Slide 1 — Portada**
- Fundamentos de IA
- Curso de IA Aplicada — Módulo 1
- Audiencia: MLOps / Plataforma

**Slide 2 — Roadmap**
- 1. Cambio de paradigma (8')
- 2. Modelo = artefacto compilado (10')
- 3. Redes y backprop (12')
- 4. Embeddings (12')
- 5. Transformers y atención (13')
- 6. De Transformers a LLMs (8')
- 7. Agentes (10')

**Slide 3 — Programación clásica vs ML**
- Clásica: humano escribe reglas → código → ejecuta
- ML: humano provee datos + arquitectura → entrenamiento descubre reglas → pesos
- El "código fuente" del comportamiento son números, no texto

**Slide 4 — Implicancias del cambio**
- Testing: no podés cubrir con unit tests
- Debugging: el bug puede estar en los datos
- Versionado: del código + de los datos + de los pesos
- Reproducibilidad ≠ determinismo

**Slide 5 — Modelo como imagen de Docker**
- Dockerfile ≈ código de entrenamiento + arquitectura
- Contexto de build ≈ dataset
- `docker build` ≈ training run
- Imagen taggeada ≈ pesos del modelo
- `docker run` ≈ inferencia

**Slide 6 — LLM = artefacto que NO compilás**
- Cientos de GB de pesos
- Costo de entrenamiento: ~$79M-$100M+ (caso GPT-4 según Epoch AI / Sam Altman)
- Lo consumís como dependencia (API o weights de Hugging Face)
- Más parecido a "bajar Postgres" que a "compilar tu app"

**Slide 7 — Red neuronal = perillas**
- Función matemática gigante con N parámetros ajustables
- Frontier hoy: 10⁹ – 10¹² parámetros
- Una perilla por conexión

**Slide 8 — Backpropagation**
- Rumelhart, Hinton & Williams — *Nature* 323:533-536, 1986
- Loop: predecir → calcular error → calcular gradiente → ajustar perillas
- Repetir millones de veces

**Slide 9 — Descenso por gradiente (visual)**
- Demo en vivo: pelotita bajando una cuadrática
- Mismo principio, en miles de millones de dimensiones

**Slide 10 — Embeddings: GPS del significado**
- Texto → vector de 384/768/1536/3072 dimensiones
- Cercanía geométrica = similitud semántica
- `rey - hombre + mujer ≈ reina`

**Slide 11 — Papers fundacionales de embeddings**
- Word2Vec — Mikolov et al., arXiv:1301.3781 (ene 2013) y NeurIPS 2013
- GloVe — Pennington, Socher, Manning, EMNLP 2014
- Embeddings contextuales: vienen de los Transformers

**Slide 12 — Embeddings: stack moderno**
- Modelo de embeddings (text-embedding-3, all-MiniLM-L6-v2, etc.)
- Vector DB (pgvector, Pinecone, Weaviate, Milvus, Qdrant)
- Habilita: RAG, búsqueda semántica, dedup, recomendación

**Slide 13 — 2017: Attention Is All You Need**
- Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin
- NeurIPS 2017 — arXiv:1706.03762
- Tira RNN/CNN, deja sólo atención
- Modelo original: 100M params, 41.8 BLEU en EN-FR en 3.5 días con 8 GPUs

**Slide 14 — Self-attention en una línea**
- Cada token mira simultáneamente a todos los demás
- Query / Key / Value
- Multi-head: varias atenciones en paralelo

**Slide 15 — Por qué fue la revolución**
- Paralelizable en GPU → entrenás modelos mucho más grandes mucho más rápido
- Dependencias largas en O(1) hops (vs O(N) en RNN)
- Sin Transformers no había GPT

**Slide 16 — Tokenización**
- Texto → IDs numéricos (no es 1 palabra = 1 token)
- BPE / tiktoken (`o200k_base` para GPT-4o+)
- Costos y context windows se miden en tokens

**Slide 17 — De Transformers a LLMs**
- Receta: decoder Transformer + escala + corpus masivo + autoregresivo
- GPT-3 (175B, may 2020): primer momento de capacidades emergentes
- ChatGPT (30 nov 2022): producto masivo
- GPT-4 (14 mar 2023), Claude Opus 4.8, GPT-5.1, Gemini 3 Pro (2025-2026)

**Slide 18 — Scaling laws**
- Kaplan et al. 2020 (arXiv:2001.08361): loss ~ ley de potencia en params, datos, cómputo
- Chinchilla (Hoffmann et al. 2022, arXiv:2203.15556): ~20 tokens por parámetro es compute-optimal
- Implicancia: el problema se vuelve presupuestario

**Slide 19 — LLM = sistema operativo / infraestructura**
- Lo construyen 5-10 organizaciones en el mundo
- Vos lo consumís
- Lo configurás con prompts, system messages, herramientas, contexto

**Slide 20 — De LLM a agente**
- LLM puro: `texto → texto`
- Agente: LLM en loop con herramientas y objetivo
- Puede planificar, ejecutar, observar, iterar

**Slide 21 — Patrones canónicos**
- ReAct (Yao et al. 2022, ICLR 2023): Thought-Action-Observation
- Toolformer (Schick et al. NeurIPS 2023, oral): tool use aprendido self-supervised
- Function calling: estándar en APIs de modelo

**Slide 22 — Model Context Protocol (MCP)**
- Anthropic, 25 noviembre 2024 (David Soria Parra & Justin Spahr-Summers)
- "USB-C para AI"
- Donado al Linux Foundation / Agentic AI Foundation (9-dic-2025)
- Co-fundadores AAIF: Anthropic, Block, OpenAI. Platinum: AWS, Bloomberg, Cloudflare, Google, Microsoft
- 97M+ descargas mensuales de SDKs, 10.000+ servidores activos

**Slide 23 — Anthropic: Building Effective Agents (19-dic-2024)**
- Workflows: caminos predefinidos en código
- Agents: el LLM dirige dinámicamente su proceso
- Recomendación: empezá simple, sólo escalá complejidad cuando hace falta

**Slide 24 — Coding agents: el dominio que explotó**
- Por qué: feedback objetivo (tests), espacio bien definido, calidad medible
- Claude Code (GA 22-may-2025), Devin (12-mar-2024), Cursor (mar 2023), Codex CLI, Aider
- SWE-bench Verified: 1.96% Claude 2 (oct 2023) → 13.86% Devin → 80.9% Opus 4.5 (nov 2025) → 93.9% Claude Mythos Preview (jun 2026)

**Slide 25 — Línea de tiempo ancla (verificada)**
- 1986: Backpropagation — Rumelhart, Hinton, Williams (*Nature* 323:533-536)
- 2012: AlexNet rompe ImageNet (NeurIPS 2012)
- ene 2013: Word2Vec (arXiv:1301.3781, Mikolov et al.)
- 2014: GloVe (EMNLP)
- jun 2017: Transformer (arXiv:1706.03762)
- oct 2018: BERT (arXiv:1810.04805, 340M)
- feb 2019: GPT-2 (1.5B, staged release hasta nov 2019)
- may 2020: GPT-3 (arXiv:2005.14165, 175B) / Scaling Laws (Kaplan)
- mar 2022: Chinchilla (Hoffmann et al.)
- oct 2022: ReAct (arXiv:2210.03629)
- 30 nov 2022: ChatGPT
- 14 mar 2023: GPT-4
- feb 2023: Toolformer (arXiv:2302.04761)
- 12 mar 2024: Devin (Cognition)
- 25 nov 2024: MCP (Anthropic)
- 19 dic 2024: "Building Effective Agents" (Anthropic)
- 22 may 2025: Claude Code GA
- nov 2025: Claude Opus 4.5, primer modelo >80% en SWE-bench Verified
- 9 dic 2025: MCP donado al Linux Foundation
- jun 2026: estado del arte de coding agents ~94% SWE-bench Verified

**Slide 26 — Qué cambia para MLOps**
- El "modelo" deja de ser algo que vos compilás
- El "deploy" incluye tools, permisos, sandboxing
- El "monitoreo" incluye evals, traces, cost por request
- IaC para definir herramientas y permisos de agentes
- CI/CD para prompts y agent configs
- Próximo módulo: agentes en serio

**Slide 27 — Cierre**
- Reglas → datos → patrones
- Pesos → embeddings → atención → escala → agentes
- Las habilidades de plataforma valen más que nunca

---

## PARTE 3 — APÉNDICE DE EJEMPLOS PRÁCTICOS

Todos los ejemplos se corren **en local**, sin claves de API, con dependencias mínimas. Probados con Python 3.11+.

**Setup único (en una venv limpia):**
```bash
python -m venv .venv && source .venv/bin/activate
pip install tiktoken sentence-transformers matplotlib numpy
```

> Nota: la primera vez que se corre `embeddings_similarity.py`, `sentence-transformers` baja el modelo (~80 MB). Conviene correrlo una vez antes de la clase para que el cacheo no rompa el flujo.

---

### Demo 1 — `gradient_descent.py` (Bloque 3, ~3 min)

**Qué mostrar en pantalla:** dos paneles de matplotlib. A la izquierda la función cuadrática con la trayectoria de la pelotita marcada con puntos rojos descendiendo al mínimo. A la derecha, la loss vs iteración.

**Qué decir mientras corre:**
> "Mirá: arranca lejos del mínimo. En cada paso calculo el gradiente —que es simplemente la derivada en ese punto— y muevo `x` en la dirección opuesta, multiplicado por un learning rate. La pelotita baja, la loss baja. Esto es backprop conceptualmente. En una red real esto pasa en miles de millones de dimensiones simultáneamente, pero la idea es exactamente la misma."

```python
# gradient_descent.py
# Demo: descenso por gradiente sobre f(x) = (x - 3)^2 + 2.
# Muestra cómo "ajustar una perilla" para minimizar el error.

import numpy as np
import matplotlib.pyplot as plt

# Función a minimizar: una cuadrática con mínimo en x=3, f=2.
def f(x):
    return (x - 3) ** 2 + 2

# Gradiente analítico: f'(x) = 2(x - 3).
def grad(x):
    return 2 * (x - 3)

# Hiperparámetros.
x = -4.0          # arrancamos lejos del mínimo
lr = 0.1          # learning rate (tamaño del pasito)
steps = 30        # cuántas iteraciones

# Historial para graficar.
xs, ys = [x], [f(x)]
for _ in range(steps):
    x = x - lr * grad(x)   # paso de descenso por gradiente
    xs.append(x)
    ys.append(f(x))

# Visualización.
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Panel 1: la función y la trayectoria de la pelotita.
xx = np.linspace(-5, 8, 200)
ax1.plot(xx, f(xx), label="f(x) = (x-3)^2 + 2")
ax1.scatter(xs, ys, c="red", s=30, label="trayectoria")
ax1.set_title("Descenso por gradiente sobre f(x)")
ax1.set_xlabel("x (la 'perilla')"); ax1.set_ylabel("loss")
ax1.legend()

# Panel 2: la loss a lo largo de las iteraciones.
ax2.plot(ys, marker="o")
ax2.set_title("Loss vs iteración")
ax2.set_xlabel("iteración"); ax2.set_ylabel("loss")

plt.tight_layout()
plt.show()
```

---

### Demo 2 — `tokenization.py` (Bloque 5, ~2 min)

**Qué mostrar en pantalla:** consola con el output. Cada frase con su lista de tokens y la cantidad. Idealmente con la frase en castellano que muestra cómo se fragmenta en subwords más que la en inglés.

**Qué decir mientras corre:**
> "Miren. La frase en inglés `'Hello, world!'` se parte en pocos tokens limpitos. La frase en castellano `'Hola, mundo, ¿cómo andás?'` se parte en más tokens porque el vocabulario fue entrenado dominantemente con inglés. La palabra `andás`, que el tokenizador nunca vio mucho, se rompe en pedacitos. Esto importa porque el LLM cobra por token y mide su context window en tokens. Si trabajan en español pagan más por la misma información que en inglés."

```python
# tokenization.py
# Demo: cómo tiktoken (el tokenizador BPE oficial de OpenAI) parte texto.
# Documentación: https://github.com/openai/tiktoken

import tiktoken

# Encoding o200k_base es el usado por GPT-4o y modelos posteriores.
enc = tiktoken.get_encoding("o200k_base")

ejemplos = [
    "Hello, world!",
    "Hola, mundo, ¿cómo andás?",
    "MLOps developers love Docker images.",
    "Los desarrolladores MLOps aman las imágenes de Docker.",
]

for texto in ejemplos:
    ids = enc.encode(texto)
    # decode_single_token_bytes devuelve los bytes de cada token.
    pieces = [enc.decode_single_token_bytes(t).decode("utf-8", errors="replace")
              for t in ids]
    print(f"\nTexto:   {texto!r}")
    print(f"Tokens:  {pieces}")
    print(f"IDs:     {ids}")
    print(f"Total:   {len(ids)} tokens")
```

---

### Demo 3 — `embeddings_similarity.py` (Bloque 4, ~3 min)

**Qué mostrar en pantalla:** la matriz de similitud impresa en consola.

**Qué decir mientras corre:**
> "Tres frases. Dos son sobre mascotas, una es burocracia AFIP. Después de pasarlas por el modelo, cada una es un vector de 384 dimensiones. Calculo coseno entre todos los pares. Miren la matriz: las dos de mascotas tienen score alto entre sí. Cada una contra la de AFIP está muy bajo. La geometría refleja el significado. Esto es lo que hace funcionar a RAG: convertís tu query y tus docs en vectores, y traés los más cercanos."

```python
# embeddings_similarity.py
# Demo: convertir frases en vectores y medir similitud coseno.
# Modelo: sentence-transformers/all-MiniLM-L6-v2 (~80 MB, corre en CPU,
# embeddings de 384 dimensiones).
# Docs: https://www.sbert.net/

from sentence_transformers import SentenceTransformer
import numpy as np

# La primera ejecución descarga el modelo y lo cachea en ~/.cache/.
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

frases = [
    "El perro corre por el parque.",
    "El gato duerme en el sillón.",
    "Factura electrónica AFIP comprobante tipo A.",
]

# encode() devuelve un array (N, 384). Normalizamos para que el producto
# punto = similitud coseno directamente.
emb = model.encode(frases, normalize_embeddings=True)
print("Shape del embedding:", emb.shape)

# Similitud coseno como producto punto entre vectores normalizados.
sim = emb @ emb.T

print("\nMatriz de similitud coseno:")
header = " | ".join(f"frase {i}" for i in range(len(frases)))
print(f"{'':40}{header}")
for i, f in enumerate(frases):
    fila = "  ".join(f"{x:+.3f}" for x in sim[i])
    print(f"frase {i}: {f[:38]:38}  {fila}")

# Lectura esperada: los pares de mascotas (0,1) dan score alto;
# cualquiera vs AFIP (2) da score bajo. La geometría = el significado.
```

---

### Demo 4 — `attention_viz.py` (Bloque 5, ~3 min)

**Qué mostrar en pantalla:** un heatmap con los tokens de la frase en ambos ejes y celdas más oscuras donde la atención es más fuerte.

**Qué decir mientras corre:**
> "Esta es una matriz de atención simulada —no la de un modelo real, sino una que armé para ilustrar el patrón. Cada fila es un token preguntando 'a quién miro'. Cada columna es un token siendo mirado. Las celdas más claras son atención fuerte. Fíjense: el verbo 'ajusta' atiende al sujeto 'modelo'; los tokens 'función', 'loss' y 'gradiente' se miran mutuamente porque conceptualmente van juntos. En un Transformer real esto emerge solo del entrenamiento, sin que nadie le diga. Y hay muchas capas y muchas cabezas, cada una capturando un patrón distinto."

```python
# attention_viz.py
# Demo: visualización simple de una matriz de atención sobre una frase.
# Para que sea didáctico y sin dependencias pesadas, construimos una
# matriz "a mano" que ilustra patrones típicos: pronombre → sustantivo,
# verbo → sujeto, palabras temáticamente relacionadas.

import numpy as np
import matplotlib.pyplot as plt

tokens = ["El", "modelo", "ajusta", "la", "función",
          "de", "loss", "con", "el", "gradiente", "."]
n = len(tokens)

# Matriz random suave + refuerzos en relaciones específicas.
rng = np.random.default_rng(42)
A = rng.uniform(0.0, 0.15, size=(n, n))

# Refuerzos didácticos (fila = quien atiende, columna = a quién):
A[2, 1] += 0.7   # 'ajusta' -> 'modelo'  (verbo -> sujeto)
A[4, 6] += 0.7   # 'función' -> 'loss'
A[6, 4] += 0.5   # 'loss' -> 'función'
A[9, 4] += 0.6   # 'gradiente' -> 'función'
A[9, 6] += 0.5   # 'gradiente' -> 'loss'
A[3, 4] += 0.6   # 'la' -> 'función' (artículo -> sustantivo)
A[8, 9] += 0.6   # 'el' -> 'gradiente'

# Cada fila suma 1 (softmax-like), como en atención real.
A = A / A.sum(axis=1, keepdims=True)

fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(A, cmap="viridis")
ax.set_xticks(range(n)); ax.set_xticklabels(tokens, rotation=45, ha="right")
ax.set_yticks(range(n)); ax.set_yticklabels(tokens)
ax.set_xlabel("Atendido (key)")
ax.set_ylabel("Atendiendo (query)")
ax.set_title("Matriz de atención (ilustrativa)\nfila = token que mira, columna = token mirado")
fig.colorbar(im, ax=ax, fraction=0.046)
plt.tight_layout()
plt.show()
```

---

**Fin del material.**

**Notas para quien convierta esto a HTML con Claude Code:**
- Las slides 1, 2, 25 y 27 son ancla; el resto es contenido de bloque.
- Los bullets están limitados a 5-6 por slide; donde necesité más, partí en dos slides.
- Las demos son self-contained: un archivo por demo, ejecutables independientemente.
- El instructor puede saltearse Demo 4 si va corto de tiempo; los Bloques 3, 4 y 5 dependen más de sus demos.
- Si se quiere acortar el bloque 6 a 6 min, sacar la mención a Llama 3.1 405B y dejar sólo Kaplan/Chinchilla.
- Si se quiere extender el bloque 7 a 12 min, agregar un mini-demo de Claude Code en pantalla resolviendo un bug trivial en un repo de juguete.