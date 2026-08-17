import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    api_key = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)

st.set_page_config(
    page_title="AI Technical Support Assistant",
    page_icon="🛠️"
)

st.title("AI Technical Support Assistant")

st.caption(
    "Built with Python, Streamlit and Google's Gemini API."
)

st.write(
    "Enter a customer technical issue below. "
    "The assistant will analyse the problem and suggest troubleshooting steps."
)

if "issue" not in st.session_state:
    st.session_state["issue"] = ""

issue = st.text_area(
    "Customer issue",
    placeholder="Example: Users are receiving a 401 error when trying to access our API...",
    key="issue"
)

col1, col2 = st.columns([1, 5])

with col1:
    analyse = st.button("Analyse Issue")

with col2:
    clear = st.button("Clear")

if clear:
    st.session_state["issue"] = ""
    st.rerun()

if analyse:

    if not issue.strip():
        st.warning("Please enter a technical issue.")

    else:
        prompt = f"""
You are a technical support assistant.

Analyse the following customer technical issue.

Provide your response using exactly these sections:

## Summary
Give a concise summary of the problem.

## Category
Choose the most appropriate category:
API, Authentication, Database, Networking, Software, Security, or Other.

## Priority
Choose Low, Medium, or High and briefly explain why.

## Possible Causes
List the most likely technical causes.

## Troubleshooting Steps
Provide clear numbered troubleshooting steps.

## Customer-Friendly Response
Write a professional response that could be sent to the customer.

Customer issue:
{issue}
"""

        with st.spinner("Analysing issue..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                st.subheader("Analysis")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")