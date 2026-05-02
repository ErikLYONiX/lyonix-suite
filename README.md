# LYONiX Suite

**Lightweight graph-based provenance system for AI-generated content**

LYONiX helps track who created what and when, detects derivatives, and supports fair attribution using cryptography and future semantic analysis.

### Core Idea
Combines tamper-proof timestamps (Monad Core) with a graph that shows content relationships. Designed for the era of generative AI.

### Tier System (Roadmap)

| Tier | Name                    | What it does                                      | Status      |
|------|-------------------------|---------------------------------------------------|-------------|
| 0-1  | Monad Core             | Cryptographic timestamping + LYO attribution     | ✅ Done     |
| 2    | Graph Layer            | Tracks lineage and relationships                  | Planned     |
| 3    | Semantic Similarity    | Embedding-based derivative detection              | Planned     |
| 4+   | Reasoning & Risk       | Disagreement engines, AI risk & compliance        | Vision      |

### How to Run the Demo

```bash
git clone https://github.com/ErikLYONiX/lyonix-suite.git
cd lyonix-suite
python lyonix_demo.py