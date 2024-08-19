import streamlit as st
import os
from predibase import Predibase, FinetuningConfig, DeploymentConfig

st.set_page_config(page_title="User/Company Multi-Page App", layout="wide")

# 챗봇 섹션
st.title("Refund Ranger Chatbot")

# 사용자에게 입력받을 occupation 변수
occupation = st.text_input("What is your occupation?")

# 이메일 주소 입력 (옵셔널)
email = st.text_input("What is your email address? (optional) ", placeholder="example@example.com")


# 시스템 메시지 추가
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": f"You are a helper for Australian Tax Refund, especially connecting occupations to deduction lists. The customer's job title is: {occupation}.",
        },
        {
            "role": "system",
            "content": (
                f"According to the Australian Tax Office (ATO), the job title '{occupation}' must be classified into one of the following ATO occupation categories: "
                "Adult industry workers, Agricultural workers, Apprentices and trainees, Australian Defence Force members, "
                "Building and construction employees, Bus drivers, Call centre operators, Cleaners, Community support workers and direct carers, "
                "Doctor, specialist or other medical professionals, Factory workers, Fire fighters, Fitness and sporting industry employees, "
                "Flight crew, Gaming attendants, Guards and security employees, Hairdressers and beauty professionals, "
                "Hospitality industry employees, Lawyers, Meat workers, Media professionals, Mining site employees, Nurses and midwives, "
                "Paramedics, Performing artists, Pilots, Police officers, Professional sportspersons, Real estate employees, Recruitment consultants, "
                "Retail industry workers, Sales and marketing managers, Teachers and education professionals, Tradespersons, Train drivers, "
                "Travel agent employees, Truck drivers, IT Professionals, Office workers, Engineers. "
                "Please provide occupation category descriptions using full text labels and avoid numerical codes unless specifically requested."
            ),
        },
        {
            "role": "system",
            "content": (
                "When providing responses, base all answers strictly on the ATO's official individual tax refund guidelines. "
                "Do not reference any information that is not directly derived from the ATO's official documentation."
            ),
        },
        {
            "role": "assistant",
            "content": "From your occupation, I can suggest some potential deductions. Would you like to know?" ?",
        },
    ]

# 이전 메시지 출력 (시스템 메시지는 제외)
for msg in st.session_state.messages:
    if msg["role"] != "system":  # 시스템 메시지를 출력하지 않음
        st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 처리
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Predibase 모델 호출
    response = lorax_client.generate(
        prompt,
        adapter_id=adapter_id,
        max_new_tokens=1000,  # 필요에 따라 조정 가능
    ).generated_text

    # # 아니면 여기에 RAG response로 대체 
    # response = run_rag_model(prompt, occupation)
    # 모델 응답 처리 및 출력
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
