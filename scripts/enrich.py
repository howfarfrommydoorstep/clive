#!/usr/bin/env python3
import json, pathlib, requests, time

SRC = pathlib.Path("hotels.json")
DST = pathlib.Path("hotels_geocoded.json")

hotels = json.loads(SRC.read_text(encoding='utf-8'))
URL = "https://nominatim.openstreetmap.org/reverse"

for h in hotels:
    params = {"format": "jsonv2", "lat": h["Latitude"], "lon": h["Longitude"]}
    reply = requests.get(URL, params=params, timeout=15).json()
    h["Area"] = reply.get("address", {}).get("city") or \
                reply.get("address", {}).get("town")  or \
                reply.get("address", {}).get("village") or "-"
    h["Address"] = reply.get("display_name", "-")
    time.sleep(1.2)        # stay under Nominatim limits

DST.write_text(json.dumps(hotels, indent=2, ensure_ascii=False))
