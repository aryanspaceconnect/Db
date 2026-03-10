"""Core in-memory skeleton for OmniWeaveDB."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
import math
import re
from typing import Dict, Iterable, List, Sequence, Set, Tuple


TOKEN_PATTERN = re.compile(r"\b[a-z0-9_]{2,}\b")


@dataclass(frozen=True)
class Document:
    """A web-like document unit."""

    doc_id: str
    title: str
    text: str
    links: Sequence[str] = field(default_factory=tuple)
    entities: Sequence[str] = field(default_factory=tuple)
    timestamp: int = 0
    authority: float = 0.5


class OmniWeaveDB:
    """Unified Meaning Fabric skeleton for indexing and search."""

    def __init__(self) -> None:
        self.documents: Dict[str, Document] = {}
        self.term_to_docs: Dict[str, Counter[str]] = defaultdict(Counter)
        self.entity_to_docs: Dict[str, Counter[str]] = defaultdict(Counter)
        self.doc_links: Dict[str, Set[str]] = defaultdict(set)
        self.doc_backlinks: Dict[str, Set[str]] = defaultdict(set)
        self.doc_terms: Dict[str, Counter[str]] = defaultdict(Counter)
        self.max_timestamp: int = 0

    def ingest(self, doc: Document) -> None:
        """Ingest or update a document into the unified fabric."""
        if doc.doc_id in self.documents:
            self._remove_document(doc.doc_id)

        self.documents[doc.doc_id] = doc
        self.max_timestamp = max(self.max_timestamp, doc.timestamp)

        tokens = self._tokenize(f"{doc.title} {doc.text}")
        token_counts = Counter(tokens)
        self.doc_terms[doc.doc_id] = token_counts

        for term, freq in token_counts.items():
            self.term_to_docs[term][doc.doc_id] = freq

        for entity in doc.entities:
            normalized = entity.strip().lower()
            if normalized:
                self.entity_to_docs[normalized][doc.doc_id] += 1

        for target in doc.links:
            self.doc_links[doc.doc_id].add(target)
            self.doc_backlinks[target].add(doc.doc_id)

    def query(self, text: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """Return ranked document IDs and scores."""
        query_terms = self._tokenize(text)
        if not query_terms:
            return []

        scores: Counter[str] = Counter()
        for term in query_terms:
            docs = self.term_to_docs.get(term, {})
            idf = self._idf(term)
            for doc_id, tf in docs.items():
                scores[doc_id] += (1 + math.log(tf)) * idf

        expanded = self._expand_neighbors(set(scores.keys()))
        for doc_id in expanded:
            if doc_id in self.documents:
                scores[doc_id] += 0.15

        ranked = []
        for doc_id, base_score in scores.items():
            ranked.append((doc_id, self._apply_global_signals(doc_id, base_score)))

        ranked.sort(key=lambda item: item[1], reverse=True)
        return ranked[:top_k]

    def related_terms(self, term: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """Find terms that co-occur with a term across documents."""
        normalized = term.strip().lower()
        if not normalized or normalized not in self.term_to_docs:
            return []

        co_terms: Counter[str] = Counter()
        for doc_id in self.term_to_docs[normalized].keys():
            for candidate, freq in self.doc_terms[doc_id].items():
                if candidate != normalized:
                    co_terms[candidate] += freq

        return co_terms.most_common(top_k)

    def _apply_global_signals(self, doc_id: str, score: float) -> float:
        doc = self.documents[doc_id]
        freshness = self._freshness(doc.timestamp)
        authority = max(0.0, min(1.0, doc.authority))
        link_popularity = min(1.0, len(self.doc_backlinks.get(doc_id, set())) / 10.0)

        return score * (1.0 + 0.4 * freshness + 0.3 * authority + 0.3 * link_popularity)

    def _freshness(self, ts: int) -> float:
        if self.max_timestamp <= 0:
            return 0.0
        age = max(0, self.max_timestamp - ts)
        return 1.0 / (1.0 + age / 100000)

    def _idf(self, term: str) -> float:
        total_docs = max(1, len(self.documents))
        docs_with_term = max(1, len(self.term_to_docs.get(term, {})))
        return math.log((1 + total_docs) / docs_with_term) + 1.0

    def _expand_neighbors(self, seed_docs: Set[str]) -> Set[str]:
        expanded = set(seed_docs)
        for doc_id in list(seed_docs):
            expanded.update(self.doc_links.get(doc_id, set()))
            expanded.update(self.doc_backlinks.get(doc_id, set()))
        return expanded

    def _remove_document(self, doc_id: str) -> None:
        old_doc = self.documents.pop(doc_id)

        old_terms = self.doc_terms.pop(doc_id, Counter())
        for term in old_terms:
            self.term_to_docs[term].pop(doc_id, None)
            if not self.term_to_docs[term]:
                self.term_to_docs.pop(term, None)

        for entity in old_doc.entities:
            normalized = entity.strip().lower()
            if normalized in self.entity_to_docs:
                self.entity_to_docs[normalized].pop(doc_id, None)
                if not self.entity_to_docs[normalized]:
                    self.entity_to_docs.pop(normalized, None)

        for target in self.doc_links.get(doc_id, set()):
            self.doc_backlinks[target].discard(doc_id)
        self.doc_links.pop(doc_id, None)

        for source in self.doc_backlinks.get(doc_id, set()):
            self.doc_links[source].discard(doc_id)
        self.doc_backlinks.pop(doc_id, None)

        if self.documents:
            self.max_timestamp = max(d.timestamp for d in self.documents.values())
        else:
            self.max_timestamp = 0

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return TOKEN_PATTERN.findall(text.lower())
