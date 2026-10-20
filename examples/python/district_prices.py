"""Compare asking prices across a city's districts and write a CSV.

    python district_prices.py --city-id 21 --category 6 --districts 15 --out riyadh.csv

For each of the busiest districts, pulls up to 50 current listings and reports the median
asking price and median SAR per m2. For rentals, pass --rent-period (3 = yearly) so you do
not mix daily, monthly and yearly prices in one median.
"""

import argparse
import csv
from statistics import median

from client import get, price_per_m2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--city-id", type=int, default=21, help="21 Riyadh, 66 Jeddah, 18 Dammam")
    parser.add_argument("--category", type=int, default=6, help="see /categories; 6 = apartment for sale")
    parser.add_argument("--rent-period", type=int, help="rental categories only: 1 daily ... 3 yearly")
    parser.add_argument("--districts", type=int, default=15, help="how many of the busiest districts")
    parser.add_argument("--out", default="district_prices.csv")
    args = parser.parse_args()

    districts = get("/districts", category=args.category, city_id=args.city_id)["districts"]
    districts = sorted(districts, key=lambda d: d["count"], reverse=True)[: args.districts]

    rows = []
    for d in districts:
        data = get(
            "/search",
            category=args.category,
            city_id=args.city_id,
            district_id=d["district_id"],
            rent_period=args.rent_period,
            size=50,
        )
        prices = [l["price"] for l in data["listings"] if l.get("price")]
        per_m2 = [p for p in map(price_per_m2, data["listings"]) if p]
        rows.append({
            "district_id": d["district_id"],
            "district_en": d["name_en"],
            "district_ar": d["name"],
            "listings_total": data["total"],
            "sampled": len(prices),
            "median_price_sar": round(median(prices)) if prices else None,
            "median_sar_per_m2": round(median(per_m2)) if per_m2 else None,
        })
        print(f"{d['name_en']:<22} {rows[-1]['median_price_sar']} SAR, {rows[-1]['median_sar_per_m2']} SAR/m2")

    with open(args.out, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["district_id"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} districts to {args.out}")


if __name__ == "__main__":
    main()
