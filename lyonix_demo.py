#!/usr/bin/env python3
"""
LYONiX System SLS — Suite (Provenance + Monad Integration)
==========================================================
Local-first provenance tracking with cryptographic integrity,
derivative detection, and multi-perspective reasoning.

Creator: Erik L. Palmer
License: See LICENSE file in this repository

Components
----------
1. MonadGeometricEngine  — multi-view disagreement (lightweight)
2. LYONiXProvenance      — SHA-256 fingerprint + HMAC signing + lineage graph
3. LyonixSystem          — unified API + domain demos

Run:
    python lyonix_demo.py
"""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from math import sqrt
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

# =============================================================================
# Shared math primitives (aligned with Monad Core SLS)
# =============================================================================

PHI = (1.0 + sqrt(5.0)) / 2.0
VORTEX_CYCLE = [1, 2, 4, 8, 7, 5]


def digital_root(n: int) -> int:
    if n == 0:
        return 0
    return 1 + (abs(int(n)) - 1) % 9


def polar_complement(n: int) -> int:
    d = digital_root(n)
    return 9 if d in (0, 9) else 9 - d


# =============================================================================
# Monad Geometric Engine (suite-embedded, compatible with Monad Core API)
# =============================================================================

@dataclass
class PerspectiveResult:
    view: str
    insight_score: float
    energy: float


@dataclass
class MultiViewResult:
    perspectives: Dict[str, PerspectiveResult]
    disagreement: float
    consensus_insight: float
    elapsed_ms: float


class MonadGeometricEngine:
    """Multi-perspective geometric reasoning (SLS foundation)."""

    DEFAULT_VIEWS = ("standard", "inside_out", "boundary", "long_term", "vortex")

    def __init__(self, views: Optional[Sequence[str]] = None):
        self.vantage_points = list(views) if views else list(self.DEFAULT_VIEWS)

    @staticmethod
    def _as_2d(data: np.ndarray) -> np.ndarray:
        arr = np.asarray(data, dtype=float)
        if arr.ndim == 0:
            return arr.reshape(1, 1)
        if arr.ndim == 1:
            return arr.reshape(-1, 1)
        return arr

    def _transform(self, data: np.ndarray, view: str) -> np.ndarray:
        x = self._as_2d(data)
        if view == "standard":
            return x
        if view == "inside_out":
            return np.flip(x, axis=0)
        if view == "boundary":
            return x * (1.0 / PHI)
        if view == "long_term":
            c = np.cumsum(x, axis=0)
            n = np.arange(1, x.shape[0] + 1, dtype=float).reshape(-1, 1)
            return c / n
        if view == "vortex":
            w = np.array([VORTEX_CYCLE[i % 6] for i in range(x.shape[0])], dtype=float).reshape(-1, 1)
            return x * w
        raise ValueError(f"Unknown view: {view!r}")

    def analyze_multi_view(self, data: np.ndarray) -> MultiViewResult:
        t0 = time.perf_counter()
        perspectives: Dict[str, PerspectiveResult] = {}
        insights: List[float] = []
        for view in self.vantage_points:
            t = self._transform(data, view)
            insight = float(np.mean(np.abs(t))) if t.size else 0.0
            energy = float(np.sum(t * t)) if t.size else 0.0
            perspectives[view] = PerspectiveResult(view, insight, energy)
            insights.append(insight)
        arr = np.asarray(insights, dtype=float)
        return MultiViewResult(
            perspectives=perspectives,
            disagreement=float(np.std(arr)) if arr.size else 0.0,
            consensus_insight=float(np.mean(arr)) if arr.size else 0.0,
            elapsed_ms=(time.perf_counter() - t0) * 1000.0,
        )


# =============================================================================
# Provenance Engine
# =============================================================================

@dataclass
class WorkRecord:
    fingerprint: str
    creator: str
    signature: str
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[np.ndarray] = None


class LYONiXProvenance:
    """
    Immutable content registration with HMAC integrity and derivative detection.

    - Fingerprint: SHA-256 of content
    - Integrity:   HMAC-SHA256 (secret from env LYONiX_HMAC_KEY or ephemeral)
    - Derivatives: cosine similarity on character-bigram embeddings
    - Lineage:     directed graph of (parent_fp -> (child_fp, similarity))

    Note: bigram embeddings are a fast baseline, not semantic NLP embeddings.
    """

    def __init__(self, secret_key: Optional[bytes] = None):
        env_key = os.environ.get("LYONiX_HMAC_KEY")
        if secret_key is not None:
            self.secret_key = secret_key
        elif env_key:
            self.secret_key = env_key.encode()
        else:
            self.secret_key = secrets.token_bytes(32)
            self._ephemeral = True
        self._ephemeral = secret_key is None and not env_key
        self.works: Dict[str, WorkRecord] = {}
        self.graph: Dict[str, List[Tuple[str, float]]] = defaultdict(list)

    def _embedding(self, text: str) -> np.ndarray:
        emb = np.zeros(256, dtype=float)
        text = text.lower()
        for i in range(len(text) - 1):
            c1 = ord(text[i]) % 256
            c2 = ord(text[i + 1]) % 256
            emb[c1] += 1.0
            emb[c2] += 0.5
        norm = np.sum(emb) + 1e-9
        return emb / norm

    def _sign(self, content: str) -> str:
        return hmac.new(self.secret_key, content.encode("utf-8"), hashlib.sha256).hexdigest()

    @staticmethod
    def fingerprint(content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def register(
        self,
        content: str,
        creator: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        fp = self.fingerprint(content)
        sig = self._sign(content)
        emb = self._embedding(content)
        self.works[fp] = WorkRecord(
            fingerprint=fp,
            creator=creator,
            signature=sig,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata or {},
            embedding=emb,
        )
        return fp

    def verify(self, content: str, fp: str) -> bool:
        rec = self.works.get(fp)
        if rec is None:
            return False
        if self.fingerprint(content) != fp:
            return False
        return hmac.compare_digest(rec.signature, self._sign(content))

    def detect_derivatives(
        self, new_content: str, threshold: float = 0.73
    ) -> List[Tuple[str, str, float]]:
        """
        Returns list of (creator, parent_fp, similarity) above threshold.
        Also records edges in the lineage graph.
        """
        new_emb = self._embedding(new_content)
        new_fp = self.fingerprint(new_content)
        matches: List[Tuple[str, str, float]] = []
        for fp, rec in self.works.items():
            if rec.embedding is None:
                continue
            denom = (np.linalg.norm(new_emb) * np.linalg.norm(rec.embedding)) + 1e-9
            sim = float(np.dot(new_emb, rec.embedding) / denom)
            if sim > threshold:
                self.graph[fp].append((new_fp, sim))
                matches.append((rec.creator, fp, round(sim, 4)))
        matches.sort(key=lambda x: -x[2])
        return matches

    def lineage(self, fp: str) -> List[Tuple[str, float]]:
        """Children of a fingerprint."""
        return list(self.graph.get(fp, []))

    def stats(self) -> Dict[str, Any]:
        return {
            "registered": len(self.works),
            "edges": sum(len(v) for v in self.graph.values()),
            "ephemeral_key": self._ephemeral,
        }


# =============================================================================
# Unified system
# =============================================================================

class LyonixSystem:
    """Monad + Provenance integrated API."""

    def __init__(self, hmac_key: Optional[bytes] = None):
        self.monad = MonadGeometricEngine()
        self.provenance = LYONiXProvenance(secret_key=hmac_key)

    def stock_style_demo(self, prices: np.ndarray) -> MultiViewResult:
        return self.monad.analyze_multi_view(np.asarray(prices, dtype=float).reshape(-1, 1))

    def weather_style_demo(self, temps: np.ndarray) -> MultiViewResult:
        return self.monad.analyze_multi_view(np.asarray(temps, dtype=float).reshape(-1, 1))


# =============================================================================
# Self-test + benchmark
# =============================================================================

def _self_test() -> Tuple[bool, Dict[str, bool]]:
    checks: Dict[str, bool] = {}
    checks["phi"] = abs(PHI ** 2 - (PHI + 1)) < 1e-14
    checks["vortex"] = VORTEX_CYCLE == [1, 2, 4, 8, 7, 5]
    key = b"test-key-for-self-test-only-32b!!"
    prov = LYONiXProvenance(secret_key=key)
    content = "stable test content alpha"
    fp = prov.register(content, "tester")
    checks["register"] = len(fp) == 64
    checks["verify_ok"] = prov.verify(content, fp) is True
    checks["verify_tamper"] = prov.verify(content + "x", fp) is False
    prov.register("cyberpunk neon city rain reflections night", "Alice")
    hits = prov.detect_derivatives("neon cyberpunk city at night with rain reflections")
    checks["derivative_hit"] = len(hits) >= 1
    eng = MonadGeometricEngine()
    mv = eng.analyze_multi_view(np.random.default_rng(0).normal(size=(32, 2)))
    checks["multiview"] = mv.disagreement >= 0 and len(mv.perspectives) == 5
    ok = all(checks.values())
    return ok, checks


def _benchmark() -> Dict[str, float]:
    out: Dict[str, float] = {}
    eng = MonadGeometricEngine()
    rng = np.random.default_rng(1)
    for n in (100, 1000, 10000):
        data = rng.normal(size=(n, 3))
        t0 = time.perf_counter()
        for _ in range(10):
            eng.analyze_multi_view(data)
        out[f"monad_{n}x3_ms"] = (time.perf_counter() - t0) / 10 * 1000.0
    prov = LYONiXProvenance(secret_key=b"bench-key-32-bytes-pad-pad-pad!!")
    t0 = time.perf_counter()
    for i in range(200):
        prov.register(f"benchmark content line {i} padding text", f"u{i}")
    out["prov_200_register_ms"] = (time.perf_counter() - t0) * 1000.0
    t0 = time.perf_counter()
    keys = list(prov.works.keys())
    for i in range(50):
        prov.verify(f"benchmark content line {i} padding text", keys[i])
    out["prov_50_verify_ms"] = (time.perf_counter() - t0) * 1000.0
    return out


if __name__ == "__main__":
    print("=" * 72)
    print("  LYONiX System SLS — Suite Demo")
    print("  Provenance • HMAC Integrity • Multi-Perspective Reasoning")
    print("  Creator: Erik L. Palmer")
    print("=" * 72)

    ok, checks = _self_test()
    print("\n[Self-test]")
    for k, v in checks.items():
        print(f"  {k:<20} {'PASS' if v else 'FAIL'}")
    print(f"  overall: {'PASS' if ok else 'FAIL'}")

    print("\n[Micro-benchmark]")
    for k, v in _benchmark().items():
        print(f"  {k:<28} {v:8.3f} ms")

    system = LyonixSystem(hmac_key=b"demo-key-not-for-production-use!!")

    print("\n[1] Provenance registration + verify")
    fp1 = system.provenance.register(
        "High quality image of a futuristic city at night, cyberpunk style, neon lights, rain reflections",
        "Alice",
        metadata={"type": "image_prompt"},
    )
    fp2 = system.provenance.register(
        "Original melody: C E G A B in 128bpm electronic track with deep synth leads",
        "Bob",
        metadata={"type": "audio_desc"},
    )
    original = "High quality image of a futuristic city at night, cyberpunk style, neon lights, rain reflections"
    print(f"  Alice fp: {fp1[:16]}...")
    print(f"  verify original: {system.provenance.verify(original, fp1)}")
    print(f"  verify tampered: {system.provenance.verify(original + 'x', fp1)}")

    print("\n[2] Derivative detection")
    hits = system.provenance.detect_derivatives(
        "Neon cyberpunk cityscape at midnight, pouring rain, dramatic reflections and glowing holographic signs v2"
    )
    for creator, parent, sim in hits:
        print(f"  → {creator:<8} sim={sim:.4f}  parent={parent[:12]}...")

    print("\n[3] Domain demos (Monad multi-view)")
    prices = np.random.default_rng(3).normal(size=200) * 10 + 100
    mv = system.stock_style_demo(prices)
    print(f"  stock-style  disagreement={mv.disagreement:.4f}  elapsed={mv.elapsed_ms:.3f} ms")
    temps = np.random.default_rng(4).normal(size=100) * 5 + 20
    mv2 = system.weather_style_demo(temps)
    print(f"  weather-style disagreement={mv2.disagreement:.4f}  elapsed={mv2.elapsed_ms:.3f} ms")

    print("\n[4] Stats")
    print(f"  {system.provenance.stats()}")

    print("\n" + "=" * 72)
    print("  Core: SHA-256 • HMAC-SHA256 • bigram cosine • multi-view disagreement")
    print("  Ready for: lineage, derivative flags, audit demos, tier extensions")
    print("=" * 72)