ReturnRanger
===
![05b3386b50b9b664057302a69accc5b2-0](https://github.com/user-attachments/assets/09761ff6-1460-480d-8339-7d03986e7568)

# Project Overview
![05b3386b50b9b664057302a69accc5b2-4](https://github.com/user-attachments/assets/92307778-c932-4f90-aa88-b931d0e3ce4d)
- Vision: Maximise people’s tax returns while minimising the time they spend on it.
- Chatbot that provides guidance on tax returns.
    - Superior search for the latest ATO legislation and comprehensive info from ATO Community Forums.
    - Offers interactable features for in-depth clarification to help users maximize their tax return.
---
# Solution
![05b3386b50b9b664057302a69accc5b2-6](https://github.com/user-attachments/assets/5ee5c8dc-6d8f-4d2f-abcc-509fe382df26)
1. AI Chatbot to maximize tax return
2. Suggestions for deductions based on Occupation
    - Suggestions based on Context provided
---
# Implemented Method
1. Embeding RAG
    - Layout Analyzer for PDF Documents
    - Solar Embedding-1-large for discovering RAG
    - Vector Database for Efficient data storage and speed

2. Chatbot with fine-tuned Model
    - Fine-tuning SolarLLM via Predibase
    - StreamLit for Python frontend
---
# Usage
```bash
streamlit run main.py
```

# Upstage API Used
1. Layout Analysis
![Layout+Analysis_WebHero_1600x900](https://github.com/user-attachments/assets/786bcf20-b340-49bb-aa62-2572c8670ce7)
- The Layout Analyzer is a tool that accurately recognizes and separates various document elements such as headers, footers, paragraphs, captions, tables, and images. It enables clean data extraction by identifying each element distinctly.
- Convert documents to maximize RAG performance
- LangChain provides powerful tools for text splitting and vectorization

2. Upstage Solar Embedding
<img width="954" alt="59" src="https://github.com/user-attachments/assets/221bc90e-741a-4dd1-b117-f10d811fcb36">
- Solar Embedding-1-large outperforms OpenAI's text-embedding-3-large, delivering superior results across English, Korean, and Japanese languages.
- designed to tackle complex challenges and revolutionize search systems with its innovative embedding capabilities.
- Offering exceptional performance at an affordable price, Solar Embedding-1-large sets a new benchmark for embedding models.

3. Groundedness Check
<img width="1250" alt="9" src="https://github.com/user-attachments/assets/6ccd57e1-e1d9-40e1-a7d6-d0b13b568b57">
- Groundedness Check enhances system reliability by validating the accuracy of answers before presenting them to the user.
- This final step ensures precision and reduces the risk of misinformation or hallucination to nearly zero.
-----------------------------------------

## Inspiration

## What it does

## Challenges faced
- Finding the right data
- Groundedness Check Failed

## Accomplishments

## Learnings

## Made by
![05b3386b50b9b664057302a69accc5b2-11](https://github.com/user-attachments/assets/3edd5ffc-9d24-4c10-9364-be1af163cb89)

## What's next
### Technical
- User Authentication for data privacy and security
- Monitoring for usage feedback and metrics
- Stripe for payments towards financial sustainability

### Non-technical
- Get access to Australian Tax Office's API by registering as a digital service provider (DSP)
