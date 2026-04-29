# Add this near the top
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity   # ← This is the problem
# lyonix_demo.py
# Clean single-file demo for xAI

import hashlib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

class LYONiX:
    """Lightweight graph-based provenance engine for AI content."""
    
    def __init__(self):
        self.works = {}                    # fingerprint -> metadata
        self.graph = defaultdict(list)     # source_fp -> list of (derivative, similarity)

    def register(self, content: str, creator: str):
        """Register a work and return its fingerprint."""
        fp = hashlib.sha256(content.encode()).hexdigest()
        emb = np.array([ord(c) % 10 for c in content[:200]])
        self.works[fp] = {"creator": creator, "embedding": emb}
        print(f"Registered: {creator} | {fp[:16]}...")
        return fp

    def detect_derivatives(self, new_content: str):
        """Detect similar/derivative works and build graph."""
        new_emb = np.array([ord(c) % 10 for c in new_content[:200]])
        matches = []
        
        for fp, data in self.works.items():
            sim = cosine_similarity([new_emb], [data["embedding"]])[0][0]
            if sim > 0.75:
                self.graph[fp].append((new_content[:60] + "...", round(sim, 3)))
                matches.append((data["creator"], round(sim, 3)))
        
        return sorted(matches, key=lambda x: -x[1])

# === Demo ===
if __name__ == "__main__":
    lx = LYONiX()
    
    lx.register("High quality image of a futuristic city at night, cyberpunk style", "Alice")
    lx.register("Original melody: C E G A B in 128bpm electronic track", "Bob")
    
    print("\n--- Detecting derivatives ---")
    results = lx.detect_derivatives("Futuristic cityscape at night, neon cyberpunk aesthetic v2")
    
    print("Derivative matches:", results)
    print("\nLYONiX: Real-time AI provenance & derivative tracking.")
