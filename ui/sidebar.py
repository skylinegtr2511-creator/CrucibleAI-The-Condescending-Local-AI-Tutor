import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.header("⚙️ Tutor Settings")
        
        # Sarcasm Meter
        sarcasm_level = st.slider(
            "Sarcasm Meter", 
            min_value=1, 
            max_value=10, 
            value=8, 
            help="1 = Mildly Annoyed, 10 = Ruthless Savage"
        )
        
        st.divider()
        
        # Document Upload Area
        st.header("📄 Upload Material")
        uploaded_file = st.file_uploader(
            "Upload a document for me to mock...", 
            type=["pdf", "docx", "txt", "csv"]
        )
        
        if uploaded_file:
            st.success("File loaded. Let's see how bad this is.")
            
        return sarcasm_level, uploaded_file