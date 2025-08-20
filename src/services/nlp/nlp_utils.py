from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text as sklearn_text
import re

# Combine default stop words with custom set
STOP = set(list(sklearn_text.ENGLISH_STOP_WORDS)) | {"amp", "rt", "—", "•"}

def _clean(t: str) -> str:
    # Remove URLs
    t = re.sub(r"http\S+", "", t or "")
    # Keep only allowed characters
    t = re.sub(r"[^\w\s#@&+-]", " ", t)
    # Normalize spaces and lowercase
    return re.sub("\s+", " ", t).strip().lower()

def analyze_texts(texts):
    # Remove None or empty strings
    texts = [t for t in texts if t and t.strip()]
    if not texts:
        print("[WARNING] No valid profiles to analyze. Using fallback topic.")
        return (["networking"], [])

    # Clean texts
    cleaned = list(map(_clean, texts))

    # Remove any that became empty after cleaning
    cleaned_non_empty = [doc for doc in cleaned if doc.strip()]
    removed_count = len(cleaned) - len(cleaned_non_empty)
    if removed_count > 0:
        print(f"[WARNING] {removed_count} profiles removed after cleaning (empty or only stop words).")

    # If nothing left after cleaning, fallback
    if not cleaned_non_empty:
        print("[ERROR] All profiles were empty after cleaning. Using fallback topic.")
        return (["networking"], [])

    try:
        vec = TfidfVectorizer(
            stop_words=list(STOP),
            ngram_range=(1, 2),
            max_features=20
        )
        X = vec.fit_transform(cleaned_non_empty)
        feats = vec.get_feature_names_out().tolist()

        # Simple heuristic: top features as topics
        topics = feats[:5] or ["networking"]

        # Entities stub (title-case words)
        entities = [w for w in feats if w.istitle()]

        return (topics, entities)

    except ValueError as e:
        print(f"[ERROR] Vectorization failed: {e}")
        return (["networking"], [])
