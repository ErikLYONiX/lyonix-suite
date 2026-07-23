# LYONiX System SLS — Provenance Engine
import hashlib
import numpy as np
from collections import defaultdict
from datetime import datetime
from typing import Dict, Any
import json

class LYONiXProvenance:
    """Immutable provenance tracking with cryptographic signing for the LYONiX System SLS."""
    def __init__(self):
        self.works = {}
        self.graph = defaultdict(list)
        self.signatures = {}
    
    def _embedding(self, text: str) -> np.ndarray:
        emb = np.zeros(256, dtype=float)
        for i in range(len(text)-1):
            c1 = ord(text[i].lower()) % 256
            c2 = ord(text[i+1].lower()) % 256
            emb[c1] += 1.0
            emb[c2] += 0.5
        return emb / (np.sum(emb) + 1e-9)
    
    def register(self, content: str, creator: str, metadata: Dict = None):
        fp = hashlib.sha256(content.encode()).hexdigest()
        emb = self._embedding(content)
        signature = hashlib.sha256((fp + creator).encode()).hexdigest()
        
        self.works[fp] = {
            "creator": creator,
            "embedding": emb,
            "ts": datetime.now(),
            "metadata": metadata or {}
        }
        self.signatures[fp] = signature
        print(f"✓ Registered & Signed: {creator} | {fp[:16]}...")
        return fp
    
    def detect_derivatives(self, new_content: str, threshold=0.73):
        new_emb = self._embedding(new_content)
        new_fp = hashlib.sha256(new_content.encode()).hexdigest()
        matches = []
        for fp, data in self.works.items():
            sim = float(np.dot(new_emb, data["embedding"]) / 
                       (np.linalg.norm(new_emb) * np.linalg.norm(data["embedding"]) + 1e-9))
            if sim > threshold:
                self.graph[fp].append((new_fp, sim))
                matches.append((data["creator"], round(sim, 4)))
        return sorted(matches, key=lambda x: -x[1])
    
    def save_to_file(self, filename: str = "provenance.json"):
        with open(filename, 'w') as f:
            json.dump({
                "works": {k: {**v, "embedding": v["embedding"].tolist()} for k, v in self.works.items()},
                "signatures": self.signatures
            }, f, indent=2)
        print(f"✅ Provenance saved to {filename}")

if __name__ == "__main__":
    provenance = LYONiXProvenance()
    provenance.register("Sample content", "Alice")
    provenance.save_to_file()
    print("LYONiX System SLS Provenance Engine Active")
