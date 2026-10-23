"""Map Google Maps Actor input/output onto this app's field names."""

from typing import Any, Dict


def build_maps_actor_input(actor_id: str, query: str, limit: int) -> Dict[str, Any]:
    """Build Apify run input for the configured Maps or Search Actor.

    Args:
        actor_id: Store slug from the actors map (slash or tilde form).
        query: Combined keyword-plus-location search string.
        limit: Requested place cap.

    Returns:
        Actor input matching johnvc/google-maps-places-api, the search
        scraper, or the legacy compass-style payload.
    """
    normalized = actor_id.replace("~", "/")
    if "google-search-scraper" in normalized:
        return {
            "queries": query,
            "maxPagesPerQuery": 1,
            "resultsPerPage": limit,
            "mobileResults": False,
        }
    if "google-maps-places-api" in normalized:
        return {
            "searchTerms": [query],
            "maxResultsPerSearch": max(20, int(limit) if limit else 20),
            "language": "en",
        }
    return {
        "searchStringsArray": [query],
        "maxItems": limit,
    }


def is_notice_row(item: Dict[str, Any]) -> bool:
    """Return True when a dataset row is a free-tier notice, not a place.

    Args:
        item: One dataset row from the Actor run.

    Returns:
        True if the row should be dropped before Lead mapping.
    """
    return bool(item.get("free_tier_notice"))
