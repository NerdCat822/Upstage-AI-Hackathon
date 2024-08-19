from pydantic import BaseModel
from Func import RAG

# InputData By Pydantic
class InputData(BaseModel):
    occupation: str
    prompt: str

# Change FastAPI's endpoint function to a regular function
def process_rag(data: InputData):
    response = RAG(data.prompt, data.occupation)
    return {"response": response}
