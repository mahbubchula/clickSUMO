"""
SUMO Documentation Parser
=========================

Extracts clean text content from SUMO HTML documentation files
for use in the RAG system.

Author: Mahbub Hassan
Copyright © 2026 Mahbub Hassan
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple
from bs4 import BeautifulSoup
import re


class SUMODocParser:
    """Parse SUMO HTML documentation and extract clean text."""

    def __init__(self, docs_path: str = r"D:\02_Research_&_Projects\Research_Ideas_&_Related_Documents\sumo_documentation\docs"):
        """
        Initialize the parser.

        Args:
            docs_path: Path to SUMO documentation folder
        """
        self.docs_path = Path(docs_path)
        if not self.docs_path.exists():
            raise FileNotFoundError(f"Documentation path not found: {docs_path}")

    def parse_html_file(self, file_path: Path) -> Dict[str, str]:
        """
        Parse a single HTML file and extract content.

        Args:
            file_path: Path to HTML file

        Returns:
            Dictionary with title, content, and metadata
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else file_path.stem

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()

            # Extract main content
            # Try to find the main content div
            main_content = soup.find('div', class_=['col-md-9', 'content', 'main'])
            if not main_content:
                main_content = soup.find('body')

            # Get text
            text = main_content.get_text() if main_content else soup.get_text()

            # Clean up text
            text = self._clean_text(text)

            # Get relative path for citation
            rel_path = file_path.relative_to(self.docs_path)

            return {
                'title': title_text,
                'content': text,
                'file_path': str(rel_path),
                'url': str(rel_path).replace('\\', '/'),
                'category': self._get_category(file_path)
            }

        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def _clean_text(self, text: str) -> str:
        """Clean extracted text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove multiple newlines
        text = re.sub(r'\n+', '\n', text)
        # Strip
        text = text.strip()
        return text

    def _get_category(self, file_path: Path) -> str:
        """Determine document category from path."""
        parts = file_path.relative_to(self.docs_path).parts
        if len(parts) > 1:
            return parts[0]  # Top-level folder name
        return "General"

    def parse_all_docs(self, max_files: int = None) -> List[Dict[str, str]]:
        """
        Parse all HTML files in the documentation.

        Args:
            max_files: Maximum number of files to parse (for testing)

        Returns:
            List of parsed documents
        """
        documents = []
        html_files = list(self.docs_path.rglob("*.html"))

        if max_files:
            html_files = html_files[:max_files]

        print(f"Found {len(html_files)} HTML files to parse...")

        for i, file_path in enumerate(html_files):
            if i % 50 == 0:
                print(f"Parsing file {i+1}/{len(html_files)}...")

            doc = self.parse_html_file(file_path)
            if doc and doc['content']:
                documents.append(doc)

        print(f"Successfully parsed {len(documents)} documents")
        return documents

    def get_document_stats(self) -> Dict[str, any]:
        """Get statistics about the documentation."""
        html_files = list(self.docs_path.rglob("*.html"))

        categories = {}
        for file_path in html_files:
            category = self._get_category(file_path)
            categories[category] = categories.get(category, 0) + 1

        return {
            'total_files': len(html_files),
            'categories': categories,
            'docs_path': str(self.docs_path)
        }


# Utility function for quick testing
def test_parser(docs_path: str = "sumo_docs/docs"):
    """Test the parser with a few documents."""
    parser = SUMODocParser(docs_path)

    print("Documentation Statistics:")
    stats = parser.get_document_stats()
    print(f"Total files: {stats['total_files']}")
    print(f"Categories: {list(stats['categories'].keys())}")

    print("\nParsing first 5 documents...")
    docs = parser.parse_all_docs(max_files=5)

    for doc in docs:
        print(f"\nTitle: {doc['title']}")
        print(f"Category: {doc['category']}")
        print(f"Content length: {len(doc['content'])} characters")
        print(f"First 200 chars: {doc['content'][:200]}...")

    return docs


if __name__ == "__main__":
    # Test the parser
    test_parser()
