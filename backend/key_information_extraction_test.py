import requests
import os
from dotenv import load_dotenv
load_dotenv()

upstage_api_key = os.environ.get('UPSTAGE_API_KEY')
filename = "receipt_data/accounted for in spreadsheet/korea trip accounted receipts/Sydney 30-10 Transport.jpg"   # Replace with any other document

url = f"https://api.upstage.ai/v1/document-ai/extraction"
headers = {"Authorization": f"Bearer {upstage_api_key}"}
files = {"document": open(filename, "rb")}
data = {"model": "receipt-extraction"}
response = requests.post(url, headers=headers, files=files, data=data)
print(response.json())