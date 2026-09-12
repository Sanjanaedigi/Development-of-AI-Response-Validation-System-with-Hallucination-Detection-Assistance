import re

STOPWORDS = {
    "the","a","an","is","are","was","were","of","to","in","on","for","and",
    "or","what","why","how","does","do","this","that","it","with","from","as"
}

def words(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOPWORDS}

def evidence_text(evidence):
    return " ".join(x.get("text", "") for x in evidence)

def overlap(a, b):
    wa, wb = words(a), words(b)
    return len(wa & wb) / max(1, len(wa))
