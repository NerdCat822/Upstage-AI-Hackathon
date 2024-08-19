# Func.py
from pprint import pprint
import os
from langchain_upstage import UpstageLayoutAnalysisLoader, ChatUpstage, UpstageGroundednessCheck
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain.storage import LocalFileStore
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
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import CacheBackedEmbeddings

import json
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
import requests
import predibase
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferWindowMemory
from operator import itemgetter

from langchain_community.llms import Predibase
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain.storage import LocalFileStore

import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
load_dotenv()

upstage_api_key = os.environ.get('UPSTAGE_API_KEY')
langchain_api_key = os.environ.get("LANGCHAIN_API_KEY")
predibase_api_key = os.environ.get("PREDIBASE_API_KEY")


def RAG(query, occupation):
    # 문서 로드
    layzer = UpstageLayoutAnalysisLoader(
        "deduction_pdfs/Deductions_merged.pdf", use_ocr=True, output_type="html"
    )
    docs = layzer.load()
    cache_dir = LocalFileStore("./.cache/")
    # 문서 분할
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        chunk_size=1000, chunk_overlap=100, language=Language.HTML
    )
    splits = text_splitter.split_documents(docs)

    embedding=UpstageEmbeddings(model="solar-embedding-1-large")
    cached_embedding = CacheBackedEmbeddings.from_bytes_store(embedding, cache_dir)

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=cached_embedding,
    )

    retriever = vectorstore.as_retriever()
    # 문서 검색기
    #retriever = BM25Retriever.from_documents(splits)
    #context_docs = retriever.invoke(query)
    
    # 언어 모델 설정
    llm = ChatUpstage()

    # 프롬프트 템플릿
    prompt = PromptTemplate(
        template = """
        Please provide the most correct answer from the following context.
        Think step by step and look at the html tags and table values carefully to provide the most correct answer.
        ---
        Question: {question}
        ---
        Context: {Context}
        Occupation:""" + occupation,
        input_variables=["question", "Context"]
    )
    
    # 체인 설정
    setup_and_retrieval = RunnableParallel(
        {"Context": retriever, "question": RunnablePassthrough()}
    )
    rag_chain = setup_and_retrieval | prompt | llm | StrOutputParser()

    context_docs = retriever.invoke(query)
    # 답변 생성
    answer = rag_chain.invoke({"question": query, "Context": context_docs})
    
    # 그라운드 체크 수행
    #groundedness_check = UpstageGroundednessCheck()
    #gc_result = groundedness_check.invoke({"context": context_docs, "answer": answer})

    #if gc_result.lower().startswith("grounded"):
    #    print("✅ Groundedness check passed")
    #    answer = gc_result
    #else:
    #    print("❌ Groundedness check failed")
    #    answer = gc_result
    
    return answer
