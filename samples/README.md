# Sample responses

Example `200` responses for eight Aqar API endpoints, copied from the API's public
documentation. Long arrays are cut to their first few items, and advertiser fields (`user`,
`user_id`) are removed. Field names and values are otherwise unchanged.

| File | Request |
|---|---|
| `cities.json` | `GET /cities?category=1` |
| `districts.json` | `GET /districts?category=1&city_id=21` |
| `search.json` | `GET /search?category=1&city_id=21` |
| `listing-details.json` | `GET /listing-details` (listing 6702552) |
| `ai-search.json` | `GET /ai-search?query=...` (a 3-bedroom apartment for rent in Riyadh) |
| `reverse-geocode.json` | `GET /reverse-geocode?lat=24.7136&lng=46.6753` |
| `district-price-stats.json` | `GET /district-price-stats` (Riyadh) |
| `residential-indicators.json` | `GET /residential-indicators` (floors for rent, 3 rooms, An Narjis) |

They are useful for writing parsers and tests before you subscribe. Live data changes
daily, so do not hard-code these values.
