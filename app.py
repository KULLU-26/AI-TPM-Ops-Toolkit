import streamlit as st
import google.generativeai as genai

# --- 1. SECRETS CONFIGURATION ---
st.set_page_config(page_title="TPM Ops Toolkit", layout="wide")
st.title("🚀 AI-Powered TPM Ops Toolkit")

# Safely check for API key
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🛑 STOP: API Key is missing. Please add GEMINI_API_KEY to your Streamlit Cloud Secrets.")
    st.stop()

# Configure the API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# USE THE ACTIVE MODEL (This is the one that worked perfectly for you earlier!)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. APP UI & TABS ---
tab1, tab2, tab3 = st.tabs(["🪲 Bug Triage Classifier", "🧪 Test Case Gen", "⚠️ Sprint Risk Summariser"])

# --- TOOL 1: BUG TRIAGE ---
with tab1:
    bug_input = st.text_area("Paste Bug Description (from Jira/Logs):", height=150, key="bug1")
    
    if st.button("Triage Bug"):
        if not bug_input.strip():
            st.warning("⚠️ Please paste a bug description first.")
        else:
            with st.spinner("Analyzing..."):
                prompt = f"Act as an expert IoT TPM. Read this bug report and classify its severity (P0-P3), domain (Firmware/Cloud/Mobile), and suggest a next step using the KASA Probe framework. Bug: {bug_input}"
                try:
                    response = model.generate_content(prompt)
                    st.success("Triage Complete")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"⚠️ Could not process request. If the bug contains terms like 'fatal' or 'kill', it may have tripped the AI safety filter. Error Details: {str(e)}")

# --- TOOL 2: TEST CASE GENERATOR ---
with tab2:
    feature_input = st.text_area("Describe the Feature or PR:", height=150, key="feat1")
    
    if st.button("Generate Test Plan"):
        if not feature_input.strip():
            st.warning("⚠️ Please describe a feature first.")
        else:
            with st.spinner("Generating..."):
                prompt = f"Act as a Senior Validation Engineer. Generate 5 critical End-to-End test cases for this feature, focusing heavily on hardware-software edge cases like network drops and latency. Feature: {feature_input}"
                try:
                    response = model.generate_content(prompt)
                    st.success("Test Plan Generated")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"⚠️ Could not process request. Error Details: {str(e)}")

# --- TOOL 3: SPRINT RISK SUMMARISER ---
with tab3:
    sprint_input = st.text_area("Paste rough sprint notes or Jira dumps:", height=150, key="sprint1")
    
    if st.button("Analyze Sprint Risks"):
        if not sprint_input.strip():
            st.warning("⚠️ Please paste sprint notes first.")
        else:
            with st.spinner("Analyzing..."):
                prompt = f"Act as a Lead TPM. Analyze these sprint updates, identify cross-team blockers, highlight risks to the critical path, and give a health status. Notes: {sprint_input}"
                try:
                    response = model.generate_content(prompt)
                    st.success("Risk Analysis Complete")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"⚠️ Could not process request. Error Details: {str(e)}")
