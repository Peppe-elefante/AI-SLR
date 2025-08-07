from docling.chunking import HierarchicalChunker
from docling.document_converter import DocumentConverter
from fastembed import TextEmbedding
import random
import os
from typing import Dict, Tuple, List, Generator, Optional
import logging
import uuid

logging.basicConfig(level=logging.INFO)


class StudyPDF():
    def __init__(self, filepath: str):
        """Initialize Class with filepath, chunker and converter"""
        self.name = os.path.basename(filepath)
        self.filepath = filepath
        self.chunker = HierarchicalChunker()
        self.converter = DocumentConverter()
        self._doc = None
        self._chunks = None
        logging.info(f"Initialized StudyPDF with file: {self.name}")

    def _load_if_needed(self):
        """Load document and chunks only when needed"""
        if self._chunks is None:
            try:
                self._doc = self.converter.convert(self.filepath).document
                self._chunks = self.chunker.chunk(self._doc)
            except Exception as e:
                raise RuntimeError(f"Failed to process {self.name}: {e}")
            
    def _get_chunk_texts(self) -> Generator[str, None, None]:
        """Generator that yields chunk texts without storing all in memory"""
        self._load_if_needed()
        for chunk in self._chunks:
            if len(chunk.text) > 275:
                logging.info(f"Processing chunk: {chunk.text}")
                yield chunk.text
        
    def return_embeddings(self, text_model: TextEmbedding):
        chunks = [chunk.text for chunk in self._get_chunk_texts()]
        embeddings = list(text_model.embed(chunks))
        random_id = [random.randint(100000, 999999) for i in range(len(chunks))]
        return dict(zip(random_id, zip(embeddings, chunks)))
    
    def return_embeddings(self, text_model: TextEmbedding) -> Dict[int, Tuple[List[float], str]]:
        """
        Returns a dictionary mapping chunk uuid indices to (embedding, chunk text).
        """
        chunks = list(self._get_chunk_texts())
        embeddings = list(text_model.embed(chunks))
        return {str(uuid.uuid4()): (embedding, chunk) for  (embedding, chunk) in zip(embeddings, chunks)}




