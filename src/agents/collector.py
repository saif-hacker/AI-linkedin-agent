import json
from pathlib import Path
from services.datasources.base import write_jsonl
from services.datasources.manual_csv import fetch_from_csv
from services.datasources.phantombuster import fetch_from_phantombuster
from services.datasources.playwright_linkedin import fetch_with_playwright
from services.datasources.collector_selenium import collect_from_selenium


def collect_profiles(source: str = "csv", limit: int = 50, out_path: str = "data/profiles.jsonl"):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    if source == "csv":
        profiles = fetch_from_csv("data/new_connections.csv", limit=limit)
    elif source == "phantombuster":
        profiles = fetch_from_phantombuster(limit=limit)
    elif source == "playwright":
        profiles = fetch_with_playwright(limit=limit)
    elif source == "selenium":
        profiles = collect_from_selenium(limit=limit, out_path=out_path)
    else:
        raise ValueError(f"Unknown source: {source}")

    # If Selenium already wrote to file, avoid double-writing
    if source != "selenium":
        write_jsonl(out_path, [p.model_dump() for p in profiles])

    print(f"[collector] Wrote {len(profiles)} profiles → {out_path}")
    return profiles
