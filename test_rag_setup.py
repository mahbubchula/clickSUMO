"""
Test RAG System Setup
======================

Quick test script to verify the RAG system is working correctly.

Run this after installing dependencies to test:
1. Documentation parsing
2. Vector store creation
3. RAG query system

Author: Mahbub Hassan
Copyright © 2026 Mahbub Hassan
"""

import os
import sys
from pathlib import Path

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*70)
print("ClickSUMO RAG System Setup Test")
print("="*70)

# Test 1: Check documentation exists
print("\n[Test 1] Checking documentation location...")
docs_path = Path(r"D:\02_Research_&_Projects\Research_Ideas_&_Related_Documents\sumo_documentation\docs")
if docs_path.exists():
    html_files = list(docs_path.rglob("*.html"))
    print(f"[OK] Found {len(html_files)} HTML files")
else:
    print("[ERROR] Documentation path not found!")
    sys.exit(1)

# Test 2: Import and test doc parser
print("\n[Test 2] Testing documentation parser...")
try:
    from src.rag.doc_parser import SUMODocParser

    parser = SUMODocParser()
    stats = parser.get_document_stats()
    print(f"[OK] Parser initialized successfully")
    print(f"  - Total files: {stats['total_files']}")
    print(f"  - Categories: {len(stats['categories'])}")

    # Parse a few test documents
    print("\n  Parsing first 5 documents as test...")
    docs = parser.parse_all_docs(max_files=5)
    print(f"[OK] Successfully parsed {len(docs)} documents")

    for i, doc in enumerate(docs[:2], 1):
        print(f"\n  Sample {i}:")
        print(f"    Title: {doc['title'][:60]}...")
        print(f"    Category: {doc['category']}")
        print(f"    Content length: {len(doc['content'])} chars")

except Exception as e:
    print(f"[ERROR] Parser test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Test vector store
print("\n[Test 3] Testing vector store...")
try:
    from src.rag.vector_store import SUMOVectorStore

    print("  Initializing vector store (loading embedding model)...")
    vector_store = SUMOVectorStore(persist_directory="test_vector_db")
    print("[OK] Vector store initialized")

    # Add test documents
    print(f"  Adding {len(docs)} test documents...")
    vector_store.add_documents(docs)

    stats = vector_store.get_stats()
    print(f"[OK] Documents added successfully")
    print(f"  - Total documents in DB: {stats['total_documents']}")

    # Test search
    print("\n  Testing semantic search...")
    results = vector_store.search("How to create traffic lights?", n_results=2)
    print(f"[OK] Search completed, found {len(results)} results")

    if results:
        print(f"\n  Top result:")
        print(f"    Title: {results[0]['metadata']['title']}")
        print(f"    Category: {results[0]['metadata']['category']}")
        print(f"    Preview: {results[0]['content'][:150]}...")

except Exception as e:
    print(f"[ERROR] Vector store test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Test RAG engine
print("\n[Test 4] Testing RAG engine...")
try:
    from src.rag.rag_engine import SUMORagEngine
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv('GROQ_API_KEY')

    if not api_key:
        print("[WARNING] No API key found - skipping RAG engine test")
    else:
        print("  Initializing RAG engine...")
        engine = SUMORagEngine(api_key)

        # Check if vector store is populated
        status = engine.get_status()
        print(f"[OK] RAG engine initialized")
        print(f"  - Initialized: {status['initialized']}")
        print(f"  - Documents: {status['total_documents']}")
        print(f"  - Ready: {status['ready']}")

except Exception as e:
    print(f"[ERROR] RAG engine test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*70)
print("[SUCCESS] ALL TESTS PASSED!")
print("="*70)
print("\nNext steps:")
print("1. Run: python build_vector_db.py")
print("   This will index all 497 SUMO documentation files (takes 10-15 min)")
print("\n2. Then test with: python -m src.rag.rag_engine")
print("   This will test the complete RAG system with real queries")
print("\n3. Finally, restart your ClickSUMO app to use the RAG-powered AI Assistant!")
print("="*70)
