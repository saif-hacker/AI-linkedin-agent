import os
from openai import OpenAI

def llm_generate(prompt: str) -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return "[LLM disabled] " + prompt[:180]
    client = OpenAI(api_key=key)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7,
        max_tokens=160,
    )
    return resp.choices[0].message.content.strip()
