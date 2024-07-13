from summarizer import summarize
import streamlit as st

st.title("Extractive Text Summarizer Using NLP")
st.write("Developed and Deployed by Farhan Ali Khan")
st.divider()
text = st.text_input("Enter the text")
if len(text) != 0:
    st.text_area("Text", text)
btn = st.button("Summarize")
st.divider()
if len(text) != 0 and btn == 1:
    st.text_area("Summary", summarize(text, " ", 75))