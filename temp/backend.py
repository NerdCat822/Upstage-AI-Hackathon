from fastapi import FastAPI
from pydantic import BaseModel
from Func import *

class InputQuery(BaseModel):
    text: str

app = FastAPI()


# 여러 문자열 데이터를 받을 데이터 모델 정의
class InputData(BaseModel):
    inputs: List[str]  # 문자열 리스트로 받음



@app.post("/SelfRAG")
def PostSelfRAG(data: InputData):

    response = Self_RAG(
        data.inputs[0], data.inputs[1], data.inputs[2], data.inputs[3], 
        data.inputs[4], data.inputs[5], data.inputs[6], data.inputs[7],
        data.inputs[8], data.inputs[9], data.inputs[10], data.inputs[11],
        data.inputs[12], data.inputs[13], data.inputs[14], data.inputs[15],
        data.inputs[16], data.inputs[17], data.inputs[18], data.inputs[19],
        data.inputs[20], data.inputs[21], data.inputs[22], data.inputs[23],
        data.inputs[24], data.inputs[25], data.inputs[26], data.inputs[27],
        data.inputs[28], data.inputs[29], data.inputs[30], data.inputs[31],
        data.inputs[32], data.inputs[33], data.inputs[34], data.inputs[35],
        data.inputs[36], data.inputs[37], data.inputs[38], data.inputs[39], 
        data.inputs[40], data.inputs[41], data.inputs[42], data.inputs[43], 
        data.inputs[44], data.inputs[45], data.inputs[46]
    )
    
    return {"response": response}

@app.post("/EmbRAG")
def PostEmbRAG(query, name, tfn, answer1, answer2, answer3, answer4, 
            answer5, answer6, answer7, answer8, answer9, answer10, 
            answer11, answer12, answer13, answer14, answer15_1, answer15_2, answer16_1, answer16_2, 
            answer17_1, answer17_2, answer18, answer19_1, answer19_2, answer19_3, answer20, answer21, 
            answer22_1, answer22_2, answer23_1, answer23_2, answer24_1, answer24_2, answer25_1, answer25_2, 
            answer26_1, answer26_2, answer27_1, answer27_2, answer28_1, answer28_2, answer29_1, answer29_2, answer30_1, answer30_2):
    response = Emb_RAG(query, name, tfn, answer1, answer2, answer3, answer4, 
            answer5, answer6, answer7, answer8, answer9, answer10, 
            answer11, answer12, answer13, answer14, answer15_1, answer15_2, answer16_1, answer16_2, 
            answer17_1, answer17_2, answer18, answer19_1, answer19_2, answer19_3, answer20, answer21, 
            answer22_1, answer22_2, answer23_1, answer23_2, answer24_1, answer24_2, answer25_1, answer25_2, 
            answer26_1, answer26_2, answer27_1, answer27_2, answer28_1, answer28_2, answer29_1, answer29_2, answer30_1, answer30_2)
    return {"reponse": response}

@app.post("/RAG")
def PostRAG(data: InputData):
    response = RAG(
        data.inputs[0], data.inputs[1], data.inputs[2], data.inputs[3], 
        data.inputs[4], data.inputs[5], data.inputs[6], data.inputs[7],
        data.inputs[8], data.inputs[9], data.inputs[10], data.inputs[11],
        data.inputs[12], data.inputs[13], data.inputs[14], data.inputs[15],
        data.inputs[16], data.inputs[17], data.inputs[18], data.inputs[19],
        data.inputs[20], data.inputs[21], data.inputs[22], data.inputs[23],
        data.inputs[24], data.inputs[25], data.inputs[26], data.inputs[27],
        data.inputs[28], data.inputs[29], data.inputs[30], data.inputs[31],
        data.inputs[32], data.inputs[33], data.inputs[34], data.inputs[35],
        data.inputs[36], data.inputs[37], data.inputs[38], data.inputs[39], 
        data.inputs[40], data.inputs[41], data.inputs[42], data.inputs[43], 
        data.inputs[44], data.inputs[45], data.inputs[46]
    )
    return {"reponse": response}
