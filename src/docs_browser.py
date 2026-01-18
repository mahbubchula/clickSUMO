"""
Documentation Browser Module
=============================

Provides browsing, searching, and navigation of SUMO documentation.

Features:
- Category-based browsing
- Full-text search
- Document viewer
- Bookmarks/favorites
- Related documents

Author: Mahbub Hassan
Copyright © 2026 Mahbub Hassan
"""

import streamlit as st
from pathlib import Path
from typing import List, Dict, Optional
import json


class DocumentationBrowser:
    """Browser for SUMO documentation with search and navigation."""

    def __init__(self, vector_store=None):
        """
        Initialize documentation browser.

        Args:
            vector_store: SUMOVectorStore instance for search functionality
        """
        self.vector_store = vector_store
        self.bookmarks_file = Path("user_data/bookmarks.json")
        self.bookmarks_file.parent.mkdir(exist_ok=True)

        # Initialize session state for bookmarks
        if 'doc_bookmarks' not in st.session_state:
            st.session_state.doc_bookmarks = self._load_bookmarks()

    def _load_bookmarks(self) -> List[Dict]:
        """Load bookmarks from file."""
        if self.bookmarks_file.exists():
            try:
                with open(self.bookmarks_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_bookmarks(self):
        """Save bookmarks to file."""
        with open(self.bookmarks_file, 'w') as f:
            json.dump(st.session_state.doc_bookmarks, f, indent=2)

    def add_bookmark(self, title: str, category: str, url: str):
        """Add a document to bookmarks."""
        bookmark = {
            'title': title,
            'category': category,
            'url': url
        }
        if bookmark not in st.session_state.doc_bookmarks:
            st.session_state.doc_bookmarks.append(bookmark)
            self._save_bookmarks()
            return True
        return False

    def remove_bookmark(self, title: str):
        """Remove a document from bookmarks."""
        st.session_state.doc_bookmarks = [
            b for b in st.session_state.doc_bookmarks if b['title'] != title
        ]
        self._save_bookmarks()

    def is_bookmarked(self, title: str) -> bool:
        """Check if a document is bookmarked."""
        return any(b['title'] == title for b in st.session_state.doc_bookmarks)

    def get_categories(self) -> Dict[str, int]:
        """Get all documentation categories with document counts."""
        if not self.vector_store:
            return {}

        categories = {}
        for metadata in self.vector_store.metadata:
            cat = metadata.get('category', 'Uncategorized')
            categories[cat] = categories.get(cat, 0) + 1

        return dict(sorted(categories.items()))

    def get_documents_by_category(self, category: str) -> List[Dict]:
        """Get all documents in a specific category."""
        if not self.vector_store:
            return []

        docs = []
        for i, metadata in enumerate(self.vector_store.metadata):
            if metadata.get('category') == category:
                docs.append({
                    'title': metadata['title'],
                    'category': metadata['category'],
                    'url': metadata['url'],
                    'file': metadata['file_path'],
                    'preview': self.vector_store.documents[i][:200] + '...'
                })

        return sorted(docs, key=lambda x: x['title'])

    def search_documents(self, query: str, n_results: int = 10) -> List[Dict]:
        """
        Search documents using semantic search.

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            List of matching documents with metadata
        """
        if not self.vector_store or not query:
            return []

        results = self.vector_store.search(query, n_results=n_results)

        formatted = []
        for result in results:
            formatted.append({
                'title': result['metadata']['title'],
                'category': result['metadata']['category'],
                'url': result['metadata']['url'],
                'file': result['metadata']['file_path'],
                'preview': result['content'][:300] + '...',
                'similarity': result.get('similarity', 0)
            })

        return formatted

    def get_document_content(self, title: str) -> Optional[Dict]:
        """Get full content of a specific document."""
        if not self.vector_store:
            return None

        for i, metadata in enumerate(self.vector_store.metadata):
            if metadata['title'] == title:
                return {
                    'title': metadata['title'],
                    'category': metadata['category'],
                    'url': metadata['url'],
                    'file': metadata['file_path'],
                    'content': self.vector_store.documents[i]
                }

        return None

    def find_related_documents(self, title: str, n_results: int = 5) -> List[Dict]:
        """Find documents related to the given document."""
        doc = self.get_document_content(title)
        if not doc:
            return []

        # Use first 500 chars as query to find similar docs
        query = doc['content'][:500]
        results = self.search_documents(query, n_results=n_results + 1)

        # Filter out the original document
        return [r for r in results if r['title'] != title][:n_results]
