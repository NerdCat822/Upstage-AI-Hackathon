import streamlit as st
from backend import process_rag, InputData
from predibase import Predibase, FinetuningConfig, DeploymentConfig


st.set_page_config(page_title="User/Company Multi-Page App", layout="wide")

# Chatbot Section
st.title("Refund Ranger Chatbot")

# Occupation variables to be entered by the user
occupation = st.text_input("What is your occupation?")

# Enter email address (optional)
email = st.text_input("What is your email address? (optional)", placeholder="example@example.com")

st.title("Your occupation's deduction strategy")
if occupation and "response_rag_displayed" not in st.session_state:
    prompt = """Based on the occupation provided by the user, 
    please recommend common deductions that individuals in this specific occupation might be eligible for according to the official Occupation and Industry Specific Guides for completing an Australian tax return. 
    Include any relevant examples or conditions that apply to these deductions."""
    input_data = InputData(occupation=occupation, prompt=prompt)
    response_rag = process_rag(input_data)
    st.write(response_rag["response"])
    st.session_state.response_rag_displayed = True  # Record that it has already been displayed

# add the system messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": f"You are a helper for Australian Tax Refund, especially connecting occupations to deduction lists. The customer's job title is: {occupation}.",
        },
        {
            "role": "assistant",
            "content": "From your occupation, I can suggest some potential deductions. Would you like to know?",
        },
    ]

# Print previous messages (excluding system messages)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# User input processing
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Chatbot response processing
    pb = Predibase(api_token="Your token")

    # Predibase model setup
    adapter_id = "Occup-deduc-guides-model/11"
    lorax_client = pb.deployments.client("solar-1-mini-chat-240612")

    response = lorax_client.generate(
        prompt,
        adapter_id=adapter_id,
        max_new_tokens=1000,
    ).generated_text

    # Model response processing and output
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
