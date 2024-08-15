#@title set API key
from pprint import pprint
import os
import getpass
from typing import List
from langchain_core.documents import Document
from langchain_upstage import UpstageLayoutAnalysisLoader
import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
load_dotenv()

upstage_api_key = os.environ.get('UPSTAGE_API_KEY')
langchain_api_key = os.environ.get("LANGCHAIN_API_KEY")


def layout_analysis(filenames: str) -> List[Document]:
    layout_analysis_loader = UpstageLayoutAnalysisLoader(filenames, split="element")
    return layout_analysis_loader.load()

# Add more files if you'd like to.
filenames = [
    "pdfs/Upstage_Solar_DUS.pdf",
]

docs = layout_analysis(filenames)
print(f'number of documents: {len(docs)}')
print(docs[0])

from langchain_chroma import Chroma
from langchain_upstage import ChatUpstage, UpstageEmbeddings
from langchain_core.vectorstores import VectorStore

db: VectorStore = Chroma(embedding_function=UpstageEmbeddings(model="solar-embedding-1-large"))
retriever = db.as_retriever()
db.add_documents(docs)

from typing import TypedDict

class RagState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        context: retrieved context
        question: question asked by the user
        answer: generated answer to the question
        groundedness: groundedness of the assistant's response
    """
    context: str
    question: str
    answer: str
    groundedness: str

from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate


template = '''Answer the question based only on the given context.
{context}

Question: {question}
'''

prompt = ChatPromptTemplate.from_template(template)
model = ChatUpstage()

# Solar model answer generation, given the context and question
model_chain = prompt | model | StrOutputParser()

def format_documents(docs: List[Document]) -> str:
    return "\n".join([doc.page_content for doc in docs])
    
def retrieve(state: RagState) -> RagState:
    docs = retriever.invoke(state['question'])
    context = format_documents(docs)
    return RagState(context=context)

def model_answer(state: RagState) -> RagState:
    response = model_chain.invoke(state)
    return RagState(answer=response)

from langchain_upstage import GroundednessCheck

gc = GroundednessCheck()

def groundedness_check(state: RagState) -> RagState:
    response = gc.run({"context": state['context'], "answer": state['answer']})
    return RagState(groundedness=response)

def groundedness_condition(state: RagState) -> RagState:
    return state['groundedness']

from langgraph.graph import END, StateGraph

workflow = StateGraph(RagState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("model", model_answer)
workflow.add_node("groundedness_check", groundedness_check)

workflow.add_edge("retrieve", "model")
workflow.add_edge("model", "groundedness_check")
workflow.add_conditional_edges("groundedness_check", groundedness_condition, {
    "grounded": END,
    "notGrounded": "model",
    "notSure": "model",
})
workflow.set_entry_point("retrieve")

app = workflow.compile()

inputs = {"question": "What is Solar?"}
for output in app.stream(inputs):
    for key, value in output.items():
        print(f"Node '{key}':{value}")
    print("\n---\n")