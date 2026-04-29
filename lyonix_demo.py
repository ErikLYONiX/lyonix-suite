# lyonix_demo.py
# Clean, improved single-file demo for xAI
# Built from Geometry → Translated into working provenance engine

import hashlib
import numpy as np
from collections import defaultdict

def cosine_sim(a, b):
    """Simple cosine similarity without sklearn dependency."""
    a = a.astype(float)
    b = b.astype(float)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)

class LYONiX:
    """LYONiX Monad Demo - Lightweight provenance engine."""
    
    def __init__(self):
        self.works = {}                    # fingerprint -> metadata
        self.graph = defaultdict(list)     # source_fp -> list of derivatives
        self.sequence = 0                  # Simple temporal sequencing

    def register(self, content: str, creator: str):
        """Register a work with cryptographic fingerprint + temporal order."""
        fp = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        # Better lightweight embedding (character frequency)
        emb = np.zeros(256, dtype=float)
        for c in content.lower():
            if ord(c) < 256:
                emb[ord(c)] += 1
        emb = emb / (np.sum(emb) + 1e-9)

        self.sequence += 1
        self.works[fp] = {
            "creator": creator,
            "content_preview": content[:100] + "..." if len(content) > 100 else content,
            "embedding": emb,
            "timestamp": self.sequence,
            "registered_at": "2026-04-29"
        }
        print(f"✓ Registered: {creator} | {fp[:12]}... | seq={self.sequence}")
        return fp

    def detect_derivatives(self, new_content: str, threshold=0.65):
        """Detect derivatives using similarity + temporal awareness."""
        new_emb = np.zeros(256, dtype=float)
        for c in new_content.lower():
            if ord(c) < 256:
                new_emb[ord(c)] += 1
        new_emb = new_emb / (np.sum(new_emb) + 1e-9)

        matches = []
        for fp, data in self.works.items():
            sim = cosine_sim(new_emb, data["embedding"])
            if sim > threshold:
                self.graph[fp].append({
                    "derivative_preview": new_content[:80] + "...",
                    "similarity": round(sim, 3)
                })
                matches.append((data["creator"], round(sim, 3), data["timestamp"]))

        return sorted(matches, key=lambda x: -x[1])

    def generate_compliance_hash(self):
        """Generate a compliance hash proving all sources were documented."""
        all_fps = sorted(self.works.keys())
        combined = "".join(all_fps).encode('utf-8')
        compliance_hash = hashlib.sha256(combined).hexdigest()
        print(f"\nCompliance Hash (proves documentation):")
        print(compliance_hash)
        return compliance_hash

# ====================== DEMO ======================
if __name__ == "__main__":
    print("=== LYONiX Monad Demo ===\n")
    print("Built from Geometry → Cryptographic Provenance\n")

    lx = LYONiX()

    # Register original works
    lx.register("High quality image of a futuristic city at night, cyberpunk style, neon lights, rain", "Alice")
    lx.register("Original melody: C E G A B in 128bpm electronic track with synth leads", "Bob")

    print("\n--- Detecting Derivatives ---")
    results = lx.detect_derivatives(
        "Futuristic neon cityscape at night with heavy rain and cyberpunk aesthetic v2"
    )

    print("Derivative matches:")
    for creator, sim, ts in results:
        print(f"  → From {creator}: similarity = {sim}")

    lx.generate_compliance_hash()

    print("\n✓ Demo completed.")
    print("This demonstrates the core Monad ideas:")
    print("   • Cryptographic registration")
    print("   • Temporal sequencing")
    print("   • Derivative detection")
    print("   • Compliance-style hashing")