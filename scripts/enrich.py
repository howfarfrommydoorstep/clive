import json, pathlib, requests, time

SRC = pathlib.Path("hotels.json")          # raw input
DST = pathlib.Path("hotels_geocoded.json") # cache

raw  = json.loads(SRC.read_text())

# read existing geocoded hotel list (create empty list if none exists)
cache = json.loads(DST.read_text()) if DST.exists() else []

# build look-up dict by (lat,lon) to detect already-done hotels
done = {(h["Latitude"], h["Longitude"]): h for h in cache}

# we only geocode the diff, then merge and overwrite the cache
hotels_to_add = []
for h in raw:
    if (h["Latitude"], h["Longitude"]) not in done:
        hotels_to_add.append(h)
        done[(h["Latitude"], h["Longitude"])] = h   # placeholder till filled

print(f"Need to geocode: {len(hotels_to_add)} of {len(raw)}")

URL = "https://api.opencagedata.com/geocode/v1/json"
API_KEY = "efa8db539d804f4a93a6cffa3dfd6131"

# only loop over *new* hotels
for h in hotels_to_add:
    params = {"key": API_KEY,
              "q": f"{h['Latitude']},{h['Longitude']}",
              "pretty": 1}
    try:
        r = requests.get(URL, params=params, timeout=15)
        geo = r.json()["results"][0]
        h["Area"] = geo["components"].get("town") or geo["components"].get("city") or "-"
        h["Address"] = geo.get("formatted", "-")
    except Exception as e:
        h["Area"] = h["Address"] = "-"
    time.sleep(0.5)  # OpenCage is faster, 0.5 s still safe

# create output list in same order as raw file
output = [done[(h["Latitude"], h["Longitude"])] for h in raw]

DST.write_text(json.dumps(output, indent=2, ensure_ascii=False))
print("Geocoding complete for diff")
