
# lyonix_demo.py
# Professional demo for xAI - Real-time AI Provenance & Derivative Detection

import hashlib
import numpy as np
from collections import defaultdict

def cosine_sim(a, b):
    """Fast cosine similarity."""
    a = a.astype(float)
    b = b.astype(float)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)

class LYONiX:
    """LYONiX: Graph-based provenance engine for AI content."""

    def __init__(self):
        self.works = {}
        self.graph = defaultdict(list)

    def register(self, content: str, creator: str):
        fp = hashlib.sha256(content.encode()).hexdigest()
        emb = np.zeros(256, dtype=float)
        for i in range(len(content) - 1):
            c1 = ord(content[i].lower()) % 256
            c2 = ord(content[i + 1].lower()) % 256
            emb[c1] += 1.0
            emb[c2] += 0.5
        emb /= (np.sum(emb) + 1e-9)

        self.works[fp] = {"creator": creator, "embedding": emb}
        print(f"✓ Registered: {creator:<12} | {fp[:16]}...")

    def detect_derivatives(self, new_content: str, threshold: float = 0.72):
        """Detect derivatives and build provenance graph."""
        new_emb = np.zeros(256, dtype=float)
        for i in range(len(new_content) - 1):
            c1 = ord(new_content[i].lower()) % 256
            c2 = ord(new_content[i + 1].lower()) % 256
            new_emb[c1] += 1.0
            new_emb[c2] += 0.5
        new_emb /= (np.sum(new_emb) + 1e-9)

        matches = []
        for fp, data in self.works.items():
            sim = cosine_sim(new_emb, data["embedding"])
            if sim > threshold:
                self.graph[fp].append(round(sim, 3))
                matches.append((data["creator"], round(sim, 3)))
        return sorted(matches, key=lambda x: -x[1])


if __name__ == "__main__":
    print("=" * 70)
    print("                  LYONiX DEMO")
    print("       Real-time Provenance & Derivative Detection")
    print("=" * 70 + "\n")

    lx = LYONiX()

    print("Registering original works...\n")
    lx.register("High quality image of a futuristic city at night, cyberpunk style, neon lights, rain reflections", "Alice")
    lx.register("Original melody: C E G A B in 128bpm electronic track with deep synth leads", "Bob")

    print("\nDetecting derivatives from new AI-generated content...\n")
    results = lx.detect_derivatives(
        "Neon cyberpunk cityscape at midnight, pouring rain, dramatic reflections and glowing holographic signs v2"
    )

    print("Results:")
    for creator, sim in results:
        print(f"   → Strong derivative from {creator:<8} | Similarity: {sim:.3f}")

    print("\nLYONiX: Cryptographic fingerprinting + embedding similarity + provenance graph.")
    print("Designed for verifiable AI systems and content authenticity.")

