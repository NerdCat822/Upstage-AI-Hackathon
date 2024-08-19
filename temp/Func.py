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

def Get_Receipt_Information(Receipt):
    # Receipt = "receipt_data/accounted for in spreadsheet/korea trip accounted receipts/Sydney 30-10 Transport.jpg"   # Replace with any other document
    url = f"https://api.upstage.ai/v1/document-ai/extraction"
    headers = {"Authorization": f"Bearer {upstage_api_key}"}
    files = {"document": open(Receipt, "rb")}
    data = {"model": "receipt-extraction"}
    response = requests.post(url, headers=headers, files=files, data=data)
    # resonse.json() : {'apiVersion': '1.1', 'confidence': 0.6918, 'documentType': 'receipt', 'fields': [{'confidence': 0.1497, 'id': 0, 'key': 'store.store_name', 'refinedValue': 'NSW GOVERNMENT for NSW'
    return response.json()


def Emb_RAG(query, name, tfn, answer1, answer2, answer3, answer4, 
            answer5, answer6, answer7, answer8, answer9, answer10, 
            answer11, answer12, answer13, answer14, answer15_1, answer15_2, answer16_1, answer16_2, 
            answer17_1, answer17_2, answer18, answer19_1, answer19_2, answer19_3, answer20, answer21, 
            answer22_1, answer22_2, answer23_1, answer23_2, answer24_1, answer24_2, answer25_1, answer25_2, 
            answer26_1, answer26_2, answer27_1, answer27_2, answer28_1, answer28_2, answer29_1, answer29_2, answer30_1, answer30_2):
    
    cache_dir = LocalFileStore("./.cache/")

    layzer = UpstageLayoutAnalysisLoader(
    "deduction_pdfs/Deductions_merged.pdf", use_ocr=True, output_type="html"
    )
    docs = layzer.load()
    # 2. Split
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        chunk_size=1000, chunk_overlap=100, language=Language.HTML
    )
    splits = text_splitter.split_documents(docs)
    # 3. Embed & indexing
    embedding=UpstageEmbeddings(model="solar-embedding-1-large")
    cached_embedding = CacheBackedEmbeddings.from_bytes_store(embedding, cache_dir)

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=cached_embedding,
    )

    retriever = vectorstore.as_retriever()
    # retriever_docs = retriever.invoke(query)
    llm = ChatUpstage()
    
    prompt = PromptTemplate(
        template = """
        Please provide most correct answer from the following context. 
        Think step by step and look the html tags and table values carefully to provide the most correct answer.
        If the answer is not present in the context, please write "The information is not present in the context."
        ---
        Question: {question}
        ---
        Context: {Context}
        Here is the personalized information.
        Name: {name},
        TFN(Tax File Number): {tfn},
        1. Were you an Australian resident for tax purposes from 1 July 2023 to 30 June 2024?: {answer1},
        2. Did you have a spouse at any time between 1 July 2023 and 30 June 2024?: {answer2},
        3. You received salary, wages or other income on an income statement/payment summary, Australian Government payments, or First home super saver (FHSS) scheme payment: {answer3},
        4. You had income from Australian superannuation or annuity funds: {answer4},
        5. You had Australian interest, or other Australian income or losses from investments or property: {answer5},
        6. You had managed fund or trust distributions (including where distribution has capital gains and foreign income): {answer6},
        7. You were a sole trader or had business income or losses or partnership distributions: {answer7},
        8. You had foreign income: {answer8},
        9. You had other income not listed above (including employee share schemes) all other income: {answer9},
        10. You had deductions you want to claim: {answer10},
        11. You had tax losses of earlier income years tax loses of earlier income years: {answer11},
        12. You are claiming tax offsets or adjustments: {answer12},
        13. Income statements and payment summaries - Occupation where you earned most income: {answer13},
        14. Salary, wages, allowances, tips ,bonusses etc- Select the companies from which you received dividends: {answer14},
        15. Interest - 1. Enter the bank name 1: {answer15_1}, 2. Enter the interest income from: {answer15_2},
        16. Dividends - 1. Enter the company name 1: {answer16_1}, 2. Enter the dividend income from: {answer16_2},
        17. Other income - 1. Enter the other income source name 1: {answer17_1}, 2. Enter the other income from: {answer17_2},
        18. Income tests - Number of dependent children: {answer18},
        19. Medicare and private health insurance - 1. Medicare levy exemption or reduction: {answer19_1}, 2. Medicare levy surcharge: {answer19_2}, 3. Private health insurance policies: {answer19_3},
        20. How did you complete this tax return?: {answer20},
        21. Will you need to lodge an Australian tax return in future years?: {answer21},
        22. Work-related car expenses - 1. Your description for car expense: {answer22_1}, 2. Amount $ for car expense: {answer22_2},
        23. Work-related travel expenses - 1. Your description for travel expense: {answer23_1}, 2. Amount $ for travel expense: {answer23_2},
        24. Work-related clothing, laundry, and dry-cleaning expenses - 1. Your description for clothing expense: {answer24_1}, 2. Amount $ for clothing expense: {answer24_2},
        25. Work-related self-education expenses - 1. Your description for education expense: {answer25_1}, 2. Amount $ for education expense: {answer25_2},
        26. Other work-related expenses - 1. Your description for other work-related expense: {answer26_1}, 2. Amount $ for other work-related expense: {answer26_2},
        27. Interest Deductions - 1. Your description for interest deduction: {answer27_1}, 2. Amount $ for interest deduction: {answer27_2},
        28. Dividend deductions - 1. Your description for dividend deduction: {answer28_1}, 2. Amount $ for dividend deduction: {answer28_2},
        29. Gifts or donations - 1. Your description for gift or donation: {answer29_1}, 2. Amount $ for gift or donation: {answer29_2},
        30. Cost of managing tax affairs - 1. Your description for managing tax affairs: {answer30_1}, 2. Amount $ for managing tax affairs: {answer30_2}
        """,
        input_variables=["question", "Context", "name", "tfn", 
                         "answer1", "answer2", "answer3", "answer4", "answer5", "answer6",
                         "answer7", "answer8", "answer9", "answer10", "answer11", "answer12",
                         "answer13", "answer14", "answer15_1", "answer15_2", "answer16_1", "answer16_2",
                         "answer17_1", "answer17_2", "answer18", "answer19_1", "answer19_2", "answer19_3",
                         "answer20", "answer21", "answer22_1", "answer22_2", "answer23_1", "answer23_2", "answer24_1",
                         "answer24_2", "answer25_1", "answer25_2", "answer26_1", "answer26_2", "answer27_1", "answer27_2",
                         "answer28_1", "answer28_2", "answer29_1", "answer29_2", "answer30_1", "answer30_2"]
    )

    setup_and_retrieval = RunnableParallel(
    {"Context": retriever, "question": RunnablePassthrough()}
    )
    rag_chain = setup_and_retrieval | prompt | llm | StrOutputParser()

    answer = rag_chain.invoke({"question": query, "Context": retriever, "name": name, "tfn": tfn, "answer1": answer1, 
    "answer2": answer2, "answer3": answer3, "answer4": answer4,"answer5": answer5, 
    "answer6": answer6,"answer7": answer7, "answer8": answer8, "answer9": answer9, 
    "answer10": answer10,"answer11": answer11, "answer12": answer12, "answer13": answer13,
    "answer14": answer14, "answer15_1": answer15_1, "answer15_2": answer15_2,"answer16_1": answer16_1, 
    "answer16_2": answer16_2, "answer17_1": answer17_1,"answer17_2": answer17_2, "answer18": answer18, 
    "answer19_1": answer19_1, "answer19_2": answer19_2, "answer19_3": answer19_3, "answer20": answer20, 
    "answer21": answer21, "answer22_1": answer22_1, "answer22_2": answer22_2, "answer23_1": answer23_1, 
    "answer23_2": answer23_2, "answer24_1": answer24_1, "answer24_2": answer24_2, "answer25_1": answer25_1, 
    "answer25_2": answer25_2, "answer26_1": answer26_1, "answer26_2": answer26_2, "answer27_1": answer27_1, 
    "answer27_2": answer27_2, "answer28_1": answer28_1, "answer28_2": answer28_2, "answer29_1": answer29_1, 
    "answer29_2": answer29_2, "answer30_1": answer30_1, "answer30_2": answer30_2
})
    

    return answer

def Self_RAG(query, name, tfn, answer1, answer2, answer3, answer4, 
            answer5, answer6, answer7, answer8, answer9, answer10, 
            answer11, answer12, answer13, answer14, answer15_1, answer15_2, answer16_1, answer16_2, 
            answer17_1, answer17_2, answer18, answer19_1, answer19_2, answer19_3, answer20, answer21, 
            answer22_1, answer22_2, answer23_1, answer23_2, answer24_1, answer24_2, answer25_1, answer25_2, 
            answer26_1, answer26_2, answer27_1, answer27_2, answer28_1, answer28_2, answer29_1, answer29_2, answer30_1, answer30_2):
    
    cache_dir = LocalFileStore("./.cache/")

    layzer = UpstageLayoutAnalysisLoader(
    "deduction_pdfs/Deductions_merged.pdf", use_ocr=True, output_type="html"
    )
    docs = layzer.load()
    # 2. Split
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        chunk_size=1000, chunk_overlap=100, language=Language.HTML
    )
    splits = text_splitter.split_documents(docs)
    # 3. Embed & indexing
    embedding=UpstageEmbeddings(model="solar-embedding-1-large")
    cached_embedding = CacheBackedEmbeddings.from_bytes_store(embedding, cache_dir)

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=cached_embedding,
    )

    retriever = vectorstore.as_retriever()
    # retriever_docs = retriever.invoke(query)
    llm = ChatUpstage()
    
    
    prompt = PromptTemplate(
        template = """
        Please provide most correct answer from the following context. 
        Think step by step and look the html tags and table values carefully to provide the most correct answer.
        If the answer is not present in the context, please write "The information is not present in the context."
        ---
        Question: {question}
        ---
        Context: {Context}
        Here is the personalized information.
        Name: {name},
        TFN(Tax File Number): {tfn},
        1. Were you an Australian resident for tax purposes from 1 July 2023 to 30 June 2024?: {answer1},
        2. Did you have a spouse at any time between 1 July 2023 and 30 June 2024?: {answer2},
        3. You received salary, wages or other income on an income statement/payment summary, Australian Government payments, or First home super saver (FHSS) scheme payment: {answer3},
        4. You had income from Australian superannuation or annuity funds: {answer4},
        5. You had Australian interest, or other Australian income or losses from investments or property: {answer5},
        6. You had managed fund or trust distributions (including where distribution has capital gains and foreign income): {answer6},
        7. You were a sole trader or had business income or losses or partnership distributions: {answer7},
        8. You had foreign income: {answer8},
        9. You had other income not listed above (including employee share schemes) all other income: {answer9},
        10. You had deductions you want to claim: {answer10},
        11. You had tax losses of earlier income years tax loses of earlier income years: {answer11},
        12. You are claiming tax offsets or adjustments: {answer12},
        13. Income statements and payment summaries - Occupation where you earned most income: {answer13},
        14. Salary, wages, allowances, tips ,bonusses etc- Select the companies from which you received dividends: {answer14},
        15. Interest - 1. Enter the bank name 1: {answer15_1}, 2. Enter the interest income from: {answer15_2},
        16. Dividends - 1. Enter the company name 1: {answer16_1}, 2. Enter the dividend income from: {answer16_2},
        17. Other income - 1. Enter the other income source name 1: {answer17_1}, 2. Enter the other income from: {answer17_2},
        18. Income tests - Number of dependent children: {answer18},
        19. Medicare and private health insurance - 1. Medicare levy exemption or reduction: {answer19_1}, 2. Medicare levy surcharge: {answer19_2}, 3. Private health insurance policies: {answer19_3},
        20. How did you complete this tax return?: {answer20},
        21. Will you need to lodge an Australian tax return in future years?: {answer21},
        22. Work-related car expenses - 1. Your description for car expense: {answer22_1}, 2. Amount $ for car expense: {answer22_2},
        23. Work-related travel expenses - 1. Your description for travel expense: {answer23_1}, 2. Amount $ for travel expense: {answer23_2},
        24. Work-related clothing, laundry, and dry-cleaning expenses - 1. Your description for clothing expense: {answer24_1}, 2. Amount $ for clothing expense: {answer24_2},
        25. Work-related self-education expenses - 1. Your description for education expense: {answer25_1}, 2. Amount $ for education expense: {answer25_2},
        26. Other work-related expenses - 1. Your description for other work-related expense: {answer26_1}, 2. Amount $ for other work-related expense: {answer26_2},
        27. Interest Deductions - 1. Your description for interest deduction: {answer27_1}, 2. Amount $ for interest deduction: {answer27_2},
        28. Dividend deductions - 1. Your description for dividend deduction: {answer28_1}, 2. Amount $ for dividend deduction: {answer28_2},
        29. Gifts or donations - 1. Your description for gift or donation: {answer29_1}, 2. Amount $ for gift or donation: {answer29_2},
        30. Cost of managing tax affairs - 1. Your description for managing tax affairs: {answer30_1}, 2. Amount $ for managing tax affairs: {answer30_2}
        """,
        input_variables=["question", "Context", "name", "tfn", 
                         "answer1", "answer2", "answer3", "answer4", "answer5", "answer6",
                         "answer7", "answer8", "answer9", "answer10", "answer11", "answer12",
                         "answer13", "answer14", "answer15_1", "answer15_2", "answer16_1", "answer16_2",
                         "answer17_1", "answer17_2", "answer18", "answer19_1", "answer19_2", "answer19_3",
                         "answer20", "answer21", "answer22_1", "answer22_2", "answer23_1", "answer23_2", "answer24_1",
                         "answer24_2", "answer25_1", "answer25_2", "answer26_1", "answer26_2", "answer27_1", "answer27_2",
                         "answer28_1", "answer28_2", "answer29_1", "answer29_2", "answer30_1", "answer30_2"]
    )

    chain = prompt | llm | StrOutputParser()
    
    context_docs = retriever.invoke(query)

    answer = chain.invoke({"question": query, "Context": context_docs, "name": name, "tfn": tfn, "answer1": answer1, 
    "answer2": answer2, "answer3": answer3, "answer4": answer4,"answer5": answer5, 
    "answer6": answer6,"answer7": answer7, "answer8": answer8, "answer9": answer9, 
    "answer10": answer10,"answer11": answer11, "answer12": answer12, "answer13": answer13,
    "answer14": answer14, "answer15_1": answer15_1, "answer15_2": answer15_2,"answer16_1": answer16_1, 
    "answer16_2": answer16_2, "answer17_1": answer17_1,"answer17_2": answer17_2, "answer18": answer18, 
    "answer19_1": answer19_1, "answer19_2": answer19_2, "answer19_3": answer19_3, "answer20": answer20, 
    "answer21": answer21, "answer22_1": answer22_1, "answer22_2": answer22_2, "answer23_1": answer23_1, 
    "answer23_2": answer23_2, "answer24_1": answer24_1, "answer24_2": answer24_2, "answer25_1": answer25_1, 
    "answer25_2": answer25_2, "answer26_1": answer26_1, "answer26_2": answer26_2, "answer27_1": answer27_1, 
    "answer27_2": answer27_2, "answer28_1": answer28_1, "answer28_2": answer28_2, "answer29_1": answer29_1, 
    "answer29_2": answer29_2, "answer30_1": answer30_1, "answer30_2": answer30_2})
    groundedness_check = UpstageGroundednessCheck()
    gc_result = groundedness_check.invoke({"context": context_docs, "answer": answer})


    if gc_result.lower().startswith("grounded"):
        print("✅ Groundedness check passed")
        answer = gc_result
    else:
        print("❌ Groundedness check failed")
        answer = gc_result
    return answer

def RAG(query, name, tfn, answer1, answer2, answer3, answer4, 
            answer5, answer6, answer7, answer8, answer9, answer10, 
            answer11, answer12, answer13, answer14, answer15_1, answer15_2, answer16_1, answer16_2, 
            answer17_1, answer17_2, answer18, answer19_1, answer19_2, answer19_3, answer20, answer21, 
            answer22_1, answer22_2, answer23_1, answer23_2, answer24_1, answer24_2, answer25_1, answer25_2, 
            answer26_1, answer26_2, answer27_1, answer27_2, answer28_1, answer28_2, answer29_1, answer29_2, answer30_1, answer30_2):

    layzer = UpstageLayoutAnalysisLoader(
    "deduction_pdfs/Deductions_merged.pdf", use_ocr=True, output_type="html"
    )
    docs = layzer.load()
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        chunk_size=1000, chunk_overlap=100, language=Language.HTML
    )
    splits = text_splitter.split_documents(docs)

    retriever = BM25Retriever.from_documents(splits)
    context_docs = retriever.invoke(query)
    llm = ChatUpstage()

    prompt = PromptTemplate(
        template = """
        Please provide most correct answer from the following context. 
        Think step by step and look the html tags and table values carefully to provide the most correct answer.
        If the answer is not present in the context, please write "The information is not present in the context."
        ---
        Question: {question}
        ---
        Context: {Context}
        Here is the personalized information.
        Name: {name},
        TFN(Tax File Number): {tfn},
        1. Were you an Australian resident for tax purposes from 1 July 2023 to 30 June 2024?: {answer1},
        2. Did you have a spouse at any time between 1 July 2023 and 30 June 2024?: {answer2},
        3. You received salary, wages or other income on an income statement/payment summary, Australian Government payments, or First home super saver (FHSS) scheme payment: {answer3},
        4. You had income from Australian superannuation or annuity funds: {answer4},
        5. You had Australian interest, or other Australian income or losses from investments or property: {answer5},
        6. You had managed fund or trust distributions (including where distribution has capital gains and foreign income): {answer6},
        7. You were a sole trader or had business income or losses or partnership distributions: {answer7},
        8. You had foreign income: {answer8},
        9. You had other income not listed above (including employee share schemes) all other income: {answer9},
        10. You had deductions you want to claim: {answer10},
        11. You had tax losses of earlier income years tax loses of earlier income years: {answer11},
        12. You are claiming tax offsets or adjustments: {answer12},
        13. Income statements and payment summaries - Occupation where you earned most income: {answer13},
        14. Salary, wages, allowances, tips ,bonusses etc- Select the companies from which you received dividends: {answer14},
        15. Interest - 1. Enter the bank name 1: {answer15_1}, 2. Enter the interest income from: {answer15_2},
        16. Dividends - 1. Enter the company name 1: {answer16_1}, 2. Enter the dividend income from: {answer16_2},
        17. Other income - 1. Enter the other income source name 1: {answer17_1}, 2. Enter the other income from: {answer17_2},
        18. Income tests - Number of dependent children: {answer18},
        19. Medicare and private health insurance - 1. Medicare levy exemption or reduction: {answer19_1}, 2. Medicare levy surcharge: {answer19_2}, 3. Private health insurance policies: {answer19_3},
        20. How did you complete this tax return?: {answer20},
        21. Will you need to lodge an Australian tax return in future years?: {answer21},
        22. Work-related car expenses - 1. Your description for car expense: {answer22_1}, 2. Amount $ for car expense: {answer22_2},
        23. Work-related travel expenses - 1. Your description for travel expense: {answer23_1}, 2. Amount $ for travel expense: {answer23_2},
        24. Work-related clothing, laundry, and dry-cleaning expenses - 1. Your description for clothing expense: {answer24_1}, 2. Amount $ for clothing expense: {answer24_2},
        25. Work-related self-education expenses - 1. Your description for education expense: {answer25_1}, 2. Amount $ for education expense: {answer25_2},
        26. Other work-related expenses - 1. Your description for other work-related expense: {answer26_1}, 2. Amount $ for other work-related expense: {answer26_2},
        27. Interest Deductions - 1. Your description for interest deduction: {answer27_1}, 2. Amount $ for interest deduction: {answer27_2},
        28. Dividend deductions - 1. Your description for dividend deduction: {answer28_1}, 2. Amount $ for dividend deduction: {answer28_2},
        29. Gifts or donations - 1. Your description for gift or donation: {answer29_1}, 2. Amount $ for gift or donation: {answer29_2},
        30. Cost of managing tax affairs - 1. Your description for managing tax affairs: {answer30_1}, 2. Amount $ for managing tax affairs: {answer30_2}
        """,
        input_variables=["question", "Context", "name", "tfn", 
                         "answer1", "answer2", "answer3", "answer4", "answer5", "answer6",
                         "answer7", "answer8", "answer9", "answer10", "answer11", "answer12",
                         "answer13", "answer14", "answer15_1", "answer15_2", "answer16_1", "answer16_2",
                         "answer17_1", "answer17_2", "answer18", "answer19_1", "answer19_2", "answer19_3",
                         "answer20", "answer21", "answer22_1", "answer22_2", "answer23_1", "answer23_2", "answer24_1",
                         "answer24_2", "answer25_1", "answer25_2", "answer26_1", "answer26_2", "answer27_1", "answer27_2",
                         "answer28_1", "answer28_2", "answer29_1", "answer29_2", "answer30_1", "answer30_2"]
    )

    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"question": query, "Context": context_docs, "name": name, "tfn": tfn, "answer1": answer1, 
    "answer2": answer2, "answer3": answer3, "answer4": answer4,"answer5": answer5, 
    "answer6": answer6,"answer7": answer7, "answer8": answer8, "answer9": answer9, 
    "answer10": answer10,"answer11": answer11, "answer12": answer12, "answer13": answer13,
    "answer14": answer14, "answer15_1": answer15_1, "answer15_2": answer15_2,"answer16_1": answer16_1, 
    "answer16_2": answer16_2, "answer17_1": answer17_1,"answer17_2": answer17_2, "answer18": answer18, 
    "answer19_1": answer19_1, "answer19_2": answer19_2, "answer19_3": answer19_3, "answer20": answer20, 
    "answer21": answer21, "answer22_1": answer22_1, "answer22_2": answer22_2, "answer23_1": answer23_1, 
    "answer23_2": answer23_2, "answer24_1": answer24_1, "answer24_2": answer24_2, "answer25_1": answer25_1, 
    "answer25_2": answer25_2, "answer26_1": answer26_1, "answer26_2": answer26_2, "answer27_1": answer27_1, 
    "answer27_2": answer27_2, "answer28_1": answer28_1, "answer28_2": answer28_2, "answer29_1": answer29_1, 
    "answer29_2": answer29_2, "answer30_1": answer30_1, "answer30_2": answer30_2})
    return answer

receipt_json = Get_Receipt_Information("receipt_data/accounted for in spreadsheet/US, Syd Jan-Mar trip 2024 accounted for in spreadsheet/NSW Transport receipts/Screenshot_20240413-131854.png")

