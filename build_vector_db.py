"""
Build SUMO Documentation Vector Database
=========================================

This script builds the complete vector database from all SUMO documentation.
Run this ONCE to index all 497 HTML files.

After running this, the RAG system will be ready to use!

Usage:
    python build_vector_db.py

Time: ~10-15 minutes for 497 documents

Author: Mahbub Hassan
Copyright © 2026 Mahbub Hassan
"""

import os
import sys
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.rag.doc_parser import SUMODocParser
from src.rag.vector_store import SUMOVectorStore

print("="*70)
print("ClickSUMO - Building SUMO Documentation Vector Database")
print("="*70)
print("\nThis will:")
print("  1. Parse 497 SUMO HTML documentation files")
print("  2. Extract clean text content")
print("  3. Create vector embeddings")
print("  4. Build searchable vector database")
print("\nEstimated time: 10-15 minutes")
print("="*70)

input("\nPress ENTER to start building the database...")

start_time = time.time()

# Step 1: Parse documentation
print("\n[Step 1/3] Parsing SUMO documentation...")
print("-" * 70)

parser = SUMODocParser()
stats = parser.get_document_stats()

print(f"Found {stats['total_files']} HTML files")
print(f"Categories: {', '.join(list(stats['categories'].keys())[:10])}...")

print("\nParsing all documents (this may take 5-8 minutes)...")
documents = parser.parse_all_docs()

print(f"✓ Successfully parsed {len(documents)} documents")
print(f"  Time elapsed: {(time.time() - start_time)/60:.1f} minutes")

# Step 2: Build vector database
print("\n[Step 2/3] Building vector database...")
print("-" * 70)
print("Initializing vector store (downloading embedding model if needed)...")

vector_store = SUMOVectorStore(persist_directory="vector_db")

print(f"\nAdding {len(documents)} documents to vector database...")
print("Progress will be shown every 500 documents...")

step2_start = time.time()
vector_store.add_documents(documents, batch_size=100)

print(f"✓ Vector database built successfully")
print(f"  Time for this step: {(time.time() - step2_start)/60:.1f} minutes")

# Step 3: Verify and test
print("\n[Step 3/3] Verifying database...")
print("-" * 70)

stats = vector_store.get_stats()
print(f"✓ Vector database statistics:")
print(f"  - Total documents: {stats['total_documents']}")
print(f"  - Embedding model: {stats['embedding_model']}")
print(f"  - Storage location: {stats['persist_directory']}")

# Test search
print("\n  Testing semantic search...")
test_queries = [
    "How do I create a simple network?",
    "What are car-following models?",
    "How do traffic lights work?"
]

for query in test_queries:
    results = vector_store.search(query, n_results=1)
    if results:
        print(f"  ✓ '{query[:40]}...' → {results[0]['metadata']['title']}")

# Summary
total_time = time.time() - start_time
print("\n" + "="*70)
print("✓ DATABASE BUILD COMPLETE!")
print("="*70)
print(f"\nTotal time: {total_time/60:.1f} minutes")
print(f"Documents indexed: {stats['total_documents']}")
print(f"Database size: {Path('vector_db').stat().st_size / (1024*1024):.1f} MB")

print("\n" + "="*70)
print("Next Steps:")
print("="*70)
print("\n1. Test the RAG system:")
print("   python -m src.rag.rag_engine")
print("\n2. Restart ClickSUMO app:")
print("   streamlit run app.py")
print("\n3. Go to 🤖 AI Assistant page and ask SUMO questions!")
print("   Example: 'How do I model traffic lights in SUMO?'")
print("\n" + "="*70)
print("The RAG system is now ready to power your AI Assistant! 🚀")
print("="*70)
