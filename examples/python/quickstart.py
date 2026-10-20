"""Pick a city and district, search it, then open the first listing.

    python quickstart.py            # Riyadh, apartments for rent
    python quickstart.py 66 6       # Jeddah, apartments for sale

Arguments: city_id (from /cities) and category (from /categories; 1 = apartment for rent,
6 = apartment for sale, 3 = villa for sale, 2 = land for sale).
"""

import sys

from client import get, price_per_m2, updated_at

# rent_period codes from the documentation; live rows are sometimes null (period unknown).
PERIODS = {1: "daily", 3: "yearly", None: "period ?"}

city_id = int(sys.argv[1]) if len(sys.argv) > 1 else 21
category = int(sys.argv[2]) if len(sys.argv) > 2 else 1

# 1. Districts in the city, with their listing counts for this category. Names come in
#    Arabic (`name`) and English (`name_en`); searches take the numeric district_id.
districts = get("/districts", category=category, city_id=city_id)["districts"]
for d in districts[:5]:
    print(f"{d['district_id']:>6}  {d['name_en']:<20} {d['name']}  {d['count']} listings")
if not districts:
    raise SystemExit("No districts for that city and category")
district = districts[0]

# 2. Newest listings in the busiest district.
results = get(
    "/search",
    category=category,
    city_id=city_id,
    district_id=district["district_id"],
    sort="newest",
    size=10,
)
print(f"\n{results['total']} listings in {district['name_en']}, showing {len(results['listings'])}")
# Sale listings carry no period; only label periods when this is a rental search.
is_rental = any(row.get("rent_period") for row in results["listings"])
for row in results["listings"]:
    period = PERIODS.get(row.get("rent_period"), "") if is_rental else ""
    per_m2 = price_per_m2(row)
    per_m2_text = f"{per_m2:,} SAR/m2" if per_m2 else ""
    print(
        f"{row['id']}  {row['price']:>10,} SAR  {row.get('area') or '?':>5} m2  "
        f"{row.get('beds') or 0} beds  {per_m2_text:<14} {period:<8} "
        f"updated {updated_at(row):%Y-%m-%d}"
    )

# 3. Full record for the first listing: address, description, REGA ad licence, views.
if results["listings"]:
    listing = get("/listing-details", listing_id=results["listings"][0]["id"])
    print(f"\n{listing['address']}")
    print(f"Floor {listing.get('fl')}, {listing.get('views')} views, ad licence {listing.get('ad_license_number')}")
    print(f"https://sa.aqar.fm/{listing['uri']}")
