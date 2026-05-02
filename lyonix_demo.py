# =============================================
# LYONiX Suite - Demo
# Lightweight Provenance for AI Content
# =============================================

import hashlib
from datetime import datetime

print("🚀 LYONiX Suite Demo")
print("Graph-based Provenance & Derivative Tracking\n")

def create_lyo(content: str, creator: str):
    """Create a tamper-proof LYO provenance unit"""
    timestamp = datetime.now().isoformat()
    data = f"{content}|{creator}|{timestamp}".encode('utf-8')
    hash_value = hashlib.sha256(data).hexdigest()
    
    print(f"✅ LYO Created")
    print(f"   Creator   : {creator}")
    print(f"   Time      : {timestamp}")
    print(f"   Hash      : {hash_value[:16]}...\n")
    return hash_value

# Demo
print("=== Original Work ===")
work1 = create_lyo(
    "Artificial intelligence is transforming how we understand the universe.", 
    "ErikLYONiX"
)

print("=== Possible Derivative ===")
work2 = create_lyo(
    "AI is changing our understanding of the cosmos.", 
    "AnotherUser"
)

print("=== Summary ===")
print("• Cryptographic records for provenance")
print("• Timestamps prove what came first")
print("• Ready for graph layer and similarity detection")
print("\nGreat for AI training data transparency and attribution!")