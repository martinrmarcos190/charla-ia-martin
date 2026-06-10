# Fundamentos de IA — Presentación (spec para Claude Code)

> **Para Claude Code:** este archivo es la especificación de una presentación de slides para una clase presencial de 75 min. Construí un **deck HTML autocontenido** a partir de esto. Abajo van (a) las instrucciones técnicas de build, (b) el contenido slide por slide, y (c) las cuatro demos interactivas embebidas. El contenido textual está en español rioplatense y debe respetarse tal cual. No reordenes slides.

---

## A. Instrucciones de build (leer primero)

**Objetivo:** un único archivo `index.html` (o reveal.js con assets locales) que el instructor abre en el navegador y proyecta. Debe funcionar **sin notebook** y, en lo posible, **sin conexión** durante la clase.

**Stack sugerido:**
- **reveal.js** como motor de slides (vía CDN o, mejor, vendoreado localmente para que ande offline en el aula).
- Tema oscuro, alto contraste, tipografía grande (esto se proyecta). Code blocks con syntax highlighting.
- Cada demo va embebida como HTML/JS dentro de su slide (ver sección C). Las demos deben poder dispararse con un botón y reiniciarse.

**Decisiones de las demos (importante, ya están tomadas):**

| Demo | Modo | Implementación |
|---|---|---|
| 1. Descenso de gradiente 2D | **Live en navegador** | JS puro + `<canvas>`. Sin dependencias externas. Slider de learning rate. |
| 2. Embeddings + coseno | **Precomputado** (default) | Matriz de similitud calculada en Python, embebida como JSON. Heatmap interactivo. Variante live opcional con `transformers.js`. |
| 3. Mapa de atención | **Precomputado** | Matriz embebida como JSON (2-3 oraciones). Heatmap con hover. |
| 4. Tokenización | **Live en navegador** | `gpt-tokenizer` vía CDN/ESM. Input de texto → tokens en tiempo real. Toggle `cl100k_base`/`o200k_base`. |

**Por qué precomputado en 2 y 3:** correr un modelo de embeddings real en el navegador (transformers.js) baja ~30 MB y necesita red; en un aula es frágil. Para esas dos demos, **embebé los resultados ya calculados** y mostralos de forma interactiva. Dejá la variante live como bloque comentado, por si hay buena conexión.

**Para generar los JSON precomputados** (corré esto una vez y pegá la salida en los `<script type="application/json">` correspondientes): el snippet Python está al final de cada demo en la sección C.

**Accesibilidad de proyección:** fuente mínima 28px en cuerpo, 40px+ en títulos; nada de texto gris sobre gris; los heatmaps con etiquetas legibles.

---

## B. Contenido slide por slide

> Formato: **Título** → contenido en pantalla (bullets cortos, lo que se proyecta) → 🖼️ nota visual para vos, Claude Code.

### Slide 0 — Portada
- **Fundamentos de IA**
- Módulo 1 · Clase 1 · 75 min — Curso de IA Aplicada para MLOps
- *De random forests a agentes: el puente conceptual*

🖼️ Portada limpia, tema oscuro. Subtítulo en menor jerarquía.

---

### Slide 1 — Hoja de ruta
- Lo que ya sabés: Docker · IaC · CI/CD · pipelines · training · serving
- Lo que tendemos hoy: el puente hacia **LLMs y agentes**
- Regla: lo que ya sabés no lo explicamos, lo usamos como **analogía**
- 4 demos en vivo · todo en esta presentación · sin notebooks

🖼️ Dos columnas: "Ya sabés" / "Vas a entender hoy". Flecha entre ambas.

---

### Slide 2 — Línea de tiempo (ANCLA)
- **2001** · Random Forest (Breiman) — tabular sigue vigente
- **2012** · AlexNet — deep learning sale del laboratorio
- **2013** · Word2Vec (Mikolov) — embeddings
- **2017** · *Attention Is All You Need* (Vaswani et al.) — Transformers
- **2018–2020** · BERT · GPT-2 · GPT-3 — escala
- **2022** · ReAct (Yao et al.) + ChatGPT
- **2024** · Anthropic — *Building Effective Agents*
- **2025** · Claude Code GA · **$1B run-rate revenue en noviembre** (Anthropic, dic-2025)

🖼️ Timeline horizontal con 3 zonas de color: ML clásico (2001-2012) / deep learning + transformers (2012-2020) / LLMs + agentes (2020-2025). Esta slide es de referencia: hacela visualmente fuerte.

---

### Slide 3 — 1.1 De reglas a patrones
- Software tradicional: programás el **qué hacer** (`if`, reglas)
- ML: programás el **cómo aprender** (le das ejemplos)
- Las reglas no escalan: "reconocé un gato", "esto es spam"
- Costo del paradigma: opacidad · no determinismo · dependencia de los datos

🖼️ Contraste lado a lado: bloque de `if/else` vs nube de datos → modelo.

---

### Slide 4 — 1.2 Un modelo es un artefacto compilado
- Viene de la estadística (regresión = años 50-60). Cambió la escala, no la idea.
- Clásicos vigentes: regresión · árboles · **Random Forest** · gradient boosting · SVM
- **La analogía clave:**

| Mundo DevOps | Mundo ML |
|---|---|
| Código fuente | Dataset de entrenamiento |
| `docker build` | `model.fit()` |
| Imagen de Docker | Modelo serializado (`.pkl`, `.safetensors`) |
| Container registry | Model registry |
| `docker run` | `model.predict()` |

- Como todo binario: **opaco**. No lo leés como un `.py`.

🖼️ La tabla es el centro de la slide. Resaltala. Pie: *Breiman (2001), Random Forests, Machine Learning 45(1):5–32*.

---

### Slide 5 — 1.3 Redes neuronales y backpropagation
- Una red = `activación(W·x + b)` apilado en capas
- Aprenden las features solas → adiós feature engineering manual
- **Backprop** (Rumelhart, Hinton, Williams · *Nature*, 1986):
  1. pesos random → 2. predigo (mal) → 3. mido el error
  4. propago el error hacia atrás → 5. ajusto cada peso → 6. repito ×millones
- Analogía: un **CI loop infinito** con auto-fix de los pesos

🖼️ Diagrama del loop de 6 pasos en círculo. Pie con la cita de Nature.

---

### Slide 6 — 🎬 Demo 1: el modelo se equivoca y se ajusta
- Descenso de gradiente sobre una superficie de error
- El learning rate decide si converge, diverge o se arrastra

🖼️ **Demo embebida #1** (ver sección C.1). Canvas con contornos + punto que baja + slider de learning rate + botón "Reiniciar".

---

### Slide 7 — 1.4 Embeddings: coordenadas GPS del significado
- One-hot: cada palabra ortogonal → **no captura significado**
- Embedding: vector denso (100–3072 dim) donde **proximidad = similitud semántica**
- `vector(rey) − vector(hombre) + vector(mujer) ≈ vector(reina)` — aritmética sobre significado
- Métrica de cercanía: **similitud coseno**
- Base de: RAG · búsqueda semántica · recomendadores · deduplicación

🖼️ Mapa 2D estilo GPS: "perro"/"gato"/"cachorro" agrupados; "factura"/"inflación" en otro cluster lejano. Pie: *Mikolov et al. (2013), arXiv:1301.3781 · Pennington et al. (2014), EMNLP*.

---

### Slide 8 — 🎬 Demo 2: ¿perro está más cerca de gato o de factura?
- `all-MiniLM-L6-v2` · 384 dimensiones · ~80 MB · local
- 1.00 = idéntico · 0.00 = sin relación

🖼️ **Demo embebida #2** (ver sección C.2). Heatmap interactivo de la matriz de similitud; al hacer hover, mostrar el par de frases y el valor.

---

### Slide 9 — 1.5 Transformers y atención: la revolución
- Pre-2017: RNN/LSTM → secuenciales, pierden contexto largo, **no paralelizan**
- 2017: *Attention Is All You Need* (Vaswani et al., Google)
- Idea: **cada token mira a todos los demás simultáneamente**
- Mecánica: **Query** (qué busco) · **Key** (qué ofrezco) · **Value** (qué tengo) → softmax(Q·Kᵀ/√dₖ)·V
- Multi-head: varios en paralelo, cada uno aprende relaciones distintas
- Por qué fue LA revolución: **paraleliza** (escala) + **captura contexto largo**

🖼️ Diagrama: una oración con flechas de cada token a todos los demás. Analogía al pie: *RNN = build secuencial · Transformer = build paralelo*. Cita: *arXiv:1706.03762*.

---

### Slide 10 — 🎬 Demo 3: ¿quién mira a quién?
- Self-attention sobre una oración
- Cada fila: un token y a quién le presta atención

🖼️ **Demo embebida #3** (ver sección C.3). Heatmap con selector de oración (2-3 precargadas) y hover que resalta fila/columna.

---

### Slide 11 — 1.6 De Transformers a LLMs
- Receta: Transformer **decoder-only** → escalar (GPT-3 = 175B) → entrenar para **predecir el próximo token** → fine-tuning + RLHF
- **Un LLM es un autocomplete cósmico**
- Tokenización: el modelo ve **enteros**, no strings · `cl100k_base` (GPT-4) · `o200k_base` (GPT-4o, GPT-5, o1/o3/o4)
- ⚠️ **NO ES DETERMINÍSTICO**: muestrea de una distribución (`temperature`, `top_p`)

🖼️ Diagrama: prompt → [Transformer] → distribución de probabilidad sobre el vocabulario → muestreo → token. Citas: *Brown et al. (2020), arXiv:2005.14165 (GPT-3); Devlin et al. (2018), arXiv:1810.04805 (BERT)*.

---

### Slide 12 — El no-determinismo te cambia el MLOps
- Mismo prompt → outputs diferentes
- Se rompe `assert output == "..."` → evaluá por propiedades, LLM-as-judge, golden sets semánticos
- Versioná el modelo explícitamente (el proveedor lo actualiza sin avisar)
- `temperature=0` ayuda, no garantiza
- Diseño: caching · idempotencia · schema validation · retries · observability

🖼️ Tabla "ML clásico (determinístico) vs LLM (estocástico)" en dos columnas.

---

### Slide 13 — 🎬 Demo 4: lo que el modelo realmente ve
- El español gasta más tokens que el inglés (= más costo y context window)
- `o200k_base` suele ser más eficiente en multilingüe

🖼️ **Demo embebida #4** (ver sección C.4). Input de texto en vivo → chips de tokens coloreados + contador. Toggle entre encodings. Frases de ejemplo precargadas.

---

### Slide 14 — 1.7 De LLM a Agente
- LLM solo: **genera texto**. Un agente: **planifica, usa tools, ejecuta acciones, observa, itera**
- Anthropic (2024): *workflows* (camino de código predefinido) vs *agents* (el LLM dirige su propio proceso)
- El loop **ReAct** (Yao et al., 2022): **PENSAR → ACTUAR (tool) → OBSERVAR → ¿terminé? → loop**
- Bloque mínimo: **augmented LLM** = LLM + retrieval + tools + memory

🖼️ Diagrama del loop ReAct, circular y prominente:
```
PENSAR ─► ACTUAR (tool call) ─► OBSERVAR (resultado) ─► ¿terminé?
   ▲                                                       │ no
   └───────────────────────────────────────────────────────┘
```
Cita: *Yao et al. (2022), arXiv:2210.03629 · Anthropic, Building Effective Agents (2024)*.

---

### Slide 15 — Impacto real en software (2025–2026)
- **Claude Code**: GA mayo 2025 · **$1B run-rate revenue en nov-2025** (Anthropic, 3-dic-2025)
- **Stripe**: 1.370 ingenieros · migración Scala→Java de 10k líneas en **4 días** (vs 10 engineer-weeks)
- **Wiz**: 50k líneas Python→Go en **~20 horas** (vs 2-3 meses)
- **Ramp**: **−80%** en tiempo de investigación de incidentes
- **Rakuten**: delivery de features de **24 → 5 días** hábiles
- ⚖️ El contraste honesto:
  - **METR 2025** (arXiv:2507.09089): devs experimentados **19% más lentos** con la herramienta
  - **Veracode 2025**: el modelo eligió el método **inseguro el 45% de las veces**
  - **Gartner** (jun-2025): **>40%** de proyectos agénticos se cancelan antes de fin de 2027
  - **DORA 2025**: la IA *"magnifica las fortalezas de las orgs de alto rendimiento y las disfunciones de las que luchan"*

🖼️ Mitad superior verde (wins), mitad inferior ámbar (cautelas). No mezclar visualmente.

---

### Slide 16 — Tu rol está cambiando
- De *"write code → run tests → fix → repeat"*
- A *"set goal → review changes → approve"*
- **Diseñás la fábrica, no atornillás cada pieza**
- Próxima clase: **tools, skills y patrones de diseño de agentes** — con las manos en la masa

🖼️ Antes/después. Imagen mental de "operario" → "diseñador de la línea de producción".

---

### Slide 17 — Recap
- ML clásico = **artefactos compilados** desde datos
- Redes + backprop = aprenden features vía loop error/corrección
- Embeddings = significado en **coordenadas geométricas**
- Transformers = **atención** rompe la secuencialidad → escala
- LLMs = Transformers gigantes que autocompletan, **no determinísticos**
- Agentes = el LLM que **actúa**: piensa, usa tools, observa, itera
- **Preguntas**

🖼️ Las 6 ideas como íconos en grilla. Slide final de cierre.

---

## C. Demos interactivas embebidas

> Cada demo es un componente HTML/JS autónomo que se inserta en su slide. Abajo va una implementación de referencia para cada una; adaptá el estilo al tema del deck.

### C.1 — Demo descenso de gradiente (live, JS puro)

Insertar en Slide 6. Sin dependencias. Canvas con contornos de una loss cuadrática, punto que desciende, slider de learning rate, botón reiniciar.

```html
<div class="demo" id="demo-gd">
  <canvas id="gd-canvas" width="640" height="480"></canvas>
  <div class="controls">
    <label>learning rate: <span id="gd-lr-val">0.10</span></label>
    <input type="range" id="gd-lr" min="0.01" max="0.55" step="0.01" value="0.10">
    <button id="gd-run">▶ Correr</button>
    <button id="gd-reset">↺ Reiniciar</button>
    <span id="gd-status"></span>
  </div>
</div>
<script>
(function () {
  const cv = document.getElementById('gd-canvas');
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;
  // Loss elíptica: L(x,y) = (x-3)^2 + 4*(y+2)^2 ; mínimo en (3,-2).
  const loss = (x, y) => (x - 3) ** 2 + 4 * (y + 2) ** 2;
  const grad = (x, y) => [2 * (x - 3), 8 * (y + 2)];
  // Mapeo de coords del mundo [-6,6] al canvas.
  const X0 = -6, X1 = 6, Y0 = -6, Y1 = 6;
  const sx = x => (x - X0) / (X1 - X0) * W;
  const sy = y => H - (y - Y0) / (Y1 - Y0) * H;

  function drawContours() {
    ctx.clearRect(0, 0, W, H);
    for (let i = 0; i < W; i += 4) {
      for (let j = 0; j < H; j += 4) {
        const wx = X0 + i / W * (X1 - X0);
        const wy = Y0 + (H - j) / H * (Y1 - Y0);
        const v = loss(wx, wy);
        const t = Math.min(1, v / 120);
        ctx.fillStyle = `hsl(${220 - t * 160}, 70%, ${20 + t * 35}%)`;
        ctx.fillRect(i, j, 4, 4);
      }
    }
    // Mínimo.
    ctx.fillStyle = 'gold';
    ctx.beginPath(); ctx.arc(sx(3), sy(-2), 9, 0, 7); ctx.fill();
    ctx.strokeStyle = 'black'; ctx.stroke();
  }

  let pt, traj, timer = null;
  function reset() {
    if (timer) clearInterval(timer), timer = null;
    pt = [-4, 3]; traj = [pt.slice()];
    drawContours(); drawPoint();
    document.getElementById('gd-status').textContent = `loss = ${loss(...pt).toFixed(2)}`;
  }
  function drawPoint() {
    ctx.strokeStyle = 'red'; ctx.lineWidth = 2; ctx.beginPath();
    traj.forEach((p, k) => k ? ctx.lineTo(sx(p[0]), sy(p[1])) : ctx.moveTo(sx(p[0]), sy(p[1])));
    ctx.stroke();
    ctx.fillStyle = 'red';
    ctx.beginPath(); ctx.arc(sx(pt[0]), sy(pt[1]), 7, 0, 7); ctx.fill();
  }
  function step() {
    const lr = parseFloat(document.getElementById('gd-lr').value);
    const g = grad(...pt);
    pt = [pt[0] - lr * g[0], pt[1] - lr * g[1]];
    traj.push(pt.slice());
    if (traj.length > 60 || Math.abs(pt[0]) > 12 || Math.abs(pt[1]) > 12) { clearInterval(timer); timer = null; }
    drawContours(); drawPoint();
    document.getElementById('gd-status').textContent = `loss = ${loss(...pt).toFixed(2)}`;
  }
  document.getElementById('gd-lr').addEventListener('input', e =>
    document.getElementById('gd-lr-val').textContent = parseFloat(e.target.value).toFixed(2));
  document.getElementById('gd-run').addEventListener('click', () => {
    if (timer) return; timer = setInterval(step, 120);
  });
  document.getElementById('gd-reset').addEventListener('click', reset);
  reset();
})();
</script>
```

**Para mostrar / decir:** punto rojo = parámetros; estrella = óptimo. Subí el learning rate al máximo → diverge (saltos). Bajalo al mínimo → se arrastra. Es el mismo `lr` del entrenamiento real.

---

### C.2 — Demo embeddings + similitud coseno (precomputado)

Insertar en Slide 8. La matriz se precomputa en Python y se pega como JSON. Render: heatmap con hover.

**Snippet Python para generar el JSON (correr una vez, pegar la salida):**

```python
from sentence_transformers import SentenceTransformer
import numpy as np, json
m = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
frases = [
    "El perro corre por el parque",
    "Mi gato duerme arriba del sillón",
    "El cachorro persigue una pelota",
    "Pagué la factura de la luz ayer",
    "Tengo que abonar el servicio eléctrico",
    "La inflación de Argentina en 2025",
]
e = m.encode(frases, convert_to_numpy=True, normalize_embeddings=True)
sim = (e @ e.T).round(3).tolist()
print(json.dumps({"frases": frases, "sim": sim}, ensure_ascii=False))
```

**Componente HTML (pegar el JSON en el `<script type="application/json">`):**

```html
<div class="demo" id="demo-emb">
  <div id="emb-grid"></div>
  <p id="emb-hover">Pasá el mouse sobre una celda…</p>
</div>
<script type="application/json" id="emb-data">
{ "frases": ["...pegar aquí la salida del snippet Python..."], "sim": [[1.0]] }
</script>
<script>
(function () {
  const data = JSON.parse(document.getElementById('emb-data').textContent);
  const { frases, sim } = data;
  const grid = document.getElementById('emb-grid');
  const n = frases.length;
  grid.style.display = 'grid';
  grid.style.gridTemplateColumns = `repeat(${n}, 1fr)`;
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
    const v = sim[i][j];
    const cell = document.createElement('div');
    cell.className = 'emb-cell';
    cell.textContent = v.toFixed(2);
    cell.style.background = `hsl(${200 - v * 160}, 70%, ${25 + v * 30}%)`;
    cell.style.padding = '14px'; cell.style.textAlign = 'center'; cell.style.cursor = 'pointer';
    cell.onmouseenter = () => document.getElementById('emb-hover').textContent =
      `sim("${frases[i]}", "${frases[j]}") = ${v.toFixed(3)}`;
    grid.appendChild(cell);
  }
})();
</script>
```

**Variante LIVE opcional (transformers.js, requiere red, ~30 MB):**

```html
<!-- Descomentar sólo si hay buena conexión en el aula.
<script type="module">
  import { pipeline, cos_sim } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers';
  const extractor = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');
  // const out = await extractor(frases, { pooling: 'mean', normalize: true });
  // ...calcular cos_sim entre pares y renderizar el mismo grid...
</script>
-->
```

**Para mostrar / decir:** perro/gato ≈ 0.50 · perro/cachorro ≈ 0.65 · perro/factura ≈ 0.05 · factura/abonar ≈ 0.65. Cercanía = significado.

---

### C.3 — Demo mapa de atención (precomputado)

Insertar en Slide 10. Matriz de atención precomputada por oración, embebida como JSON. Heatmap con hover que resalta fila/columna.

**Snippet Python para generar el JSON:**

```python
from sentence_transformers import SentenceTransformer
import numpy as np, json
m = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
oraciones = [
    "El gato que vi ayer en el parque estaba durmiendo",
    "La factura que llegó hoy tiene un error grave",
]
salida = []
for o in oraciones:
    toks = o.split()
    e = m.encode(toks, convert_to_numpy=True)
    dk = e.shape[1]
    s = e @ e.T / np.sqrt(dk)
    s = s - s.max(1, keepdims=True)
    a = np.exp(s); a = a / a.sum(1, keepdims=True)
    salida.append({"tokens": toks, "attn": a.round(3).tolist()})
print(json.dumps(salida, ensure_ascii=False))
```

**Componente HTML:**

```html
<div class="demo" id="demo-attn">
  <select id="attn-sel"></select>
  <div id="attn-grid"></div>
  <p id="attn-hover"></p>
</div>
<script type="application/json" id="attn-data">
[ { "tokens": ["..."], "attn": [[1.0]] } ]
</script>
<script>
(function () {
  const data = JSON.parse(document.getElementById('attn-data').textContent);
  const sel = document.getElementById('attn-sel');
  data.forEach((d, i) => { const o = document.createElement('option'); o.value = i; o.textContent = d.tokens.join(' '); sel.appendChild(o); });
  function render(idx) {
    const { tokens, attn } = data[idx];
    const grid = document.getElementById('attn-grid');
    const n = tokens.length;
    grid.innerHTML = '';
    grid.style.display = 'grid';
    grid.style.gridTemplateColumns = `120px repeat(${n}, 1fr)`;
    grid.appendChild(document.createElement('div')); // esquina
    tokens.forEach(t => { const h = document.createElement('div'); h.textContent = t; h.className = 'attn-head'; grid.appendChild(h); });
    for (let i = 0; i < n; i++) {
      const rh = document.createElement('div'); rh.textContent = tokens[i]; rh.className = 'attn-head'; grid.appendChild(rh);
      for (let j = 0; j < n; j++) {
        const v = attn[i][j];
        const c = document.createElement('div');
        c.textContent = v.toFixed(2);
        c.style.background = `hsl(${260 - v * 200}, 70%, ${20 + v * 45}%)`;
        c.style.padding = '8px'; c.style.textAlign = 'center';
        c.onmouseenter = () => document.getElementById('attn-hover').textContent =
          `"${tokens[i]}" presta ${(v * 100).toFixed(0)}% de atención a "${tokens[j]}"`;
        grid.appendChild(c);
      }
    }
  }
  sel.addEventListener('change', e => render(+e.target.value));
  render(0);
})();
</script>
```

**Para mostrar / decir:** aclarar que es simplificación didáctica (Q/K/V crudos, no proyecciones aprendidas, sin multi-head). Cada fila = un token preguntando a quién mira. Señalar verbo → sujeto.

---

### C.4 — Demo tokenización (live, gpt-tokenizer vía ESM)

Insertar en Slide 13. Live, sin precómputo. Carga `gpt-tokenizer` desde CDN (esm.sh / jsDelivr). Si el aula es offline, vendorear el paquete localmente.

```html
<div class="demo" id="demo-tok">
  <textarea id="tok-input" rows="3" style="width:100%">Hola, ¿cómo andás che?</textarea>
  <div class="controls">
    <label><input type="radio" name="enc" value="cl100k" checked> cl100k_base (GPT-4)</label>
    <label><input type="radio" name="enc" value="o200k"> o200k_base (GPT-4o/5)</label>
    <span id="tok-count"></span>
  </div>
  <div id="tok-chips" style="line-height:2.2"></div>
</div>
<script type="module">
  // gpt-tokenizer expone encodings con nombre. Import dinámico según selección.
  import * as cl100k from 'https://esm.sh/gpt-tokenizer/encoding/cl100k_base';
  import * as o200k  from 'https://esm.sh/gpt-tokenizer/encoding/o200k_base';
  const palette = ['#3b82f6','#10b981','#f59e0b','#ef4444','#8b5cf6','#ec4899','#14b8a6','#eab308'];
  function render() {
    const txt = document.getElementById('tok-input').value;
    const enc = document.querySelector('input[name=enc]:checked').value === 'o200k' ? o200k : cl100k;
    const ids = enc.encode(txt);
    document.getElementById('tok-count').textContent = `${ids.length} tokens`;
    const box = document.getElementById('tok-chips'); box.innerHTML = '';
    ids.forEach((id, k) => {
      const piece = enc.decode([id]);
      const chip = document.createElement('span');
      chip.textContent = piece.replace(/ /g, '␣');
      chip.title = `id ${id}`;
      chip.style.cssText = `background:${palette[k % palette.length]};color:#fff;padding:3px 7px;margin:2px;border-radius:5px;font-family:monospace`;
      box.appendChild(chip);
    });
  }
  document.getElementById('tok-input').addEventListener('input', render);
  document.querySelectorAll('input[name=enc]').forEach(r => r.addEventListener('change', render));
  render();
</script>
```

**Frases de ejemplo para tener a mano:** `Hello, how are you today?` · `Hola, ¿cómo andás che?` · `import numpy as np` · `🚀 La IA está cambiando todo en 2026 🤖`

**Para mostrar / decir:** el español gasta más tokens que el inglés (costo + context window); código y emojis se tokenizan distinto; `o200k_base` suele ser más eficiente en multilingüe. Estimá costos **por token**, no por caracteres.

---

## D. Checklist para Claude Code

- [ ] Generar los 2 JSON precomputados (demos 2 y 3) corriendo los snippets Python, y pegarlos en sus `<script type="application/json">`.
- [ ] Vendorear reveal.js y `gpt-tokenizer` localmente si el aula puede estar sin conexión.
- [ ] Verificar que las 4 demos disparen y reinicien bien.
- [ ] Tipografía de proyección (≥28px cuerpo / ≥40px títulos), tema oscuro alto contraste.
- [ ] La Slide 2 (timeline) y la Slide 14 (loop ReAct) son las dos más visuales: cuidarlas.
- [ ] Respetar textos en rioplatense tal cual; no traducir ni reescribir.
- [ ] Pie de cita en las slides que la tienen (4, 5, 7, 9, 11, 14, 15).
