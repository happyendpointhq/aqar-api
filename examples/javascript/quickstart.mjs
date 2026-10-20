// Aqar API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs

const HOST = 'aqar.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`Aqar API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

// Riyadh (city_id 21), apartments for rent (category 1).
const { districts } = await get('/districts', { category: 1, city_id: 21 });
const district = districts[0];
console.log(`Busiest district: ${district.name_en} (${district.name}), ${district.count} listings`);

const results = await get('/search', {
  category: 1,
  city_id: 21,
  district_id: district.district_id,
  sort: 'newest',
  size: 10,
});
console.log(`${results.total} listings`);
for (const row of results.listings) {
  const updated = new Date(row.last_update * 1000).toISOString().slice(0, 10);
  console.log(`${row.id}  ${row.price.toLocaleString()} SAR  ${row.area ?? '?'} m2  updated ${updated}`);
}
