[🇬🇧 Read in English](README.md)

# Kalima

> Un asistente de documentos completamente local con RAG — sin APIs externas, sin enviar tus datos a ningún servidor.

Kalima te permite mantener conversaciones naturales con tus propios documentos. Haz preguntas en lenguaje natural y obtén respuestas precisas basadas en tus archivos. Todo corre en tu máquina: el LLM, los embeddings, la base de datos vectorial y la interfaz.

Desarrollado como parte de un Máster en Full Stack Development, Kalima fue un ejercicio deliberado para entender cómo funcionan los pipelines RAG de principio a fin — desde la ingesta de documentos hasta la generación de respuestas — sin depender de servicios de IA gestionados.

---

## Cómo funciona

```
┌─────────────┐     ┌──────────────┐     ┌────────────┐     ┌──────────────┐
│ Documentos  │────▶│  LlamaIndex  │────▶│  ChromaDB  │────▶│    Ollama    │
│  PDF / TXT  │     │  (indexado)  │     │ (vectores) │     │  (respuesta) │
└─────────────┘     └──────────────┘     └────────────┘     └──────────────┘
                                                                     │
                         ┌───────────────────────────────────────────┘
                         ▼
                  ┌─────────────┐
                  │  Streamlit  │  ◀── tú preguntas aquí
                  └─────────────┘
```

1. **Ingesta** — PyMuPDF lee los PDFs. LlamaIndex los trocea con `SentenceSplitter` y genera embeddings con `nomic-embed-text` a través de Ollama.
2. **Persistencia** — ChromaDB almacena los vectores en disco. El índice solo se reconstruye cuando se detectan documentos nuevos.
3. **Recuperación** — Al hacer una pregunta, se recuperan los fragmentos más relevantes y se reordenan con un cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`).
4. **Generación** — El contexto reordenado se pasa a `gemma3:4b` para generar una respuesta en streaming en el mismo idioma que la pregunta.
5. **Vigilancia en tiempo real** — Un observer de `watchdog` monitoriza la carpeta `docs/`. Los archivos nuevos se indexan automáticamente sin reiniciar la app.

---

## Stack técnico

| Capa | Tecnología | Por qué |
|---|---|---|
| LLM | Ollama (`gemma3:4b`) | Inferencia local, sin coste de API |
| Embeddings | Ollama (`nomic-embed-text`) | Alta calidad, completamente local |
| Vector DB | ChromaDB | Persistente, embebido, sin servidor |
| Orquestación | LlamaIndex | Abstracciones limpias para pipelines RAG |
| Reranker | SentenceTransformers (`cross-encoder/ms-marco-MiniLM-L-6-v2`) | Mejora significativamente la precisión de recuperación |
| Frontend | Streamlit | Rápido de iterar, suficiente para una herramienta local |
| Contenedorización | Docker + Docker Compose | Setup reproducible en cualquier máquina |

---

## Decisiones de diseño

**¿Por qué completamente local?** Privacidad. Los documentos que se alimentan a un sistema RAG suelen contener información sensible. Correr todo localmente significa que ningún dato sale de la máquina — sin OpenAI, sin Anthropic, sin vector stores en la nube.

**¿Por qué un reranker?** La búsqueda por similitud vectorial devuelve los fragmentos más *similares*, no necesariamente los más *relevantes*. El cross-encoder puntúa cada fragmento recuperado contra la pregunta real, mejorando significativamente la calidad de las respuestas con un pequeño coste de latencia.

**¿Por qué el modo de chat `condense_plus_context`?** Este modo condensa el historial de la conversación en una pregunta autónoma antes de la recuperación, lo que hace que las preguntas de seguimiento funcionen correctamente sin perder el contexto de turnos anteriores.

**¿Por qué ChromaDB en lugar de un vector store alojado?** Coherencia con la filosofía local-first. ChromaDB persiste en disco y no requiere infraestructura — solo una carpeta.

---

## Requisitos

- [Ollama](https://ollama.com) instalado y corriendo en el host
- Docker y Docker Compose
- 8GB+ RAM recomendado (16GB+ para `gemma3:12b`)

---

## Inicio rápido

### 1. Descargar los modelos necesarios

```bash
ollama pull gemma3:4b
ollama pull nomic-embed-text
```

### 2. Añadir documentos

Crea la carpeta `docs/` y coloca tus archivos `.pdf` dentro:

```bash
mkdir docs
cp tus-documentos/*.pdf docs/
```

### 3. Arrancar ⭐ Recomendado

La forma más rápida — sin necesidad de build. Usa la imagen pre-construida de GitHub Container Registry:

```yaml
# docker-compose.yml
services:
  app:
    container_name: kalima
    image: ghcr.io/nico-barroso/kalima:latest
    ports:
      - "8501:8501"
    environment:
      - OLLAMA_URL=http://host.docker.internal:11434
      - PYTHONUNBUFFERED=1
      - TRANSFORMERS_VERBOSITY=error
      - TOKENIZERS_PARALLELISM=false
    volumes:
      - ./docs:/app/docs
      - ./chroma_db:/app/chroma_db
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

```bash
docker compose up
```

Abre [http://localhost:8501](http://localhost:8501) en tu navegador.

---

## Alternativa: build desde el código fuente

Si quieres modificar el código:

```bash
git clone https://github.com/nico-barroso/kalima
cd kalima
docker compose up --build
```

> NOTA: La primera build tarda ~15–20 minutos — instala dependencias ML pesadas (torch, sentence-transformers). Las siguientes son instantáneas gracias a la caché de capas de Docker.

### O correr sin Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/main.py
```

---

## Estructura del proyecto

```
kalima/
├── app/
│   ├── main.py                         # Punto de entrada de la app
│   ├── constants.py                    # Configuración y variables de entorno
│   ├── pipeline/
│   │   ├── indexer.py                  # Orquestación de build y carga del índice
│   │   └── query.py                    # Motor de consulta, reranker, historial
│   ├── rag/
│   │   ├── chunks/splitter.py          # Configuración del SentenceSplitter
│   │   ├── corpus/reader.py            # Lector de documentos con PyMuPDF
│   │   ├── corpus/watcher.py           # Observer de archivos con Watchdog
│   │   ├── embeddings/                 # Inicialización de embeddings y LLM
│   │   └── vectorstore/store.py        # Setup de ChromaDB y gestión del índice
│   └── frontend/
│       ├── run_chat.py                 # Controlador principal de la UI
│       └── components/                 # Componentes de Streamlit
├── docs/                               # Tus documentos van aquí
├── chroma_db/                          # Persistencia del vector store (git-ignored)
├── Dockerfile
└── docker-compose.yml
```

---

## Licencia

MIT — ver [LICENSE](LICENSE) para más detalles.
