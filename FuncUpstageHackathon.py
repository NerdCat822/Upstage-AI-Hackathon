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

import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
load_dotenv()

upstage_api_key = os.environ.get('UPSTAGE_API_KEY')
langchain_api_key = os.environ.get("LANGCHAIN_API_KEY")


def Tax_Self_RAG(receipt, query):
    # Add more files if you'd like to.
    # receipt: pdf, Needed or not OCR
    layzer = UpstageLayoutAnalysisLoader(
    "pdfs/Australia_tax_guide_2020.pdf", use_ocr=True, output_type="html"
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
        ---
        Context: {Context}
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
    answer = chain.invoke({"question": query, "Context": context_docs})
    gc_response = groundedness_check.invoke({"context": context_docs, "answer": answer})
    
    print("GC check result: ", gc_response)
    if gc_response.lower().startswith("grounded"):
        print("✅ Groundedness check passed")
    else:
        print("❌ Groundedness check failed")
    return gc_response
    