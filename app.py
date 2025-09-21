import streamlit as st
import re
from transformers import pipeline

# -----------------------
# Load AI models
# -----------------------
@st.cache_resource
def load_models():
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    simplifier = pipeline("text2text-generation", model="t5-small")
    return summarizer, simplifier

summarizer, simplifier = load_models()

# -----------------------
# Streamlit App
# -----------------------
st.set_page_config(page_title="Legal AI Assistant", layout="wide")

st.title("⚖️ Generative AI for Demystifying Legal Documents")
st.write(
    "This prototype makes legal documents easier to understand with **Simplification**, "
    "**Summarization**, and **Clause Highlighting**."
)

# Text input
user_text = st.text_area("📄 Paste Legal Document Text Here:", height=200,
                         placeholder="Enter a legal contract, agreement, or policy text...")

# Buttons for features
col1, col2, col3 = st.columns(3)

# -----------------------
# Simplify
# -----------------------
if col1.button("✨ Simplify"):
    if user_text.strip():
        with st.spinner("Simplifying..."):
            output = simplifier(user_text, max_length=120, do_sample=False)[0]['generated_text']
        st.subheader("✅ Simplified Text")
        st.write(output)
    else:
        st.warning("Please enter some text.")

# -----------------------
# Summarize
# -----------------------
if col2.button("📝 Summarize"):
    if user_text.strip():
        with st.spinner("Summarizing..."):
            output = summarizer(user_text, max_length=120, min_length=40, do_sample=False)[0]['summary_text']
        st.subheader("✅ Summary")
        st.write(output)
    else:
        st.warning("Please enter some text.")

# -----------------------
# Highlight Clauses
# -----------------------
if col3.button("🔍 Highlight Clauses"):
    if user_text.strip():
        keywords = ["penalty", "termination", "confidentiality", "obligation", "fees", "payment", "liability"]
        found = [kw for kw in keywords if re.search(rf"\b{kw}\b", user_text, flags=re.IGNORECASE)]
        st.subheader("✅ Highlighted Clauses")
        if found:
            st.write(f"⚠️ Found clauses related to: **{', '.join(set(found))}**")
        else:
            st.write("No critical clauses detected.")
    else:
        st.warning("Please enter some text.")
