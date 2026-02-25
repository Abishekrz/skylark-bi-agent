import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="Monday BI Agent", layout="wide")

st.title("📊 Monday.com Business Intelligence Agent")
st.markdown("Ask founder-level business questions about pipeline, revenue, sectors, and execution.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask your question:")

if st.button("Submit") and user_input:
    try:
        response = requests.get(
            BACKEND_URL,
            params={"question": user_input}
        )

        if response.status_code == 200:
            data = response.json()
            summary = data.get("executive_summary", "No response generated.")
        else:
            summary = "Error communicating with backend."

    except Exception as e:
        summary = f"Connection error: {str(e)}"

    st.session_state.chat_history.append(
        {"question": user_input, "answer": summary}
    )

for chat in reversed(st.session_state.chat_history):
    st.markdown("---")
    st.markdown(f"**🧑 Question:** {chat['question']}")
    st.markdown(f"**🤖 Answer:**")
    st.text(chat["answer"])