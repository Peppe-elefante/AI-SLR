from docling.chunking import HierarchicalChunker
from docling.document_converter import DocumentConverter
from fastembed import TextEmbedding
import random
import os

class StudyPDF():
    def __init__(self, filepath: str):
        self.name = os.path.basename(filepath)
        self.chunker = HierarchicalChunker()
        self.converter = DocumentConverter()
        self.doc = self.converter.convert(filepath).document
        self.chunks = self.chunker.chunk(self.doc)
        
    def return_embeddings(self, text_model: TextEmbedding):
        chunks = [chunk.text for chunk in self.chunks]
        embeddings = list(text_model.embed(chunks))
        random_id = [random.randint(100000, 999999) for i in range(len(chunks))]
        return dict(zip(random_id, zip(embeddings, chunks)))




