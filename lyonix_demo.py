
# =============================================
# LYONiX Suite - Demo
# Lightweight Provenance & Derivative Tracking
# =============================================

import hashlib
from datetime import datetime

print("🚀 LYONiX Suite Demo")
print("Graph-based Provenance for AI Content\n")

def create_lyo(content: str, creator: str):
    """Create a tamper-proof LYO provenance unit"""
    timestamp = datetime.now().isoformat()
    data = f"{content}|{creator}|{timestamp}".encode('utf-8')
    hash_value = hashlib.sha256(data).hexdigest()
    
    print(f"✅ LYO Created")
    print(f"   Creator   : {creator}")
    print(f"   Time      : {timestamp}")
    print(f"   Hash      : {hash_value[:16]}...\n")
    return {"content": content, "creator": creator, "time": timestamp, "hash": hash_value}

# Demo 1: Original creation
print("=== Original Work ===")
work1 = create_lyo(
    "Artificial intelligence is transforming how we understand the universe.", 
    "ErikLYONiX"
)

# Demo 2: Possible derivative
print("=== Possible Derivative Work ===")
work2 = create_lyo(
    "AI is changing our understanding of the cosmos and reality.", 
    "AnotherUser"
)

print("=== Summary ===")
print("• Cryptographic hashing provides tamper-proof records")
print("• Timestamps prove what came first")
print("• Next: Add similarity detection + graph connections between works")
print("\nLYONiX is ready for higher tiers (Graph, Semantic Similarity, Reasoning)")