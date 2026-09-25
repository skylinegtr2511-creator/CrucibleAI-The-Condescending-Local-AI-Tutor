import streamlit as st
from openai import OpenAI

import config
from database import session_store
from parsers.document_loader import extract_text
from ui.sidebar import render_sidebar
from ui.styles import inject_custom_css, render_hero, typing_indicator_html

# ── Page setup ──────────────────────────────────────────────────────────
st.set_page_config(page_title=config.APP_NAME, page_icon=config.APP_ICON, layout="wide")
inject_custom_css()

session_store.init_db()

# ── Sidebar ─────────────────────────────────────────────────────────────
sarcasm_level, uploaded_file, new_chat_clicked, switch_to = render_sidebar()
st.session_state["sarcasm_level"] = sarcasm_level

render_hero()

client = OpenAI(base_url=config.OLLAMA_BASE_URL, api_key="ollama")

# ── Session bootstrapping ──────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = session_store.new_session_id()
    st.session_state.messages = [
        {"role": "assistant", "content": "Oh good, another student. What glaring gap in your knowledge are we fixing today?"}
    ]

if new_chat_clicked:
    st.session_state.session_id = session_store.new_session_id()
    st.session_state.messages = [
        {"role": "assistant", "content": "Back again? Let's see if today goes any better."}
    ]
    st.session_state.pop("document_context", None)
    st.rerun()

if switch_to and switch_to != st.session_state.session_id:
    st.session_state.session_id = switch_to
    st.session_state.messages = session_store.load_messages(switch_to) or [
        {"role": "assistant", "content": "Picking up where we left off. Try to keep up."}
    ]
    st.rerun()

# ── Document grounding ──────────────────────────────────────────────────
if uploaded_file is not None and st.session_state.get("last_uploaded_name") != uploaded_file.name:
    with st.spinner("Reading through this so I can judge it properly..."):
        st.session_state.document_context = extract_text(uploaded_file)
        st.session_state.last_uploaded_name = uploaded_file.name

# ── Render chat history ──────────────────────────────────────────────────
for msg in st.session_state.messages:
    avatar = config.APP_ICON if msg["role"] == "assistant" else "🧑"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ── Chat input ─────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask a question, try not to embarrass yourself..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    session_store.save_message(st.session_state.session_id, "user", prompt)

    # Auto-title fresh sessions from the first message
    sessions = {s["id"]: s for s in session_store.list_sessions()}
    current = sessions.get(st.session_state.session_id)
    if current and current["title"] == "New Chat":
        session_store.rename_session(st.session_state.session_id, prompt[:48])

    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    system_prompt = config.build_system_prompt(
        sarcasm_level, st.session_state.get("document_context")
    )
    api_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

    with st.chat_message("assistant", avatar=config.APP_ICON):
        placeholder = st.empty()
        placeholder.markdown(typing_indicator_html(), unsafe_allow_html=True)
        try:
            stream = client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=api_messages,
                stream=True,
            )
            full_response = ""
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                if delta:
                    full_response += delta
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
        except Exception as exc:  # noqa: BLE001
            full_response = (
                f"*Sighs.* I can't even roast you right now — the model backend "
                f"errored out: `{exc}`. Check that Ollama is running."
            )
            placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    session_store.save_message(st.session_state.session_id, "assistant", full_response)
