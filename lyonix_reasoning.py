import numpy as np
import uuid
import datetime
import json
from typing import List, Dict, Any

def normalize(v):
    norm = np.linalg.norm(v)
    return v if norm == 0 else v / norm

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)

def timestamp():
    return str(datetime.datetime.utcnow())

class Monad:
    def __init__(self, name, dim=32):
        self.name = name
        self.state = normalize(np.random.randn(dim))
        self.reliability = np.random.uniform(0.65, 0.95)
        self.personas = ["optimistic", "skeptical", "safety_first", "pragmatic", "contrarian", "balanced"]
        self.last_response = ""
        self.last_persona = ""

    def respond(self, prompt):
        self.last_persona = np.random.choice(self.personas)
        templates = {
            "optimistic": f"[{self.last_persona}] {prompt} → Strong potential for positive outcomes with careful execution.",
            "skeptical": f"[{self.last_persona}] {prompt} → Significant risks and uncertainties remain.",
            "safety_first": f"[{self.last_persona}] {prompt} → Prioritize safeguards against failure modes.",
            "pragmatic": f"[{self.last_persona}] {prompt} → Balanced trade-offs favor practical implementation.",
            "contrarian": f"[{self.last_persona}] {prompt} → Conventional wisdom is flawed; consider the opposite.",
            "balanced": f"[{self.last_persona}] {prompt} → Nuanced view: benefits exist but require mitigation."
        }
        self.last_response = templates[self.last_persona]
        return self.last_response

class LyonixDebugger:
    def __init__(self, n_monads=6, dim=32):
        self.monads = [Monad(f"M{i}", dim) for i in range(n_monads)]
        self.logs = []

    def run(self, prompt):
        responses = []
        vectors = []
        for m in self.monads:
            r = m.respond(prompt)
            responses.append({
                "monad": m.name,
                "persona": m.last_persona,
                "response": r,
                "reliability": m.reliability
            })
            np.random.seed(abs(hash(r + m.last_persona)) % (2**32))
            perturbation = normalize(np.random.randn(dim) * 0.3)
            vector = normalize(m.state * 0.7 + perturbation)
            vectors.append(vector)

        diffs = [1 - cosine(vectors[i], vectors[j]) for i in range(len(vectors)) for j in range(i + 1, len(vectors))]
        energy = float(np.mean(diffs)) if diffs else 0.0

        _, S, _ = np.linalg.svd(np.array(vectors), full_matrices=False)
        coverage = float(np.sum(S > 1e-6 * S[0]) / dim) if len(S) > 0 else 0.0

        synthesis = {
            "final_answer": "Synthesized from multi-perspective debate.",
            "confidence": round(1.0 - abs(energy - 0.5) * 0.8, 2),
            "energy": round(energy, 3),
            "coverage": round(coverage, 3)
        }

        log_entry = {
            "id": str(uuid.uuid4()),
            "timestamp": timestamp(),
            "prompt": prompt,
            "responses": responses,
            "energy": energy,
            "coverage": coverage,
            "synthesis": synthesis
        }
        self.logs.append(log_entry)
        return log_entry

    def diagnostics(self):
        if not self.logs:
            return {"status": "no data"}
        energies = [l["energy"] for l in self.logs]
        return {
            "avg_energy": float(np.mean(energies)),
            "total_runs": len(self.logs)
        }

if __name__ == "__main__":
    system = LyonixDebugger()
    result = system.run("How should xAI approach long-term truth-seeking?")
    print("Energy:", result["energy"])
    print("Coverage:", result["coverage"])
