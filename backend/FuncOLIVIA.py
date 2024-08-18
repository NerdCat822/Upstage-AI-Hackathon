from predibase import Predibase
from dotenv import load_dotenv
import os

load_dotenv()

def fine_tuned_model(question: str):

    api_token = os.getenv('PREDIBASE_API_KEY')

    pb = Predibase(api_token=api_token)

    lorax_client = pb.deployments.client("solar-1-mini-chat-240612")

    fine_response = lorax_client.generate(
        question,
        adapter_id="tax-guides-model/5",
    ).generated_text

    return fine_response