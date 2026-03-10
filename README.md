# OmniWeaveDB (concept skeleton)

OmniWeaveDB is a **search-engine-native database concept** designed to treat every piece of data (text, links, metadata, entities, time, popularity, embeddings) as one interconnected field.

This repository now contains:

- A blueprint of the revolutionary concept and all required subsystems.
- A working in-memory skeleton implementation to ingest web-like documents.
- Relation-aware indexing for terms, entities, links, and temporal context.
- Basic query and neighborhood expansion support.

## Why this is different

Traditional systems split concerns into separate engines (document DB + graph DB + vector DB + index).
OmniWeaveDB collapses these boundaries into a single structure called a **Unified Meaning Fabric**.

Each term or entity is stored as a node in one fabric, and every ingestion adds relation edges with typed strengths:

- lexical (token appears in document)
- semantic (entity associated with term)
- structural (links between documents)
- temporal (document freshness and events)

## Project layout

- `docs/OMNIWEAVE_BLUEPRINT.md` — end-to-end vision and required components.
- `src/omniweave_db/core.py` — runnable skeleton.
- `tests/test_core.py` — executable checks of core flows.

## Quick start

```bash
python -m unittest discover -s tests -v
```

```python
from omniweave_db import Document, OmniWeaveDB

db = OmniWeaveDB()
db.ingest(
    Document(
        doc_id="doc-1",
        title="Unified data for search",
        text="Search engines need ranking, meaning, and links working together.",
        links=["doc-2"],
        entities=["search_engine", "ranking"],
        timestamp=1710000000,
        authority=0.8,
    )
)

print(db.query("search meaning", top_k=3))
```

## Current maturity

This is a **foundation skeleton**: in-memory and intentionally simple.
It is structured so we can evolve it into a distributed storage and retrieval engine in future iterations.
