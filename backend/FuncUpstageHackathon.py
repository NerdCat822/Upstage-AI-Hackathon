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
import json
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import requests
from predibase import Predibase
import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
load_dotenv()

upstage_api_key = os.environ.get('UPSTAGE_API_KEY')
langchain_api_key = os.environ.get("LANGCHAIN_API_KEY")
predibase_api_key = os.environ.get("PREDIBASE_API_KEY")

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

    # question = "Here is the receipt information.\n" + receipt_json_string + "\nMy Job is Software Engineer. Give me the Tax Refund Estimate. and explain why you think about that."
    question = """
    You are a tax deduction calculator specialized in the Australian tax system. Based on the provided receipts and occupation, calculate the potential tax deduction.

    occupation: Software Engineer

    receipt details:
    Item: Transport
    Amount: 15.9 AUD

    Please provide a detailed explanation of how much of this amount is deductible and why.
    """
    
    pb = Predibase(api_token=predibase_api_key)

    lorax_client = pb.deployments.client("solar-1-mini-chat-240612")
    fine_response = lorax_client.generate(question, adapter_id="deduction-guides-model/7", max_new_tokens=100).generated_text

    
    return fine_response

def Tax_Self_RAG(receipt, query):
    # Add more files if you'd like to.
    # receipt: pdf, uploaded_files
    receipt_json = json.dumps(receipt)
    # refined_information = finetuned_model(receipt_information) # fine
    layzer = UpstageLayoutAnalysisLoader(
    "pdfs/gstr2002-005c6.pdf", use_ocr=True, output_type="html"
    )
    # For improved memory efficiency, consider using the lazy_load method to load documents page by page.
    docs = layzer.load()  # or layzer.lazy_load()
    llm = ChatUpstage()
    prompt_template = PromptTemplate.from_template(
        """
        Please provide most correct answer from the following context. 
        If the answer is not present in the context, please write "The information is not present in the context."
        ---
        Question: {question}
        }
        ---
        Context: {Context}
        Receipt: {Receipt}
        """
    )
    chain = prompt_template | llm | StrOutputParser()
    
    
    
    # db: VectorStore = Chroma(embedding_function=UpstageEmbeddings(model="solar-embedding-1-large"))
    # retriever = db.as_retriever()
    # db.add_documents(docs)

    
    text_splitter = RecursiveCharacterTextSplitter.from_language(
    chunk_size=1000, chunk_overlap=100, language=Language.HTML)

    splits = text_splitter.split_documents(docs)

    retriever = BM25Retriever.from_documents(splits)
    
    context_docs = retriever.invoke(query)

    groundedness_check = UpstageGroundednessCheck()
    
    answer = chain.invoke({"input": query,
                           "Receipt": receipt_json, 
                           "Context": context_docs})
    
    #gc_response = groundedness_check.invoke({"context": context_docs, 
    #                                         "answer": answer})
    
    #print("GC check result: ", gc_response)
    #if gc_response.lower().startswith("grounded"):
    #    print("✅ Groundedness check passed")
    #else:
    #    print("❌ Groundedness check failed")

    #chat_history += [HumanMessage(query), AIMessage(gc_response)]

    return answer

receipt_json = Get_Receipt_Information("receipt_data/accounted for in spreadsheet/US, Syd Jan-Mar trip 2024 accounted for in spreadsheet/NSW Transport receipts/Screenshot_20240413-131854.png")
print(fine_tuned_model(receipt_json=receipt_json))