# backend.py
from pydantic import BaseModel
from Func import RAG

# InputData 클래스를 통해 데이터를 받아 처리하는 것처럼 구현
class InputData(BaseModel):
    occupation: str
    prompt: str

# FastAPI의 엔드포인트 함수를 일반 함수로 변경
def process_rag(data: InputData):
    response = RAG(data.prompt, data.occupation)
    return {"response": response}
