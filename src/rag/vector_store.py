"""
SUMO Vector Store
=================

Creates and manages vector embeddings of SUMO documentation
for semantic search and retrieval.

Uses FAISS for efficient similarity search.

Author: Mahbub Hassan
Copyright © 2026 Mahbub Hassan
"""

import os
import pickle
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class SUMOVectorStore:
    """Vector database for SUMO documentation using FAISS."""

    def __init__(self, persist_directory: str = "vector_db"):
        """
        Initialize vector store.

        Args:
            persist_directory: Directory to store the vector database
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(exist_ok=True)

        # Initialize embedding model
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = 384  # all-MiniLM-L6-v2 produces 384-dim embeddings
        print("Embedding model loaded successfully")

        # FAISS index and metadata storage
        self.index = None
        self.documents = []  # Store original documents
        self.metadata = []   # Store metadata

        # File paths for persistence
        self.index_path = self.persist_directory / "faiss_index.bin"
        self.metadata_path = self.persist_directory / "metadata.pkl"

        # Load existing index if available
        self._load_index()

    def _load_index(self):
        """Load existing FAISS index and metadata from disk."""
        if self.index_path.exists() and self.metadata_path.exists():
            try:
                # Load FAISS index
                self.index = faiss.read_index(str(self.index_path))

                # Load metadata
                with open(self.metadata_path, 'rb') as f:
                    data = pickle.load(f)
                    self.documents = data['documents']
                    self.metadata = data['metadata']

                print(f"Loaded existing index with {len(self.documents)} documents")
            except Exception as e:
                print(f"Error loading index: {e}")
                print("Creating new index...")
                self._create_new_index()
        else:
            self._create_new_index()

    def _create_new_index(self):
        """Create a new FAISS index."""
        # Use L2 (Euclidean) distance index
        # For normalized vectors, L2 distance is equivalent to cosine similarity
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.documents = []
        self.metadata = []
        print("Created new FAISS index")

    def _save_index(self):
        """Save FAISS index and metadata to disk."""
        # Save FAISS index
        faiss.write_index(self.index, str(self.index_path))

        # Save metadata
        with open(self.metadata_path, 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'metadata': self.metadata
            }, f)

    def add_documents(self, documents: List[Dict[str, str]], batch_size: int = 100):
        """
        Add documents to the vector store.

        Args:
            documents: List of parsed documents
            batch_size: Number of documents to process at once
        """
        total_docs = len(documents)
        print(f"Adding {total_docs} documents to vector store...")

        all_embeddings = []

        for i in range(0, total_docs, batch_size):
            batch = documents[i:i + batch_size]

            # Extract texts and metadata
            texts = [doc['content'] for doc in batch]

            # Generate embeddings
            embeddings = self.embedding_model.encode(
                texts,
                show_progress_bar=False,
                convert_to_numpy=True
            )

            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)

            # Add to index
            self.index.add(embeddings)

            # Store documents and metadata
            for doc in batch:
                self.documents.append(doc['content'])
                self.metadata.append({
                    'title': doc['title'],
                    'file_path': doc['file_path'],
                    'url': doc['url'],
                    'category': doc['category']
                })

            if (i + batch_size) % 500 == 0 or (i + batch_size) >= total_docs:
                print(f"  Progress: {min(i + batch_size, total_docs)}/{total_docs} documents")

        # Save to disk
        print("Saving index to disk...")
        self._save_index()
        print("All documents added successfully!")

    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Search for relevant documents.

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            List of relevant documents with metadata
        """
        if self.index is None or len(self.documents) == 0:
            return []

        # Generate query embedding
        query_embedding = self.embedding_model.encode(
            [query],
            convert_to_numpy=True
        )

        # Normalize for cosine similarity
        faiss.normalize_L2(query_embedding)

        # Search
        n_results = min(n_results, len(self.documents))
        distances, indices = self.index.search(query_embedding, n_results)

        # Format results
        formatted_results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):  # Valid index
                formatted_results.append({
                    'content': self.documents[idx],
                    'metadata': self.metadata[idx],
                    'distance': float(distances[0][i]),
                    'similarity': 1 / (1 + float(distances[0][i]))  # Convert distance to similarity
                })

        return formatted_results

    def get_stats(self) -> Dict:
        """Get vector store statistics."""
        return {
            'total_documents': len(self.documents),
            'embedding_model': 'all-MiniLM-L6-v2',
            'embedding_dim': self.embedding_dim,
            'persist_directory': str(self.persist_directory),
            'index_size_mb': self.index_path.stat().st_size / (1024*1024) if self.index_path.exists() else 0
        }

    def clear_collection(self):
        """Clear all documents from the collection (use with caution!)."""
        self._create_new_index()
        if self.index_path.exists():
            self.index_path.unlink()
        if self.metadata_path.exists():
            self.metadata_path.unlink()
        print("Collection cleared successfully")


# Utility function for testing
def test_vector_store(documents: List[Dict[str, str]] = None):
    """Test the vector store with sample documents."""
    vector_store = SUMOVectorStore()

    if documents:
        print("\nAdding documents...")
        vector_store.add_documents(documents)

    print("\nVector Store Statistics:")
    stats = vector_store.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Test search
    print("\nTesting search with query: 'traffic lights'")
    results = vector_store.search("traffic lights", n_results=3)

    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"  Title: {result['metadata']['title']}")
        print(f"  Category: {result['metadata']['category']}")
        print(f"  File: {result['metadata']['file_path']}")
        print(f"  Similarity: {result['similarity']:.3f}")
        print(f"  Preview: {result['content'][:200]}...")

    return vector_store


if __name__ == "__main__":
    # Test the vector store
    test_vector_store()
