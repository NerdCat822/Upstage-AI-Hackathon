# CURL test
import requests
import json

url = "https://serving.app.predibase.com/7ea6d0/deployments/v2/llms/solar-1-mini-chat-240612/generate"
api_token = "pb_DxAFlDvTXviUE9BQ3iyPCw"
adapter_id="tax-guides-model/5"
input_prompt = """
system\nThe following is a guide on tax refunds. Please provide a detailed explanation based on the given scenario.
scenario
I received a tax bill this year even though I usually get a refund. I want to understand why this happened and how to avoid it in the future.
response
"""

payload = {
    "inputs": input_prompt,
    "parameters": {
        "adapter_id": adapter_id,
        "adapter_source": "pbase",
        "max_new_tokens": 20,
        "temperature": 0.1
    }
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_token}"
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.text)
