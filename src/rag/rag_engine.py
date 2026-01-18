"""
SUMO RAG Engine
===============

Retrieval-Augmented Generation engine that combines
SUMO documentation search with AI-powered responses.

Author: Mahbub Hassan
Copyright © 2026 Mahbub Hassan
"""

from typing import List, Dict, Tuple
from groq import Groq
from .doc_parser import SUMODocParser
from .vector_store import SUMOVectorStore


class SUMORagEngine:
    """RAG engine for answering questions about SUMO using official documentation."""

    def __init__(self, api_key: str, docs_path: str = r"D:\02_Research_&_Projects\Research_Ideas_&_Related_Documents\sumo_documentation\docs"):
        """
        Initialize the RAG engine.

        Args:
            api_key: Groq API key
            docs_path: Path to SUMO documentation
        """
        self.api_key = api_key
        self.docs_path = docs_path
        self.vector_store = None
        self.groq_client = Groq(api_key=api_key)

        # Check if vector store exists
        try:
            self.vector_store = SUMOVectorStore()
            if self.vector_store.get_stats()['total_documents'] == 0:
                print("Vector store is empty. Run initialize() to build it.")
        except Exception as e:
            print(f"Vector store not initialized: {e}")

    def initialize(self, max_docs: int = None):
        """
        Build the vector store from SUMO documentation.

        Args:
            max_docs: Maximum number of documents to process (for testing)
        """
        print("Initializing RAG system...")
        print("Step 1: Parsing documentation...")

        parser = SUMODocParser(self.docs_path)
        documents = parser.parse_all_docs(max_files=max_docs)

        print(f"\nStep 2: Building vector database...")
        self.vector_store = SUMOVectorStore()
        self.vector_store.add_documents(documents)

        print("\nRAG system initialized successfully!")
        return self.vector_store.get_stats()

    def query(
        self,
        question: str,
        n_results: int = 3,
        model: str = "llama-3.3-70b-versatile"
    ) -> Dict[str, any]:
        """
        Answer a question using RAG.

        Args:
            question: User's question
            n_results: Number of relevant docs to retrieve
            model: Groq model to use

        Returns:
            Dictionary with answer and sources
        """
        if not self.vector_store:
            return {
                'answer': "RAG system not initialized. Please wait for indexing to complete.",
                'sources': [],
                'error': True
            }

        # Step 1: Retrieve relevant documents
        relevant_docs = self.vector_store.search(question, n_results=n_results)

        if not relevant_docs:
            return {
                'answer': "I couldn't find relevant information in the SUMO documentation for your question.",
                'sources': [],
                'error': False
            }

        # Step 2: Build context from retrieved documents
        context = self._build_context(relevant_docs)

        # Step 3: Generate answer using Groq
        answer = self._generate_answer(question, context, model)

        # Step 4: Format sources
        sources = self._format_sources(relevant_docs)

        return {
            'answer': answer,
            'sources': sources,
            'error': False
        }

    def _build_context(self, documents: List[Dict]) -> str:
        """Build context string from retrieved documents."""
        context_parts = []

        for i, doc in enumerate(documents, 1):
            title = doc['metadata']['title']
            content = doc['content'][:1000]  # Limit content length
            file_path = doc['metadata']['file_path']

            context_parts.append(
                f"[Document {i}: {title}]\n"
                f"Source: {file_path}\n"
                f"Content: {content}\n"
            )

        return "\n\n".join(context_parts)

    def _generate_answer(self, question: str, context: str, model: str) -> str:
        """Generate answer using Groq API."""
        system_prompt = """You are an expert assistant for SUMO (Simulation of Urban Mobility) traffic simulation.
You have access to SUMO's official documentation.

When answering questions:
1. Base your answers on the provided documentation context
2. Be specific and accurate
3. Include practical examples when relevant
4. If the context doesn't contain enough information, say so
5. Format your response in clear markdown
6. Use bullet points and code blocks where appropriate

Remember: You're helping users learn and use SUMO effectively."""

        user_prompt = f"""Based on the following SUMO documentation excerpts, please answer this question:

Question: {question}

Documentation Context:
{context}

Please provide a clear, accurate answer based on the documentation above."""

        try:
            response = self.groq_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Lower temperature for more factual responses
                max_tokens=1500
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating response: {str(e)}"

    def _format_sources(self, documents: List[Dict]) -> List[Dict[str, str]]:
        """Format source citations."""
        sources = []

        for doc in documents:
            sources.append({
                'title': doc['metadata']['title'],
                'file': doc['metadata']['file_path'],
                'url': doc['metadata']['url'],
                'category': doc['metadata']['category'],
                'preview': doc['content'][:200] + "..."
            })

        return sources

    def get_status(self) -> Dict:
        """Get RAG system status."""
        if not self.vector_store:
            return {
                'initialized': False,
                'total_documents': 0,
                'ready': False
            }

        stats = self.vector_store.get_stats()
        return {
            'initialized': True,
            'total_documents': stats['total_documents'],
            'ready': stats['total_documents'] > 0
        }


# Utility function for testing
def test_rag_engine(api_key: str):
    """Test the RAG engine."""
    print("Testing RAG Engine...")

    engine = SUMORagEngine(api_key)

    # Initialize with a small subset for testing
    print("\nInitializing with sample documents...")
    stats = engine.initialize(max_docs=20)
    print(f"Indexed {stats['total_documents']} documents")

    # Test queries
    test_questions = [
        "How do I create a simple network in SUMO?",
        "What are the different car-following models available?",
        "How do traffic lights work in SUMO?"
    ]

    for question in test_questions:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print('='*60)

        result = engine.query(question)

        print(f"\nAnswer:\n{result['answer']}")

        print(f"\nSources ({len(result['sources'])}):")
        for i, source in enumerate(result['sources'], 1):
            print(f"  {i}. {source['title']} ({source['category']})")
            print(f"     File: {source['file']}")

    return engine


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv('GROQ_API_KEY')

    if api_key:
        test_rag_engine(api_key)
    else:
        print("Please set GROQ_API_KEY environment variable")
