# lyonix_demo.py
# LYONiX - Graph-based Provenance Engine

import hashlib
import numpy as np
from collections import defaultdict
from datetime import datetime

class LYONiX:
    """LYONiX: Provenance via fingerprinting + cosine similarity + directed graph."""

    def __init__(self):
        self.works = {}                    # fp -> metadata
        self.graph = defaultdict(list)     # source_fp -> list of (derivative_fp, similarity)

    def _embedding(self, text: str) -> np.ndarray:
        """Character bigram frequency embedding (256-dim)."""
        emb = np.zeros(256, dtype=float)
        for i in range(len(text)-1):
            c1 = ord(text[i].lower()) % 256
            c2 = ord(text[i+1].lower()) % 256
            emb[c1] += 1.0
            emb[c2] += 0.5
        return emb / (np.sum(emb) + 1e-9)

    def register(self, content: str, creator: str):
        fp = hashlib.sha256(content.encode()).hexdigest()
        emb = self._embedding(content)
        
        self.works[fp] = {
            "creator": creator,
            "embedding": emb,
            "ts": datetime.now()
        }
        print(f"✓ Registered: {creator:<12} | {fp[:16]}...")

    def detect_derivatives(self, new_content: str, threshold=0.73):
        """Return derivatives + build graph."""
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

    def show_provenance(self):
        print("\nProvenance Graph (Lineage):")
        for source, edges in list(self.graph.items())[:3]:
            if edges:
                print(f"   {self.works[source]['creator']} → {len(edges)} derivative(s)")


if __name__ == "__main__":
    print("="*72)
    print("                  LYONiX PROVENANCE ENGINE")
    print("     Fingerprinting • Cosine Similarity • Directed Graph")
    print("="*72 + "\n")

    lx = LYONiX()

    lx.register("High quality image of a futuristic city at night, cyberpunk style, neon lights, rain reflections", "Alice")
    lx.register("Original melody: C E G A B in 128bpm electronic track with deep synth leads", "Bob")

    print("\nDetecting derivatives from new AI-generated content...\n")
    results = lx.detect_derivatives(
        "Neon cyberpunk cityscape at midnight, pouring rain, dramatic reflections and glowing holographic signs v2"
    )

    print("Derivative Matches:")
    for creator, sim in results:
        print(f"   → {creator:<8} | Cosine Similarity: {sim:.4f}")

    lx.show_provenance()

    print("\nCore Math: SHA-256 + Bigram Frequency Vectors + Cosine Similarity + Directed Acyclic Graph")
    print("Ready for training data lineage, deepfake detection, and influence mapping.")