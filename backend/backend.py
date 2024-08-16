from fastapi import FastAPI
from pydantic import BaseModel
from FuncUpstageHackathon import *

class InputQuery(BaseModel):
    # file: pdf
    text: str

app = FastAPI()

@app.post("/TaxSelfRAG")
def PostTaxSelfRAG(input: InputQuery):
    response = Tax_Self_RAG(input.file, 
                            input.text)
    return {"reponse": response}