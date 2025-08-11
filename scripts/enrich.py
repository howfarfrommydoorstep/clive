import json, pathlib, requests, time, os  # << added os

SRC = pathlib.Path("hotels.json")
DST = pathlib.Path("hotels_geocoded.json")

raw  = json.loads(SRC.read_text())

# existing cache
cache = json.loads(DST.read_text()) if DST.exists() else []
done = {(h["Latitude"], h["Longitude"]): h for h in cache}

hotels_to_add = []
for h in raw:
    key = (h["Latitude"], h["Longitude"])
    if key not in done:
        hotels_to_add.append(h)
        done[key] = h   # placeholder
print(f"Need to geocode: {len(hotels_to_add)} of {len(raw)}")

URL = "https://api.opencagedata.com/geocode/v1/json"
API_KEY = os.environ["OPENCAGE_KEY"]          # << brackets, not quotes

for h in hotels_to_add:
    params = {"key": API_KEY,
              "q": f"{h['Latitude']},{h['Longitude']}",
              "pretty": 1}
    try:
        r = requests.get(URL, params=params, timeout=15)
        r.raise_for_status()
        geo = r.json()["results"][0]
        h["Area"]    = geo["components"].get("town") or geo["components"].get("city") or "-"
        h["Address"] = geo.get("formatted", "-")
    except Exception as e:
        h["Area"] = h["Address"] = "-"
    time.sleep(0.5)

output = [done[(h["Latitude"], h["Longitude"])] for h in raw]
DST.write_text(json.dumps(output, indent=2, ensure_ascii=False))
print("Geocoding complete for diff")
