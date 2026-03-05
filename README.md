# re-pricing-sreality

Weekly scraper for **Sreality.cz** listing fees (Czech Republic).

## Platform

Sreality is the Czech Republic's leading real estate portal, operated by Seznam.cz.

## Pricing Model

**Per-day fee per listing**, with volume discounts for larger agencies:

| Tier | Portfolio Size | Fee (CZK/day/listing) |
|------|---------------|----------------------|
| Small | 1–49 listings | CZK 15 |
| Medium | 50–999 listings | CZK 12 |
| Large | 1000+ listings | CZK 9 |

- `fee_period = per_day`
- `currency = CZK`
- All prices **excluding** 21% Czech VAT
- Multiply × 30 for approximate monthly cost per listing

Source: [o-seznam.cz Sreality pricing](https://o-seznam.cz/napoveda/sreality/cenik-sluzeb/)

## Output

`data/pricing.csv` — 3 rows per scrape date, one per volume tier.

## Running Locally

```bash
pip install -r requirements.txt
python scraper.py
```
