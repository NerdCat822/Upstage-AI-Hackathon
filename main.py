# main.py
import streamlit as st
from backend import process_rag, InputData
from predibase import Predibase, FinetuningConfig, DeploymentConfig


st.set_page_config(page_title="User/Company Multi-Page App", layout="wide")

# 챗봇 섹션
st.title("Refund Ranger Chatbot")

# 사용자에게 입력받을 occupation 변수
occupation = st.text_input("What is your occupation?")

# 이메일 주소 입력 (옵셔널)
email = st.text_input("What is your email address? (optional)", placeholder="example@example.com")

st.title("Your occupation's deduction strategy")
if occupation:
    prompt = """Based on the occupation provided by the user, 
    please recommend common deductions that individuals in this specific occupation might be eligible for according to the official Occupation and Industry Specific Guides for completing an Australian tax return. 
    Include any relevant examples or conditions that apply to these deductions."""
    input_data = InputData(occupation=occupation, prompt=prompt)
    response_rag = process_rag(input_data)
    st.write(response_rag["response"])
    
# 시스템 메시지 추가
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

# 이전 메시지 출력 (시스템 메시지는 제외)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 처리
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # InputData 객체 생성
    # input_data = InputData(occupation=occupation, prompt=prompt)

    # backend.py의 process_rag 함수 호출
    # response = process_rag(input_data)
    # Predibase 모델 호출
    pb = Predibase(api_token="pb_DxAFlDvTXviUE9BQ3iyPCw")  # "pb_DxAFlDvTXviUE9BQ3iyPCw")


    # Predibase 모델 설정
    adapter_id = "Occup-deduc-guides-model/11"  # 실제 사용 중인 모델의 어댑터 ID로 교체
    lorax_client = pb.deployments.client(
        "solar-1-mini-chat-240612"
    )  # 실제 클라이언트 설정으로 교체

    response = lorax_client.generate(
        prompt,
        adapter_id=adapter_id,
        max_new_tokens=1000,  # 필요에 따라 조정 가능
    ).generated_text
    
    # 모델 응답 처리 및 출력
    # st.session_state.messages.append({"role": "assistant", "content": response["response"]})
    # st.chat_message("assistant").write(response["response"])
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)