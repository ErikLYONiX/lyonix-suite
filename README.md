# LYONiX Suite

**Lightweight graph-based provenance system for AI-generated content**

LYONiX tracks who created what, when, and detects derivatives using cryptography and similarity. It helps prove originality, fairly attribute work, and supports better AI training data compliance.

### Core Idea
Combine tamper-proof timestamps (Monad Core) with a graph that shows content relationships. Perfect for the age of generative AI.

### Tier System (Roadmap)

| Tier | Name                    | What it does                                      | Status      |
|------|-------------------------|---------------------------------------------------|-------------|
| 0-1  | Monad Core             | Cryptographic timestamping + LYO attribution     | Working    |
| 2    | Graph Layer            | Tracks lineage and relationships                  | In progress|
| 3    | Semantic Similarity    | Embedding-based derivative detection             | Planned    |
| 4+   | Reasoning & Risk       | Disagreement engines, legal risk, compliance     | Vision     |

### Quick Start
```bash
git clone https://github.com/ErikLYONiX/lyonix-suite.git
cd lyonix-suite
python lyonix_demo.py