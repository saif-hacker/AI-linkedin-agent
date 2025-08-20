import json, re
from pathlib import Path
from services.datasources.base import write_jsonl
from services.nlp.nlp_utils import analyze_texts

def analyze_profiles(inp: str = "data/profiles.jsonl", out: str = "data/enriched.jsonl"):
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    enriched = []
    with open(inp, "r", encoding="utf-8") as f:
        for line in f:
            p = json.loads(line)
            texts = [t for t in [p.get("about"), p.get("headline")] if t]
            topics, entities = analyze_texts(texts)
            p["topics"] = topics
            p["entities"] = entities
            enriched.append(p)
    write_jsonl(out, enriched)
    print(f"[analyzer] Enriched {len(enriched)} profiles → {out}")
