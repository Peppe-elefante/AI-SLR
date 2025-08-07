from dotenv import load_dotenv
import os
from qdrant_client.models import Distance, VectorParams
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import logging
from fastembed import TextEmbedding


logging.basicConfig(level=logging.INFO)
load_dotenv()



class Qdrant():
    def __init__(self):
        self.client = QdrantClient(os.getenv("QDRANT_URL"))
        self.collection_name = "tesi"
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.DOT),
        )



    def add_embeddings(self, embeddings: dict, pdf_name: str):
        points = []
        for i,c in embeddings.items():
            points.append(PointStruct(id = i, vector=c, payload = {"title": pdf_name}))
        operation_info = self.client.upsert(
            collection_name="tesi",
            wait=True,
            points=points,
        )
        logging.info(operation_info)
        

    def query(self, question, text_model : TextEmbedding):
        query = list(text_model.embed(question))[0]
        search_result = self.client.query_points(
        collection_name=self.collection_name,
        query=query,
        with_payload=True,
        with_vectors=True,
        limit=5
        ).points

        return search_result

    def clear_db(self):
        self.client.delete_collection(collection_name=self.collection_name)