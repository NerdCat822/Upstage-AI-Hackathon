from predibase import Predibase, FinetuningConfig, DeploymentConfig

api_token = "pb_DxAFlDvTXviUE9BQ3iyPCw"
pb = Predibase(api_token=api_token)
lorax_client = pb.deployments.client("solar-1-mini-chat-240612")
print(lorax_client.generate("What is Tax?", adapter_id="tax-guides-model/5", max_new_tokens=100).generated_text)
