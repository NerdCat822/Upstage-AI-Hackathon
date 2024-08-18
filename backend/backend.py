from fastapi import FastAPI
from pydantic import BaseModel
from FuncUpstageHackathon import *

class InputQuery(BaseModel):
    text: str

app = FastAPI()

"""
@app.post("/GetReceipt")
def PostGetReceipt(receipt):
    # receipt: jpg format
    response = Get_Receipt_Information(receipt)
    return response
"""

@app.post("/TaxSelfRAG")
def PostTaxSelfRAG(receipt, input: InputQuery):
    receipt_infromation = Get_Receipt_Information(receipt)
    response = Tax_Self_RAG(receipt=receipt_infromation, 
                            query=input.text)
    return {"reponse": response}