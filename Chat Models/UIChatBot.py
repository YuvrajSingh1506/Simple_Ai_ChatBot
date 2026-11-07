import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# ---------- Page setup ----------
st.set_page_config(page_title="Funny AI Agent", page_icon="🎭", layout="centered")

# ---------- Model (same settings as before) ----------
@st.cache_resource
def get_model():
    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        max_output_tokens=300,
        timeout=30,
        max_retries=1,
    )

model = get_model()

# ---------- Message history (same roles as before) ----------
if "message" not in st.session_state:
    st.session_state.message = [
        SystemMessage(content="You are a funny AI Agent ")
    ]
message = st.session_state.message

# ---------- Header ----------
st.title("🎭 Funny AI Agent")
st.caption("Welcome! Type 0 to exit the application.")

# ---------- Show chat history ----------
for msg in message:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

# ---------- Input ----------
prompt = st.chat_input("Type your message here...")

if prompt:
    if prompt == "0":
        st.info("Chat ended. Goodbye! 👋")
        st.stop()

    message.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.invoke(message)
        reply = response.content[0]["text"]
        st.write(reply)

    message.append(AIMessage(content=reply))