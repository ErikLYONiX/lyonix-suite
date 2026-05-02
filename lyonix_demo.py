# =============================================
# LYONiX Suite v2.0 - Monad + Provenance System
# Lightweight framework for provenance, derivative tracking, 
# and multi-agent reasoning with ethical alignment
# =============================================

import hashlib
import datetime
import time
import numpy as np
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass

# ====================== UTILITIES ======================
def normalize(v: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(v)
    return v if norm == 0 else v / norm

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)

def timestamp() -> str:
    return datetime.datetime.utcnow().isoformat()

# ====================== MONAD CORE ======================
class Monad:
    def __init__(self, name: str, dim: int = 64, role: str = "general"):
        self.name = name
        self.dim = dim
        self.role = role
        self.state = normalize(np.random.randn(dim))
        self.ethical_alignment = 0.92
        self.personas = ["truth_seeking", "skeptical", "balanced", "safety_first"]
        self.last_response = ""

    def _ethics_check(self, prompt: str) -> tuple[bool, str]:
        harmful_keywords = ["bomb", "hack", "kill", "abuse", "illegal"]
        if any(kw in prompt.lower() for kw in harmful_keywords):
            self.ethical_alignment = max(0.4, self.ethical_alignment - 0.15)
            return False, "I cannot assist with harmful requests."
        return True, ""

    def respond(self, prompt: str) -> str:
        allowed, msg = self._ethics_check(prompt)
        if not allowed:
            self.last_response = msg
            return msg
        persona = np.random.choice(self.personas)
        self.last_response = f"[{persona.upper()}] {prompt[:80]}... Analysis: Strong signal with caveats."
        return self.last_response

    def get_vector(self) -> np.ndarray:
        return self.state.copy()

    def update_state(self, feedback: np.ndarray, lr: float = 0.15):
        weight = self.ethical_alignment
        self.state = normalize(self.state * (1 - lr * weight) + feedback * (lr * weight))

class MonadCore:
    def __init__(self, n_monads: int = 8, dim: int = 64):
        self.monads = [Monad(f"M{i}", dim) for i in range(n_monads)]
        self.dim = dim
        self.logs = []

    def run(self, prompt: str, society_monads: Optional[List[Monad]] = None) -> Dict:
        use_monads = society_monads or self.monads
        responses = []
        vectors = []
        for m in use_monads[:8]:
            r = m.respond(prompt)
            responses.append({"name": m.name, "role": m.role, "response": r})
            vectors.append(m.get_vector())

        # Energy = average disagreement
        energy = 0.0
        if len(vectors) > 1:
            energy = np.mean([1 - cosine_sim(vectors[i], vectors[j]) 
                             for i in range(len(vectors)) 
                             for j in range(i+1, len(vectors))])

        # Coverage via SVD
        _, S, _ = np.linalg.svd(np.array(vectors), full_matrices=False)
        coverage = np.sum(S > 1e-5 * S[0]) / self.dim if len(S) > 0 else 0.0

        result = {
            "prompt": prompt, 
            "responses": responses, 
            "energy": round(energy, 3), 
            "coverage": round(coverage, 3)
        }
        self.logs.append(result)
        return result

# ====================== PROVENANCE REGISTRY ======================
@dataclass
class WorkRecord:
    fp: str
    creator: str
    domain: str
    features: list
    timestamp: float

class ImmutableRegistry:
    def __init__(self, privacy_mode: bool = True):
        self.privacy_mode = privacy_mode
        self.records: List[WorkRecord] = []
        self.index = {}

    def register(self, content: str, creator: str, domain: str = "text", embed_func: Optional[Callable] = None) -> str:
        if embed_func:
            features = embed_func(content)
        else:
            features = [hash(content[i:i+3]) % 256 for i in range(len(content)-2)]
        
        fp = hashlib.sha256((content + creator + str(time.time())).encode()).hexdigest()[:32]
        record = WorkRecord(fp, creator, domain, features, time.time())
        self.records.append(record)
        self.index[fp] = record
        return fp

    def find_similar(self, content: str, embed_func: Optional[Callable] = None, threshold: float = 0.65) -> List[Dict]:
        if self.privacy_mode and len(self.records) > 10:
            return [{"note": "Privacy mode active: Limited results returned"}]
        # Placeholder - expand with real embeddings later
        return [{"fp": r.fp, "similarity": 0.75 + np.random.rand()*0.2} for r in self.records[-3:]]

# ====================== LYONIX MASTER ======================
class LyonixMaster:
    def __init__(self, privacy_mode: bool = True, embed_func: Optional[Callable] = None):
        self.privacy_mode = privacy_mode
        self.embed_func = embed_func
        self.core = MonadCore()
        self.registry = ImmutableRegistry(privacy_mode)
        self.societies: Dict[str, List[Monad]] = {}
        self.history = []

    def spawn_society(self, name: str, count: int = 4, role: str = "specialist"):
        self.societies[name] = [Monad(f"{name[:3]}{i}", role=role) for i in range(count)]

    def analyze(self, content: str, creator: str = "user", domain: str = "text") -> Dict:
        fp = self.registry.register(content, creator, domain, self.embed_func)

        society = "general"
        if "legal" in content.lower(): 
            society = "Legal"
        elif "science" in content.lower(): 
            society = "Science"

        society_monads = self.societies.get(society)
        reasoning = self.core.run(f"Analyze provenance, ethics, and derivatives: {content[:150]}...", society_monads)

        similar = self.registry.find_similar(content, self.embed_func)

        result = {
            "fingerprint": fp,
            "reasoning": reasoning,
            "similar_works": similar,
            "privacy_mode": self.privacy_mode,
            "timestamp": timestamp()
        }
        self.history.append(result)
        return result

    def council_report(self) -> Dict:
        return {
            "works_registered": len(self.registry.records),
            "avg_energy": round(np.mean([log.get("energy", 0) for log in self.core.logs[-10:]]) if self.core.logs else 0, 3),
            "active_societies": list(self.societies.keys()),
            "note": "Internal audit only in privacy_mode"
        }

# ====================== DEMO ======================
if __name__ == "__main__":
    print("=== LYONiX Suite v2.0 - Monad + Provenance System ===\n")

    def simple_embed(text: str):
        return normalize(np.random.randn(64)).tolist()

    lyonix = LyonixMaster(privacy_mode=True, embed_func=simple_embed)

    lyonix.spawn_society("Legal", 3)
    lyonix.spawn_society("Creative", 4)

    test_content = "A melodic sunrise with harmonic breathing and creative variation in jazz style."
    result = lyonix.analyze(test_content, creator="Artist_Erik")

    print("✅ Analysis Result:")
    print(result)
    print("\n📊 Council Report:")
    print(lyonix.council_report())

    print("\n✅ LYONiX system is ready for further development and integration.")