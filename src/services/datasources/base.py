from pydantic import BaseModel
from typing import List, Optional, Iterable
import json
from pathlib import Path

class Profile(BaseModel):
    name: str
    headline: Optional[str] = None
    about: Optional[str] = None
    recent_posts: Optional[List[str]] = None
    profile_url: Optional[str] = None

def write_jsonl(path: str, rows):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def read_jsonl(path: str) -> Iterable[dict]:
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)
