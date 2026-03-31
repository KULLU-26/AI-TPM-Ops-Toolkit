import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
# Replace 'YOUR_API_KEY' with the key you got from Google AI Studio
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- APP UI ---
st.set_page_config(page_title="TPM Ops Toolkit", layout="wide")
st.title("🚀 AI-Powered TPM Ops Toolkit 2026")
st.markdown("Automating execution for Hardware/Software IoT Ecosystems.")

# Create 3 Tabs for your 3 Tools
tab1, tab2, tab3 = st.tabs(["🪲 Bug Triage Classifier", "🧪 Test Case Gen", "⚠️ Sprint Risk Summariser"])

# --- TOOL 1: BUG TRIAGE (KASA Probe Inspired) ---
with tab1:
    st.header("Bug Triage & Severity Classifier")
    bug_input = st.text_area("Paste Bug Description (from Jira/Logs):", height=150)
    
    if st.button("Triage Bug"):
        with st.spinner("Analyzing cross-stack impact..."):
            prompt = f"""
            Act as an expert IoT Technical Program Manager. Read the following bug report:
            '{bug_input}'
            1. Classify the severity (P0 - Blocker, P1 - Critical, P2 - Major, P3 - Minor).
            2. Identify if this is a Firmware, Cloud, or Mobile App issue.
            3. Provide a 1-sentence recommended next action for the engineering team.
            Output in clean bullet points.
            """
            response = model.generate_content(prompt)
            st.success("Triage Complete")
            st.write(response.text)

# --- TOOL 2: TEST CASE GENERATOR (M63 W2 Inspired) ---
with tab2:
    st.header("E2E Test Case Generator")
    feature_input = st.text_area("Describe the Feature or PR (e.g., Vision AI Dirty Lens):", height=150)
    
    if st.button("Generate Test Plan"):
        with st.spinner("Generating edge cases..."):
            prompt = f"""
            Act as a Senior Validation Engineer for connected devices. 
            Based on this feature: '{feature_input}'
            Generate 5 critical End-to-End test cases. Include at least 2 hardware-software edge cases (e.g., latency, network drop, memory constraint).
            """
            response = model.generate_content(prompt)
            st.success("Test Plan Generated")
            st.write(response.text)

# --- TOOL 3: SPRINT RISK SUMMARISER ---
with tab3:
    st.header("Sprint Risk & Blocker Summariser")
    sprint_input = st.text_area("Paste rough sprint notes, Slack updates, or Jira dumps:", height=150)
    
    if st.button("Analyze Sprint Risks"):
        with st.spinner("Identifying dependencies..."):
            prompt = f"""
            Act as a Lead TPM. Analyze these sprint updates: '{sprint_input}'
            1. Identify any hidden blockers or cross-team dependencies.
            2. Highlight any risks to the release schedule.
            3. Provide a 'Red/Yellow/Green' overall sprint health score.
            """
            response = model.generate_content(prompt)
            st.success("Risk Analysis Complete")
            st.write(response.text)
