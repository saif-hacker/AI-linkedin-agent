import json
from pathlib import Path
from jinja2 import Template
from services.llm.openai_llm import llm_generate

TEMPLATE = Template(
    "Hi {{ name.split(' ')[0] }}, loved your work {{ hook }}. "
    "Would value a connection to swap insights on {{ topic }}. — {{ sender }}"
)

def _choose_hook(p):
    if p.get("recent_posts"):
        return f"on '{p['recent_posts'][0]}'"
    if p.get("about"):
        return "in your About summary"
    if p.get("headline"):
        return f"as {p['headline']}"
    return "recently"

def generate_messages(inp: str = "data/enriched.jsonl", out: str = "data/outbox.jsonl", model: str = "template", sender: str = "Saif"):
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    out_lines = []
    with open(inp, "r", encoding="utf-8") as f:
        for line in f:
            p = json.loads(line)
            topic = (p.get("topics") or ["your work"])[0]
            hook = _choose_hook(p)
            if model == "openai":
                prompt = f"Write a 280-char LinkedIn connection note for {p.get('name')} ({p.get('headline')}). Reference {hook} and topic {topic}. Friendly, concise."
                message = llm_generate(prompt)
            else:
                message = TEMPLATE.render(name=p.get("name","there"), hook=hook, topic=topic, sender=sender)
            out_lines.append({"profile_url": p.get("profile_url"), "name": p.get("name"), "message": message})

    with open(out, "w", encoding="utf-8") as w:
        for item in out_lines:
            w.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"[generator] Wrote {len(out_lines)} messages → {out}")
