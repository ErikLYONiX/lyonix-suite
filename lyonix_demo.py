# lyonix_demo.py
# LYONiX - Graph-based AI Provenance Engine (Demo for xAI)

import hashlib
import numpy as np
from collections import defaultdict
from datetime import datetime

class LYONiX:
    """LYONiX: Lightweight provenance system for tracking content lineage and derivatives."""

    def __init__(self):
        self.works = {}                    # fp -> metadata
        self.graph = defaultdict(list)     # source_fp -> [(target_fp, similarity, timestamp)]

    def register(self, content: str, creator: str):
        fp = hashlib.sha256(content.encode()).hexdigest()
        emb = self._create_embedding(content)
        
        self.works[fp] = {
            "creator": creator,
            "content_preview": content[:120] + "..." if len(content) > 120 else content,
            "embedding": emb,
            "timestamp": datetime.now()
        }
        print(f"✓ Registered: {creator:<10} | {fp[:12]}...")

    def _create_embedding(self, text):
        emb = np.zeros(256, dtype=float)
        for i in range(len(text)-1):
            c1 = ord(text[i].lower()) % 256
            c2 = ord(text[i+1].lower()) % 256
            emb[c1] += 1.0
            emb[c2] += 0.5
        return emb / (np.sum(emb) + 1e-9)

    def detect_derivatives(self, new_content: str, threshold=0.73):
        """Detect derivatives and record provenance edges."""
        new_emb = self._create_embedding(new_content)
        new_fp = hashlib.sha256(new_content.encode()).hexdigest()
        
        matches = []
        for fp, data in self.works.items():
            sim = np.dot(new_emb, data["embedding"]) / (np.linalg.norm(new_emb) * np.linalg.norm(data["embedding"]) + 1e-9)
            if sim > threshold:
                self.graph[fp].append((new_fp, round(sim, 3), datetime.now()))
                matches.append((data["creator"], round(sim, 3)))
        
        return sorted(matches, key=lambda x: -x[1])

    def show_provenance(self):
        print("\nProvenance Graph (Lineage):")
        for source_fp, derivatives in list(self.graph.items())[:3]:
            if derivatives:
                creator = self.works[source_fp]["creator"]
                print(f"   {creator} → {len(derivatives)} derivative(s)")

if __name__ == "__main__":
    print("="*75)
    print("                    LYONiX PROVENANCE ENGINE")
    print("             Real-time Derivative & Lineage Tracking")
    print("="*75 + "\n")

    lx = LYONiX()

    print("Registering source works...\n")
    lx.register("High quality image of a futuristic city at night, cyberpunk style, neon lights, rain reflections on wet streets", "Alice")
    lx.register("Original melody: C E G A B in 128bpm electronic track with deep synth leads and atmospheric pads", "Bob")

    print("\nTesting new AI-generated content...\n")
    results = lx.detect_derivatives(
        "Neon cyberpunk city at midnight with heavy rain, dramatic reflections, glowing holographic signs v2"
    )

    print("Strong Derivatives Detected:")
    for creator, sim in results:
        print(f"   → {creator:<8} | Similarity: {sim:.3f}")

    lx.show_provenance()

    print("\nLYONiX Core: Fingerprinting + Embeddings + Directed Provenance Graph")
    print("Ready for scaling into training data lineage, deepfake detection, and truth infrastructure.")