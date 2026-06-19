import sys
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "datasets"))

from cyberdeck.analysis import add_review_signals, build_book_summary, radar_cards


class AnalysisTests(unittest.TestCase):
    def test_review_signals_flag_weak_unverified_review(self):
        reviews = pd.DataFrame(
            {
                "book name": ["Neon Pages", "Neon Pages"],
                "review title": ["Wow", "Detailed take"],
                "reviewer rating": [5, 4],
                "review description": ["Amazing!!!", "A thoughtful review with enough context to be useful."],
                "is_verified": [False, True],
            }
        )

        scored = add_review_signals(reviews)

        self.assertTrue(bool(scored.loc[0, "suspicious_flag"]))
        self.assertFalse(bool(scored.loc[1, "suspicious_flag"]))
        self.assertLess(scored.loc[0, "trust_score"], scored.loc[1, "trust_score"])

    def test_book_summary_merges_review_metrics(self):
        books = pd.DataFrame(
            {
                "book title": ["Neon Pages"],
                "book price": [10.0],
                "rating": [4.5],
                "author": ["A. Data"],
                "genre": ["Science Fiction"],
                "year of publication": [2024],
                "url": ["https://example.com"],
            }
        )
        reviews = add_review_signals(
            pd.DataFrame(
                {
                    "book name": ["Neon Pages"],
                    "review title": ["Detailed take"],
                    "reviewer rating": [5],
                    "review description": ["A useful and verified review with context."],
                    "is_verified": [True],
                }
            )
        )

        summary = build_book_summary(books, reviews)

        self.assertEqual(int(summary.loc[0, "reviews"]), 1)
        self.assertGreater(float(summary.loc[0, "trust_score"]), 70)
        self.assertIn("value_score", summary.columns)

    def test_radar_cards_returns_expected_slots(self):
        summary = pd.DataFrame(
            {
                "book title": ["A", "B"],
                "book price": [8.0, 20.0],
                "rating": [4.2, 4.9],
                "reviews": [2, 5],
                "verified_pct": [90.0, 80.0],
                "trust_score": [85.0, 92.0],
                "fragile_reviews": [0, 1],
                "rating_std": [0.1, 1.2],
                "value_score": [120.0, 115.0],
            }
        )

        cards = radar_cards(summary)

        self.assertEqual(set(cards), {
            "Melhor custo-benefício",
            "Mais confiável",
            "Mais comentado",
            "Mais controverso",
        })
        self.assertEqual(cards["Melhor custo-benefício"]["book title"], "A")


if __name__ == "__main__":
    unittest.main()
