# Aqar API and Scraper

The Aqar API returns Saudi Arabia property listings from Aqar (sa.aqar.fm) as JSON:
apartments, villas, land, floors and commercial property for sale and rent, with prices in
SAR, area in m2, district and city IDs with Arabic and English names, plus natural-language
search, district price history, district ratings and developer projects. Aqar does not
publish a public developer API for its listings, so this REST API is the way to use its data
in your own code without maintaining an Aqar scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/aqar-api?utm_source=github&utm_medium=readme&utm_campaign=aqar-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/aqar
- Product page: https://happyendpoint.com/library/aqar-api?utm_source=github&utm_medium=readme&utm_campaign=aqar-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://aqar.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 23, all `GET` |
| Coverage | Saudi Arabia: admin regions, cities, city directions (zones) and districts |
| Languages | Arabic and English names for cities, directions and districts; search queries in either |
| Currency and units | Prices in SAR, area in m2 |
| Page size | Up to 50 listings per call, offset pagination with `from` |
| Format | JSON, every response wrapped in `{"success": true, "data": {...}}` |

---

## What data you get

**Search**
- Listing search by category, city, direction, district or province, with filters for price, area, price per m2, bedrooms, rooms, living rooms, bathrooms, building age, rent period, furnished, video, REGA-verified and premium
- Nine sort orders, including newest, refreshed, price, area and price per m2
- AI search: a plain-language query in Arabic or English turned into filters, with the parsed filters returned
- Related listings, location autocomplete and place bounding boxes

**Listings**
- Price, area, bedrooms, rooms, living rooms, bathrooms, building age, floor, furnished and verified flags
- Coordinates, city, direction and district IDs, image URLs in several sizes
- Full records: Arabic address and description, REGA ad licence number, view count, the listing's Aqar URL slug
- Look up a listing by ID or by its Aqar URL

**Locations and reference data**
- Admin regions, cities and districts with listing counts per category, city directions (north, east and so on)
- Reverse geocoding from coordinates to city, direction and district IDs with Arabic and English names and the district's rating
- The category list (ID to name) and the Ministry of Justice category mapping

**Market data**
- Half-yearly district price history for a city and category
- The latest residential price indicator for a district, category and room-count bucket
- District ratings with sub-scores for utilities, internet, streets, medical and education services

**Developers and projects**
- Off-plan and ready projects with price range, area range, status and location
- Developer profiles and their project lists, and cities ranked by project count

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/aqar). Current plans are listed there. Copy `.env.example` to `.env` and paste your key.

### 2. Make a request

Searches take numeric IDs. Get the district IDs for a city and category first:

```bash
curl "https://aqar.p.rapidapi.com/districts?category=1&city_id=21" \
  -H "x-rapidapi-host: aqar.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"

curl "https://aqar.p.rapidapi.com/search?category=1&city_id=21&district_id=600&sort=newest&size=20" \
  -H "x-rapidapi-host: aqar.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

`category=1` is apartments for rent and `city_id=21` is Riyadh.

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py
```

```python
from client import get

districts = get("/districts", category=1, city_id=21)["districts"]
results = get("/search", category=1, city_id=21, district_id=districts[0]["district_id"])
for row in results["listings"]:
    print(row["id"], row["price"], "SAR", row["area"], "m2")
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs
```

---

## Example response

`GET /search?category=1&city_id=21`, trimmed to one listing. Values are the example in the
API's public documentation. The full responses are in [`samples/`](samples/).

```json
{
  "success": true,
  "data": {
    "total": 21849,
    "listings": [
      {
        "id": 6702552,
        "category": 1,
        "city_id": 21,
        "district_id": 548,
        "direction_id": 4,
        "price": 40000,
        "meter_price": null,
        "area": 70,
        "beds": 1,
        "rooms": 1,
        "livings": 1,
        "wc": 1,
        "age": 0,
        "furnished": 1,
        "verified": 1,
        "premium": 0,
        "last_update": 1780245614,
        "location": { "lat": 24.757247, "lng": 46.661992 },
        "images": [
          {
            "thumbnail": "https://images.aqar.fm/webp/200x200/props/048729072_1779133329415.jpg",
            "full": "https://images.aqar.fm/webp/original/props/048729072_1779133329415.jpg"
          }
        ]
      }
    ]
  }
}
```

---

## Endpoints

Base URL: `https://aqar.p.rapidapi.com`

### Search

| Endpoint | Returns |
|---|---|
| `GET /search` | Listings matching category, location and filters |
| `GET /ai-search` | Listings for a plain-language query, with the filters it was parsed into |
| `GET /related-listings` | Listings similar to one listing |
| `GET /autocomplete` | Place suggestions for typed text, each with a `place_id` |
| `GET /place-bounds` | The bounding box of a `place_id` |

### Listings

| Endpoint | Returns |
|---|---|
| `GET /listing-details` | The full listing by ID |
| `GET /listing-details-by-url` | The full listing from an Aqar listing URL or slug |
| `GET /listing-views` | A listing's total view count |

### Locations and reference data

| Endpoint | Returns |
|---|---|
| `GET /categories` | Category IDs and names, in Arabic or English |
| `GET /admin-regions` | Saudi provinces |
| `GET /cities` | Cities with listing counts for a category |
| `GET /directions` | A city's zones (north, south, east, west, center) with counts |
| `GET /districts` | A city's districts with counts, in Arabic and English |
| `GET /reverse-geocode` | City, direction and district for a coordinate |
| `GET /moj-categories` | Ministry of Justice category mapping |

### Market data

| Endpoint | Returns |
|---|---|
| `GET /district-price-stats` | Half-yearly price and count history per district |
| `GET /residential-indicators` | Latest average price for a district, category and room-count bucket |
| `GET /district-rating` | District rating, service sub-scores and resident comments |

### Developers and projects

| Endpoint | Returns |
|---|---|
| `GET /project-details` | One off-plan or ready project |
| `GET /developer-details` | A developer's profile |
| `GET /developer-projects` | A developer's projects, filterable by status and type |
| `GET /projects-by-city` | Cities ranked by project count |
| `GET /status` | Service health |

---

## Things to know about the data

These are the details that give wrong numbers rather than errors.

- **The category ID carries the deal type.** Apartments for rent are `1`, apartments for sale
  are `6`; villas for sale are `3` and villas for rent `5`. There is no separate "rent or
  sale" filter, so a city's counts and price history change completely with `category`. Get
  the full list from `/categories`.
- **Rental prices are per rent period, and the period can be missing.** Each row carries
  `rent_period` (the documentation gives `1` for daily up to `3` for yearly), but on live
  rows it is sometimes `null`. In one Riyadh apartment search we ran, a null row was 3,800
  SAR for 150 m2, next to yearly rents of 45,000 to 105,000 SAR. Pass `rent_period=3` (or
  drop nulls) before you take a median. `district_prices.py` takes `--rent-period`, and
  `quickstart.py` prints the period of each row.
- **`meter_price` is often null.** It is null on the documented apartment example. Divide
  `price` by `area` yourself where both are present (`client.price_per_m2()`), and remember
  that on a rental the result is SAR per m2 per rent period.
- **Join on IDs, never on names.** The same district is `حي النرجس` in `/districts` (with the
  "district" prefix), plain names elsewhere (`الورود` in `/reverse-geocode`, `اشبيلية` in
  `/district-price-stats`), and only `/districts`, `/cities`, `/directions` and
  `/reverse-geocode` add an English `name_en`. `district_id` is the stable key.
- **`place_id` is not a district ID.** `/autocomplete` returns map place IDs for
  `/place-bounds` only. For searches, take `district_id` from `/districts` or from
  `/reverse-geocode` on a coordinate.
- **`last_update` is a Unix timestamp in seconds**, and flags such as `furnished`,
  `verified` and `premium` are `0` or `1`, not booleans.
- **The two price series measure different things.** `/district-price-stats` is a
  half-yearly history (`time_range` `"1-2015"` is the first half of 2015) with a `count` per
  period, and has data mainly for sale categories; it returns an empty list when a category
  has no series. `/residential-indicators` is a single latest average for one district,
  category and room-count bucket (`size` `"0"` to `"5"`, required for most categories, omitted
  for land). Its `message_en` still embeds the Arabic district name.
- **AI search shows its working.** `/ai-search` returns `parsed_query` (category, city,
  district, beds, price and area bounds) and a `confidence`. Check it before trusting the
  results, and fall back to `/search` with explicit IDs when it guessed wrong.
- **Paging is by offset.** `size` is 1 to 50 and `from` is the number of results to skip.

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | Districts of a city, the newest listings in the busiest one, one full listing |
| [`examples/python/district_prices.py`](examples/python/district_prices.py) | Median asking price and SAR per m2 for a city's busiest districts, to CSV |
| [`examples/python/ai_search.py`](examples/python/ai_search.py) | Plain-language search in Arabic or English, printing the parsed filters |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | The quickstart in Node 18+, no dependencies |
| [`samples/`](samples/) | Documented example responses for eight endpoints |

The CSV is written as UTF-8 with a byte order mark, so Excel shows the Arabic district names
correctly.

---

## API or your own Aqar scraper

A homemade Aqar scraper has to keep up with the site's pages, IDs and anti-bot rules, and
breaks when any of them change. This API returns the same listings and reference data as
documented JSON with a stable contract, so the code you keep is the analysis. If you need a
one-off file or a recurring export rather than API calls,
[contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=aqar-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can query Aqar listings
without code:

```json
{
  "mcpServers": {
    "aqar": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: aqar.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Is there an Aqar API?

Aqar does not publish a public developer API for its listings. This API, built and
maintained by Happy Endpoint and independent of Aqar, provides that access as REST and JSON.

### Where is the Aqar API documentation?

Every endpoint, parameter and response is documented on the
[RapidAPI listing](https://rapidapi.com/happyendpoint/api/aqar), and the endpoint table
above summarises them. Example responses are in [`samples/`](samples/).

### Is there a free Aqar API?

Yes. The RapidAPI listing has a free plan, and every endpoint can be tried on it.

### Can I get Aqar data in English?

Partly. City, direction and district names come in Arabic and English, `/categories` takes
`lang=en`, and `/ai-search` accepts English queries. Listing addresses and descriptions are
the advertiser's own text, usually Arabic.

### How do I scrape Aqar listings in Python?

Install `requests`, set `RAPIDAPI_KEY`, and call the endpoints with the two RapidAPI
headers. [`examples/python/client.py`](examples/python/client.py) is the client, and the
other scripts in that folder are ready to run.

### Can I get price per square meter by district in Riyadh?

Yes. Search a district with `category` and `city_id=21` and divide price by area, or sort and
filter with `meter_price_min`, `meter_price_max` and `sort=meter_price_low_to_high`.
[`district_prices.py`](examples/python/district_prices.py) builds the comparison for a
whole city. For history, `/district-price-stats` returns a half-yearly series per district.

### Can I filter to REGA-verified listings only?

Yes. Pass `verified=true` to `/search`. Full listing records also carry the
`ad_license_number`.

### Do you cover other Saudi and Gulf property sites?

Yes, including Wasalt in Saudi Arabia and Bayut and PropertyFinder in the UAE. See the
[API library](https://happyendpoint.com/library?utm_source=github&utm_medium=readme&utm_campaign=aqar-api).

---

## Related repos

- [wasalt-api](https://github.com/happyendpointhq/wasalt-api) - Saudi property listings, REGA licences, holiday rentals and Infath auctions from Wasalt
- [awesome-real-estate-apis](https://github.com/happyendpointhq/awesome-real-estate-apis) - real estate APIs and data sources by country, including free and official ones
- [fotocasa-api](https://github.com/happyendpointhq/fotocasa-api) - Spanish property listings for sale and rent, prices and district counts
- [uae-real-estate-data-guide](https://github.com/happyendpointhq/uae-real-estate-data-guide) - how to get UAE and Dubai property data programmatically
- [bayut-api](https://github.com/happyendpointhq/bayut-api) - UAE property listings, agents, agencies and transactions

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: happyendpointhq@gmail.com

## Licence

MIT. See [LICENSE](LICENSE).
