import streamlit as st
from openai import OpenAI
import config
from ui.sidebar import render_sidebar

st.set_page_config(page_title="CrucibleAI", page_icon="🔥", layout="wide")

# Render modular sidebar and capture its return values
sarcasm_level, uploaded_file = render_sidebar()

st.title("CrucibleAI — The Condescending Tutor")

client = OpenAI(base_url=config.OLLAMA_BASE_URL, api_key="ollama")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": config.SYSTEM_PROMPT},
        {"role": "assistant", "content": "Oh good, another student. What glaring gap in your knowledge are we fixing today?"}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question, try not to embarrass yourself..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Note: Later, you will dynamically update the system prompt using the sarcasm_level variable here before calling the LLM.

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})