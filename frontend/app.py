import streamlit as st
import requests

# App Title
st.set_page_config(page_title="Language Translator", page_icon="🌍")
st.title("🌍 Language Translator using LLM")

# User Input
text = st.text_area("Enter text to translate:", height=150)
language = st.text_input("Enter target language (e.g., French, Spanish):")

# Translate Button
if st.button("Translate"):
    if text and language:
        with st.spinner("Translating..."):
            try:
                response = requests.post(
                    "http://localhost:8000/chain/invoke",
                    json={"text": text, "language": language}
                )
                if response.status_code == 200:
                    result = response.json()
                    st.success("Translation successful!")
                    st.write(f"**Translated Text:** {result}")
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter both text and target language.")

# Footer
st.markdown("---")
st.markdown("💡 **Built with LangChain, FastAPI & Streamlit**")
