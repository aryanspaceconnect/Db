import unittest

from src.omniweave_db import Document, OmniWeaveDB


class OmniWeaveDBTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db = OmniWeaveDB()
        self.db.ingest(
            Document(
                doc_id="doc-1",
                title="Unified search fabric",
                text="Search ranking combines terms meaning and links",
                links=["doc-2"],
                entities=["search_engine", "ranking"],
                timestamp=1000,
                authority=0.9,
            )
        )
        self.db.ingest(
            Document(
                doc_id="doc-2",
                title="Meaning graph",
                text="Graph relations improve semantic retrieval",
                links=[],
                entities=["semantic_search"],
                timestamp=1100,
                authority=0.7,
            )
        )

    def test_query_returns_ranked_results(self) -> None:
        results = self.db.query("search meaning")
        self.assertGreaterEqual(len(results), 2)
        self.assertEqual(results[0][0], "doc-1")

    def test_neighbor_expansion_exposes_linked_docs(self) -> None:
        results = self.db.query("ranking", top_k=5)
        ranked_ids = [doc_id for doc_id, _ in results]
        self.assertIn("doc-2", ranked_ids)

    def test_related_terms(self) -> None:
        related = self.db.related_terms("search", top_k=10)
        related_terms = {term for term, _ in related}
        self.assertIn("ranking", related_terms)

    def test_document_update_replaces_previous_content(self) -> None:
        self.db.ingest(
            Document(
                doc_id="doc-1",
                title="Completely different",
                text="quantum storage field",
                links=[],
                entities=["quantum"],
                timestamp=1200,
                authority=0.5,
            )
        )
        results = self.db.query("search")
        ids = [doc_id for doc_id, _ in results]
        self.assertNotIn("doc-1", ids)


if __name__ == "__main__":
    unittest.main()
