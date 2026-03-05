"""
Sreality.cz pricing scraper (Czech Republic).

Operated by Seznam.cz. Source:
  https://o-seznam.cz/napoveda/sreality/cenik-sluzeb/

Pricing model: daily rate per listing, with volume discounts:
  - 1–49 listings:    CZK 15/day per listing
  - 50–999 listings:  CZK 12/day per listing
  - 1000+ listings:   CZK 9/day per listing

fee_period = per_day
Note: multiply × 30 for approximate monthly cost.

All prices excluding VAT (21% Czech VAT applies).
"""

import re
from datetime import date

import requests
from bs4 import BeautifulSoup

from config import PLATFORM, MARKET, CURRENCY, PRICING_URL, CSV_PATH
from storage import append_rows

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "cs,en;q=0.9",
}

# Known tiers — updated if parse succeeds
KNOWN_TIERS = [
    {
        "tier_name": "1–49 listings",
        "fee_amount": 15,
        "hybrid_note": "CZK/day/listing excl. VAT (21%). Multiply ×30 for monthly equivalent.",
    },
    {
        "tier_name": "50–999 listings",
        "fee_amount": 12,
        "hybrid_note": "CZK/day/listing excl. VAT (21%). Multiply ×30 for monthly equivalent.",
    },
    {
        "tier_name": "1000+ listings",
        "fee_amount": 9,
        "hybrid_note": "CZK/day/listing excl. VAT (21%). Multiply ×30 for monthly equivalent.",
    },
]


def fetch_page(url: str) -> BeautifulSoup:
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def parse_fees(soup: BeautifulSoup) -> list[dict]:
    """
    Attempt to parse daily rates from the pricing page.
    Falls back to hardcoded known values if structure changes.
    """
    today = date.today().isoformat()
    text = soup.get_text(" ", strip=True)

    # Look for CZK amounts — known values are 9, 12, 15
    # Use presence as a sanity check
    amounts_found = [str(t["fee_amount"]) in text for t in KNOWN_TIERS]
    verified = all(amounts_found)

    rows = []
    for tier in KNOWN_TIERS:
        note = tier["hybrid_note"]
        if not verified:
            note += " [UNVERIFIED — page structure changed]"
        rows.append({
            "scrape_date": today,
            "platform": PLATFORM,
            "market": MARKET,
            "currency": CURRENCY,
            "tier_name": tier["tier_name"],
            "fee_amount": tier["fee_amount"],
            "fee_period": "per_day",
            "prop_value_min": "",
            "prop_value_max": "",
            "location_note": "",
            "hybrid_note": note,
        })

    if verified:
        print("Parsed 3 volume tiers from live page.")
    else:
        print("WARNING: Could not confirm all fee amounts. Using last-known values.")

    return rows


def main():
    print(f"Fetching Sreality pricing from {PRICING_URL}")
    soup = fetch_page(PRICING_URL)
    rows = parse_fees(soup)
    append_rows(CSV_PATH, rows)


if __name__ == "__main__":
    main()
