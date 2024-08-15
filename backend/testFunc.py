from langchain_upstage import ChatUpstage
from langchain_core.messages import HumanMessage, SystemMessage

chat = ChatUpstage(api_key="up_LVL4P6vqS3wBvbrTY57bxFz9xbiqS")

messages = [
  SystemMessage(content="You are a helpful assistant."),
  HumanMessage(content="Hi, how are you?")
]
response = chat.invoke(messages)
print(response)