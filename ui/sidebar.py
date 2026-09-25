"""
ui/sidebar.py
Sidebar: sarcasm meter, document upload, and chat session history.
Returns everything app.py needs to react to.
"""

import streamlit as st

from config import sarcasm_label
from database import session_store


def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-card"><h4>⚙️ Tutor Settings</h4>',
            unsafe_allow_html=True,
        )
        sarcasm_level = st.slider(
            "Sarcasm Meter",
            min_value=1,
            max_value=10,
            value=st.session_state.get("sarcasm_level", 8),
            help="1 = Mildly Annoyed, 10 = Nuclear",
        )
        st.markdown(
            f'<span class="sarcasm-badge">{sarcasm_level}/10 · {sarcasm_label(sarcasm_level)}</span>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="sidebar-card"><h4>📄 Upload Material</h4>',
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader(
            "Upload a document for me to mock...",
            type=["pdf", "docx", "txt", "csv"],
            label_visibility="collapsed",
        )
        if uploaded_file:
            st.success(f"'{uploaded_file.name}' loaded. Let's see how bad this is.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="sidebar-card"><h4>💬 Chats</h4>', unsafe_allow_html=True
        )
        new_chat_clicked = st.button("➕ New Chat", use_container_width=True, type="primary")

        sessions = session_store.list_sessions()
        switch_to = None
        if sessions:
            for s in sessions[:12]:
                cols = st.columns([5, 1])
                label = s["title"] or "New Chat"
                if cols[0].button(label, key=f"switch_{s['id']}", use_container_width=True):
                    switch_to = s["id"]
                if cols[1].button("🗑️", key=f"del_{s['id']}", help="Delete chat"):
                    session_store.delete_session(s["id"])
                    st.rerun()
        else:
            st.caption("No past chats yet — start roasting.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.caption("CrucibleAI runs locally via Ollama. Zero data leaves your machine.")

        return sarcasm_level, uploaded_file, new_chat_clicked, switch_to
