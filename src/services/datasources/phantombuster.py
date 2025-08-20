# Connector for PhantomBuster (optional, requires API key & phantom setup).
# Docs: https://phantombuster.com/
import os, requests
from typing import List
from .base import Profile

API = "https://api.phantombuster.com/api/v2"
KEY = os.getenv("PHANTOMBUSTER_API_KEY")

def fetch_from_phantombuster(limit: int = 50) -> List[Profile]:
    if not KEY:
        print("[phantombuster] Missing PHANTOMBUSTER_API_KEY; returning empty list.")
        return []
    # Placeholder: fetch from your configured Phantom (e.g., LinkedIn Network Booster export)
    # resp = requests.get(f"{API}/agents/fetch-output?agentId=YOUR_AGENT_ID", headers={"X-Phantombuster-Key-1": KEY})
    # data = resp.json()
    data = []  # Replace with real response parsing
    out = []
    for i, item in enumerate(data[:limit]):
        out.append(Profile(name=item["firstName"]+" "+item["lastName"], headline=item.get("headline"), about=item.get("summary"), recent_posts=[], profile_url=item.get("profileUrl")))
    return out

def send_via_phantombuster(item: dict):
    if not KEY:
        print("[phantombuster] Missing API key; cannot send.")
        return
    # Placeholder for sending via a phantom that supports auto-connect
    print(f"[phantombuster] Would send to {item['name']} at {item['profile_url']} with message: {item['message'][:80]}...")
