import json, time
from services.utils.rate_limiter import token_bucket
from services.datasources.base import read_jsonl
from services.datasources.phantombuster import send_via_phantombuster
from services.datasources.playwright_linkedin import send_with_playwright

def _prompt_approval(item):
    print("\n--- Preview -------------------------------------------------")
    print(f"Name: {item['name']}\nURL : {item['profile_url']}\nMsg : {item['message']}")
    ans = input("Send this message? [y/N] ").strip().lower()
    return ans == "y"

def dispatch_outreach(adapter: str = "manual", batch: str = "data/outbox.jsonl", require_approval: bool = True):
    items = list(read_jsonl(batch))
    print(f"[outreach] Loaded {len(items)} messages")

    # limit to safe pace: 1/10s (adjust as needed; respect platform limits)
    allow = token_bucket(rate_per_sec=0.1, capacity=3)

    sent = 0
    for item in items:
        if require_approval and not _prompt_approval(item):
            print("[outreach] Skipped")
            continue

        next(allow)  # rate-limit
        if adapter == "manual":
            print("[outreach] Manual mode — please send this message in the UI.")
        elif adapter == "phantombuster":
            send_via_phantombuster(item)
        elif adapter == "playwright":
            send_with_playwright(item)
        else:
            raise ValueError("Unknown adapter")
        sent += 1
    print(f"[outreach] Completed. Sent/Queued: {sent}")
