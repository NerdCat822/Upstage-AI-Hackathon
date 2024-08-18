from pprint import pprint
import os
import getpass
from typing import List
from langchain_core.documents import Document
from langchain_upstage import UpstageLayoutAnalysisLoader
from langchain_chroma import Chroma
from langchain_upstage import ChatUpstage, UpstageEmbeddings
from langchain_core.vectorstores import VectorStore
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_upstage import UpstageGroundednessCheck
from langchain_core.prompts import PromptTemplate
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from langchain_community.chat_models import ChatOpenAI
import json
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.vectorstores import Chroma, FAISS
from langchain.storage import LocalFileStore
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain.callbacks import StreamingStdOutCallbackHandler
import requests
from predibase import Predibase
import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
load_dotenv()

upstage_api_key = os.environ.get('UPSTAGE_API_KEY')
langchain_api_key = os.environ.get("LANGCHAIN_API_KEY")
predibase_api_key = os.environ.get("PREDIBASE_API_KEY")
openai_api_key = os.environ.get('OPENAI_API_KEY')

def Get_Receipt_Information(Receipt):
    # Receipt = "receipt_data/accounted for in spreadsheet/korea trip accounted receipts/Sydney 30-10 Transport.jpg"   # Replace with any other document
    url = f"https://api.upstage.ai/v1/document-ai/extraction"
    headers = {"Authorization": f"Bearer {upstage_api_key}"}
    files = {"document": open(Receipt, "rb")}
    data = {"model": "receipt-extraction"}
    response = requests.post(url, headers=headers, files=files, data=data)
    # resonse.json() : {'apiVersion': '1.1', 'confidence': 0.6918, 'documentType': 'receipt', 'fields': [{'confidence': 0.1497, 'id': 0, 'key': 'store.store_name', 'refinedValue': 'NSW GOVERNMENT for NSW'
    return response.json()

def fine_tuned_model(receipt_json):
    receipt_json_string = json.dumps(receipt_json)
    question = "Here is the receipt information.\n" + receipt_json_string + "\nGive me the Tax Refund Estimate. and explain why you think about that."
    pb = Predibase(api_token=predibase_api_key)

    lorax_client = pb.deployments.client("solar-1-mini-chat-240612")

    fine_response = lorax_client.generate(
        question,
        adapter_id="tax-guides-model/5",
    ).generated_text

    return fine_response

def Tax_Self_RAG(receipt, query):
    # Add more files if you'd like to.
    # receipt: pdf, uploaded_files
    
    receipt_json_string = json.dumps(receipt)
    # refined_information = finetuned_model(receipt_information) # fine
    #layzer = UpstageLayoutAnalysisLoader(
    #"pdfs/Individual_tax_return_instructions_2024.pdf", use_ocr=True, output_type="html"
    #)

    # For improved memory efficiency, consider using the lazy_load method to load documents page by page.
    #docs = layzer.load()  # or layzer.lazy_load()
    llm = ChatUpstage()
    
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size = 600,
        chunk_overlap=100,
    )
    prompt_template = PromptTemplate.from_template(
        """
        Please provide most correct answer from the following context. 
        If the answer is not present in the context, please write "The information is not present in the context."
        ---
        Question: {question}
        ---
        """
    )
    chain = prompt_template | llm | StrOutputParser()
    
    # db: VectorStore = Chroma(embedding_function=UpstageEmbeddings(model="solar-embedding-1-large"))
    # retriever = db.as_retriever()
    # db.add_documents(docs)
    
    
    loader = PyPDFLoader("pdfs/Australia_tax_guide_2020.pdf") # pdf loader

    docs = loader.load_and_split(text_splitter=splitter)
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(docs, embeddings)
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="refine", # 그 외에도 refine, map_reduce, map_rerank 존재
        retriever=vectorstore.as_retriever(),   
    )

    answer = chain.invoke("Here is the receipt\n" + receipt_json_string + query)
    #gc_response = groundedness_check.invoke({"context": context_docs, "answer": answer})
    
    #print("GC check result: ", gc_response)
    #if gc_response.lower().startswith("grounded"):
    #    print("✅ Groundedness check passed")
    #else:
    #    print("❌ Groundedness check failed")
    return answer

receipt_json = Get_Receipt_Information("receipt_data/accounted for in spreadsheet/korea trip accounted receipts/Sydney 16 Oct Pharmacy_page-0001.jpg")
print(Tax_Self_RAG(receipt = receipt_json, 
                   query = "Tell me GSTR 2000/10")['result'])
