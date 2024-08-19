ReturnRanger
===
![image](https://github.com/user-attachments/assets/00b77793-73af-4fd9-b2c6-973ae84a2339)

# Local Setup
## Installation Method
1. First make a virtual environment as needed, and install required packages. We're using ```Python 3.11.9```
```bash
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create a ```.env``` file and add the following API keys.
You can get a ```LANGCHAIN_API_KEY``` at [Langchain Settings](https://smith.langchain.com/settings).

```bash
UPSTAGE_API_KEY='xxxxxxxxxx'
PREDIBASE_API_KEY='xxxxxxxxxx'
LANGCHAIN_API_KEY='xxxxxxxxxx'
```

## Usage Instructions
1. Then run the Streamlit app with,
```bash
streamlit run main.py
```

# Streamlit Community Cloud Setup
### Enter the API keys in Streamlit Community Cloud
To set the API keys as an environment variable in Streamlit apps, do the following:

1. At the lower right corner, click on `< Manage app` then click on the vertical "..." followed by clicking on `Settings`.
2. This brings the **App settings**, next click on the `Secrets` tab and paste the API key into the text box as follows:

```bash
UPSTAGE_API_KEY='xxxxxxxxxx'
PREDIBASE_API_KEY='xxxxxxxxxx'
LANGCHAIN_API_KEY='xxxxxxxxxx'
```

# Project Overview
![image](https://github.com/user-attachments/assets/c7365103-7de9-4230-b1b4-ed66b5ed64a0)

## Problem: How can we empower anyone in doing their own tax return easily?
<img width="1720" alt="image" src="https://github.com/user-attachments/assets/cb6a1fac-7490-49e8-bc3e-39a181baee36">
<img width="1509" alt="image" src="https://github.com/user-attachments/assets/0f5b9d2c-f3bd-4ac3-b3ad-98c2f5ce648e">
<img width="1728" alt="image" src="https://github.com/user-attachments/assets/8f688c9e-ae6f-4ae0-bd02-92bc601ee7de">
<img width="1728" alt="image" src="https://github.com/user-attachments/assets/ecfba190-8dc2-48ea-99cc-c31cde1dcab0">

---
# Solution
<img width="1728" alt="image" src="https://github.com/user-attachments/assets/f27d1022-81e9-4a74-a985-aca84bf0d135">
<img width="1728" alt="image" src="https://github.com/user-attachments/assets/2a26582b-00d0-4b90-98f6-af8d29970feb">

- Chatbot that provides suggestions on tax returns.
    - Superior search for the latest Australian Tax Office (ATO) legislation and more niche info from ATO Community Forums.
    - Offers interactable features for in-depth clarification to help users maximize their tax return.
---
## Upstage API Usage
- Chat: for user interactions/query
- Embeddings for RAG
- Layout Analysis for data ingestion and chunking
- Fine-tuned SolarLLM to produce a SolarLLM-Australian-Tax expert
Soon integrated:
- Translation: for non-English speaking Korean Australians
- Groundedness Check: for math calculations and judgements - reduce hallucinations.
- Key Information Extraction: for receipt scanning

1. Embedding RAG
    - Layout Analyzer for PDF Documents
    - Solar Embedding-1-large for discovering RAG
    - Vector Database for Efficient data storage and speed
2. Chatbot with fine-tuned Model
    - Fine-tuning SolarLLM via Predibase
    - StreamLit for Python frontend
---
### Upstage Technology
**1. Layout Analysis**

![Layout+Analysis_WebHero_1600x900](https://github.com/user-attachments/assets/786bcf20-b340-49bb-aa62-2572c8670ce7)
- The Layout Analyzer is a tool that accurately recognizes and separates various document elements such as headers, footers, paragraphs, captions, tables, and images. It enables clean data extraction by identifying each element distinctly.
- Convert documents to maximize RAG performance
- LangChain provides powerful tools for text splitting and vectorization


**2. Upstage Solar Embedding**

<img width="954" alt="59" src="https://github.com/user-attachments/assets/221bc90e-741a-4dd1-b117-f10d811fcb36">
- Solar Embedding-1-large outperforms OpenAI's text-embedding-3-large, delivering superior results across English, Korean, and Japanese languages.
- designed to tackle complex challenges and revolutionize search systems with its innovative embedding capabilities.
- Offering exceptional performance at an affordable price, Solar Embedding-1-large sets a new benchmark for embedding models.


**3. Groundedness Check**

<img width="1250" alt="9" src="https://github.com/user-attachments/assets/6ccd57e1-e1d9-40e1-a7d6-d0b13b568b57">
- Groundedness Check enhances system reliability by validating the accuracy of answers before presenting them to the user.
- This final step ensures precision and reduces the risk of misinformation or hallucination to nearly zero.

-----------------------------------------

# Inspiration
One of our teammates, Joey, has been doing Australian tax returns himself – spending hours doing it and efforts throughout the year to gather his records.
and the 18+ Australian professionals we surveyed (and likely the growing 3.5 million who do it themselves) – resonated with that.

# Challenges
## Technical Challenges
- Tech Support - especially Ryker was a massive lifesaver.

- Math calculations/reasoning with SolarLLM: produced incorrect judgements (e.g. $129 > $300), used Groundedness check to validate further.

- Self-RAG: Refresh problem in Streamlit with Groundedness Check: Worked fine in backend, but not when integrated with frontend. Solution was to rewrite the frontend with another framework, but didn't have time to fix - removed feature.

- RAG response latency: experimented with different vector databases and chunking techniques until a decent response of 2-4 seconds was achieved.

- Uncertainty on whether to RAG or fine-tune with our 5 potential data-sources: sought tech support, reasoned based on how frequent and dense the data-sources were and approached accordingly.

- Confusion between when to use Document OCR, Layout Analysis, and Key Info Extraction: Tech Support validated our intuitions and elaborated on Layout Analysis flexibility (e.g. even with non-selectable contents in PDFs).

- Lack of enforced version control causing merge-conflicts: due to miscommunication and some inexperienced member made codebase overwritten twice. We found a way to get along.

## Non-technical Challenges
- Squeezing a 3 week hackathon into 4 days.
- Working in a team of strangers remotely, and keeping morale up.
- Collaborating across different cultural and language differences (Two S.Koreans, One Australian).
- Reaching alignment in problem and product understanding.
- Reducing scope appropriately to still achieve MVP (3 top requested key features) when things went wrong and broke.

# Made with love by
![05b3386b50b9b664057302a69accc5b2-11](https://github.com/user-attachments/assets/3edd5ffc-9d24-4c10-9364-be1af163cb89)
