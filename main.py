import os
from services.StudyPDF import StudyPDF
from services.Dao import Qdrant
from services.SummaryAgent import SummaryAgent
from fastembed import TextEmbedding
from utils.questions import questions
import logging
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(level=logging.INFO)

def get_studies():
    studies: list[StudyPDF] = []
    folder_path = "./Studi" 
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            studies.append(StudyPDF(filepath))
            logging.info("Added study " + filepath)
    return studies


def main(db: Qdrant):
    embeddings_dict: dict = {} 
    studies: list[StudyPDF] = get_studies()
    model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    agent = SummaryAgent()
    for study in studies:
        embeddings_study = study.return_embeddings(model)
        embeddings = [v[0] for v in embeddings_study.values()]
        embedding_id = [k for k in embeddings_study.keys()]
        db.add_embeddings(dict(zip(embedding_id, embeddings)), study.name)
        embeddings_dict = embeddings_dict | embeddings_study

    for question in questions:
        agent_data = {"question" : question}
        answers = []
        query_result = db.query(question, model)
        for point in query_result:
            answers.append(embeddings_dict.get(point.id)[1])
        agent_data = agent_data | {"answers" : answers}
        with open("output.txt", "a", encoding="utf-8") as f:
            f.write("\n\nQuestion: "+ question +"\n\n" + agent.ask_question(agent_data))
        

    

if __name__ == "__main__":
    try:
        db = Qdrant()
        main(db)
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.clear_db()