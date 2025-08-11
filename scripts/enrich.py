#!/usr/bin/env python3
import json, pathlib, requests, time

SRC = pathlib.Path("hotels.json")
DST = pathlib.Path("hotels_geocoded.json")

hotels = json.loads(SRC.read_text(encoding="utf-8"))
URL = "https://api.opencagedata.com/geocode/v1/json"
API_KEY = "efa8db539d804f4a93a6cffa3dfd6131"

for h in hotels:
    params = {
        "key": API_KEY,
        "q": f"{h['Latitude']},{h['Longitude']}",
        "pretty": 1
    }
    try:
        r = requests.get(URL, params=params, timeout=15)
        if r.status_code != 200:
            h["Area"] = h["Address"] = "-"
            continue
        geo = r.json()["results"][0]
        h["Area"] = (
            geo["components"].get("town") or
            geo["components"].get("city") or "-"
        )
        h["Address"] = geo.get("formatted", "-")
    except Exception as e:
        h["Area"] = h["Address"] = "-"
        print("WARN", str(e))

DST.write_text(json.dumps(hotels, indent=2, ensure_ascii=False))
