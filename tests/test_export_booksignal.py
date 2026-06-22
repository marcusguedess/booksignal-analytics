import json
import unittest
from pathlib import Path

from analytics.export_booksignal import OUTPUT, main, normalize_genre


class ExportBookSignalTests(unittest.TestCase):
    def test_normalize_genre_maps_messy_labels_to_product_buckets(self):
        cases = {
            "Fantasy, Romance, Young Adult": "Young Adult",
            "Picture Books, Childrens, Fiction": "Children",
            "Finance, Nonfiction, Business": "Business",
            "Unknown niche label": "Other",
        }

        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(normalize_genre(raw), expected)

    def test_export_writes_minimum_dashboard_contract(self):
        main()
        payload = json.loads(Path(OUTPUT).read_text(encoding="utf-8"))

        self.assertIn("metrics", payload)
        self.assertIn("dataQuality", payload)
        self.assertIn("books", payload)
        self.assertIn("scoreBreakdown", payload["books"][0])
        self.assertGreater(payload["metrics"]["books"], 0)
        self.assertGreater(payload["dataQuality"]["completeness"], 0)

    def test_export_matches_frontend_contract(self):
        main()
        payload = json.loads(Path(OUTPUT).read_text(encoding="utf-8"))

        required_top_level = {
            "generatedAt",
            "sources",
            "metrics",
            "summary",
            "dataQuality",
            "opportunityCards",
            "books",
            "genres",
            "ratingDistribution",
            "trustDistribution",
            "recentReviews",
        }
        self.assertTrue(required_top_level.issubset(payload))

        required_book_fields = {
            "title",
            "author",
            "genre",
            "rawGenre",
            "price",
            "rating",
            "reviews",
            "verifiedPct",
            "qualityScore",
            "reviewsToAudit",
            "valueScore",
            "ratingStd",
            "scoreBreakdown",
            "genreBenchmark",
        }
        self.assertTrue(required_book_fields.issubset(payload["books"][0]))

        required_breakdown_fields = {"rating", "price", "reviewQuality", "evidence"}
        self.assertTrue(required_breakdown_fields.issubset(payload["books"][0]["scoreBreakdown"]))

        required_quality_fields = {
            "completeness",
            "emptyCells",
            "duplicates",
            "genreBuckets",
            "rawGenreLabels",
            "tables",
        }
        self.assertTrue(required_quality_fields.issubset(payload["dataQuality"]))


if __name__ == "__main__":
    unittest.main()
