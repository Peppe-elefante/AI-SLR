import google.generativeai as genai
import logging
from dotenv import load_dotenv
import json

logging.basicConfig(level=logging.INFO)
load_dotenv()


class SummaryAgent():
    def __init__(self):
        genai.configure()
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def ask_question(self, agent_data):
        logging.info("logging agent_data" + json.dumps(agent_data, indent=2))
        question = agent_data.get("question")
        answers = "\n".join(agent_data.get("answers"))
        prompt = self._make_prompt(question, answers)
        response = self.model.generate_content(prompt)
        logging.info("logging response:" + str(response))
        return response.text
    
    def _make_prompt(self, question, data):
        return f"""You are an expert researcher performing a comprehensive literature review. Your task is to provide a well-supported answer to the question: '{question}'.
                Utilize the following collected study data as the basis for your response, focusing on identifying key themes, findings, and any relevant discrepancies or convergences within the information:
                **Collected Data:**
                {data}"""





