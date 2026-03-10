# OmniWeaveDB Blueprint

## 1) Core idea: One fabric, not many silos

OmniWeaveDB is a search-engine-native database where all information is represented in a single relational substrate called the **Unified Meaning Fabric (UMF)**.

Instead of storing text, graph edges, vectors, and metadata in separate engines, UMF encodes everything as:

- **Nodes**: terms, documents, entities, URLs, users, topics, events.
- **Typed edges**: lexical, semantic, structural, temporal, behavioral.
- **Field energy**: a dynamic relevance score updated over time and query context.

This creates a fundamentally different behavior: retrieval becomes *field traversal + resonance scoring* rather than isolated index lookups.

## 2) What is required to make it work end-to-end

To build a real production version, we need these subsystems.

### A. Ingestion and normalization

- Web crawler output stream (content, links, headers, language, time).
- Canonicalization (URL normalization, duplicate detection, boilerplate removal).
- Content parsing (HTML to text blocks, anchors, semantic sections).
- Multilingual tokenization and entity extraction.

### B. Unified Meaning Fabric data model

- Global node ID allocator.
- Typed edge schema with confidence/weight.
- Node and edge versioning (for updates and rollbacks).
- Temporal snapshots for freshness-aware search.

### C. Indexing and update engine

- Incremental edge updates per document ingest.
- Term-to-document lexical edges.
- Entity/topic semantic edges.
- Link graph structural edges.
- Time edges for recency decay.

### D. Query understanding and retrieval

- Query parser (tokens + entities + intent hints).
- Fabric expansion (neighborhood exploration around query nodes).
- Resonance ranking combining lexical, semantic, structural, and temporal signals.
- Top-k retrieval with explanation traces.

### E. Storage and systems layer

- Log-structured storage for append-heavy updates.
- Segment compaction.
- Memory cache for hot nodes and edges.
- Replication and sharding strategy.

### F. Quality and safety

- Spam resistance features.
- Trust/authority scoring.
- Policy filters.
- Observability and audit trails.

## 3) Revolutionary properties

1. **No separate domain boundaries**: text, links, entities, behavior all represented identically as field interactions.
2. **Native relation memory**: relationships are first-class, not post-processing artifacts.
3. **Resonance ranking**: score emerges from multi-signal propagation in the fabric.
4. **Temporal plasticity**: freshness and historical importance are simultaneously represented.
5. **Explainable retrieval paths**: every result can show which nodes/edges contributed.

## 4) Skeleton implemented in this repository

The current code provides an in-memory prototype that demonstrates:

- Document ingestion.
- Term indexing.
- Entity indexing.
- Link relation storage.
- Temporal and authority-aware scoring.
- Query-time neighborhood expansion.

It is intentionally minimal but executable so future iterations can replace internals with distributed storage.

## 5) Next evolution steps

1. Swap in persistent segment storage.
2. Add embeddings as additional relation channels.
3. Introduce distributed partitioning by graph cuts.
4. Add online learning from click feedback.
5. Build explainability API for ranking traces.
