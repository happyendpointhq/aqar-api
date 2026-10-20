"""Search Aqar with a plain-language query in Arabic or English.

    python ai_search.py "3 bedroom apartment for rent in Riyadh"
    python ai_search.py "شقة للايجار في الرياض ثلاث غرف"

Prints the filters the API understood (`parsed_query`) before the results, so you can check
the interpretation and fall back to /search with explicit filters when it is wrong.
"""

import sys

from client import get

query = " ".join(sys.argv[1:]) or "3 bedroom apartment for rent in Riyadh"
data = get("/ai-search", query=query, size=10)

parsed = data["parsed_query"]
print(f"Understood (confidence {data.get('confidence')}):")
for key, value in parsed.items():
    if value is not None:
        print(f"  {key}: {value}")

print(f"\n{data['total']} matching listings")
for row in data["listings"]:
    print(f"{row['id']}  {row['price']:>10,} SAR  {row.get('area') or '?'} m2  {row.get('beds')} beds")
