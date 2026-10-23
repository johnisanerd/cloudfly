"""Offline tests for the Google Maps Apify input mapping."""

from __future__ import annotations

import unittest

from app.infrastructure.repositories.maps_adapter import (
    build_maps_actor_input,
    is_notice_row,
)


class BuildMapsActorInputTests(unittest.TestCase):
    """Cover johnvc input vs the previous compass-style payload."""

    def test_live_maps_actor_uses_search_terms(self) -> None:
        """johnvc/google-maps-places-api takes searchTerms and a 20-place floor."""
        payload = build_maps_actor_input(
            "johnvc/google-maps-places-api", "cafe in Bogota", 5
        )
        self.assertEqual(payload["searchTerms"], ["cafe in Bogota"])
        self.assertEqual(payload["maxResultsPerSearch"], 20)
        self.assertNotIn("searchStringsArray", payload)

    def test_search_scraper_keeps_query_input(self) -> None:
        """google-search-scraper still uses queries / resultsPerPage."""
        payload = build_maps_actor_input("apify/google-search-scraper", "cafe", 10)
        self.assertEqual(payload["queries"], "cafe")
        self.assertEqual(payload["resultsPerPage"], 10)


class NoticeRowTests(unittest.TestCase):
    """Free-tier notice rows are not leads."""

    def test_notice_row(self) -> None:
        """A free_tier_notice flag drops the row."""
        self.assertTrue(is_notice_row({"free_tier_notice": True}))
        self.assertFalse(is_notice_row({"title": "Cafe"}))


if __name__ == "__main__":
    unittest.main()
