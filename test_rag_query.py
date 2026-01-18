"""
Quick RAG Query Test
Test the RAG system with a sample question
"""

import os
from dotenv import load_dotenv
from src.rag.rag_engine import SUMORagEngine

# Load API key
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

if not api_key:
    print("ERROR: No API key found in .env file")
    exit(1)

# Initialize RAG engine
print("\n" + "="*70)
print("RAG Engine Test")
print("="*70)

engine = SUMORagEngine(api_key)

# Check status
print("\n[Status Check]")
status = engine.get_status()
print(f"  Initialized: {status['initialized']}")
print(f"  Documents: {status['total_documents']}")
print(f"  Ready: {status['ready']}")

if not status['ready']:
    print("\nERROR: RAG engine not ready!")
    exit(1)

# Test query
print("\n[Test Query]")
question = "How do I create traffic lights in SUMO?"
print(f"\nQuestion: {question}")
print("\nSearching documentation and generating answer...")

result = engine.query(question, n_results=2)

print("\n" + "-"*70)
print("ANSWER:")
print("-"*70)
print(result['answer'])

print("\n" + "-"*70)
print(f"SOURCES ({len(result['sources'])} documents):")
print("-"*70)
for i, src in enumerate(result['sources'], 1):
    print(f"\n{i}. {src['title']}")
    print(f"   Category: {src['category']}")
    print(f"   Preview: {src['preview'][:150]}...")

print("\n" + "="*70)
print("[SUCCESS] RAG system is working correctly!")
print("="*70)
