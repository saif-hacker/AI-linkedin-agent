import csv
from typing import List
from .base import Profile

def fetch_from_csv(csv_path: str, limit: int = 50) -> List[Profile]:
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for i, r in enumerate(csv.DictReader(f)):
            if i >= limit: break
            rows.append(Profile(
                name=r.get("name") or "Unknown",
                headline=r.get("headline") or None,
                about=r.get("about") or None,
                recent_posts=[p.strip() for p in (r.get("recent_posts") or "").split("||") if p.strip()],
                profile_url=r.get("profile_url") or None,
            ))
    return rows
