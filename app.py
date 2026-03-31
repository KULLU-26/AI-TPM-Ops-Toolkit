import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION & SECRETS ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("⚠️ API Key missing. Please add GEMINI_API_KEY to your Streamlit secrets.")
    st.stop()

# Using the stable 1.5-flash model
model = genai.GenerativeModel('gemini-1.5-flash')

# --- APP UI ---
st.set_page_config(page_title="TPM Ops Toolkit", layout="wide")
st.title("🚀 AI-Powered TPM Ops Toolkit 2026")
st.markdown("Automating execution and edge-case validation for Hardware/Software IoT Ecosystems.")

tab1, tab2, tab3 = st.tabs(["🪲 Bug Triage Classifier", "🧪 Test Case Gen", "⚠️ Sprint Risk Summariser"])

# --- TOOL 1: BUG TRIAGE ---
with tab1:
    st.header("Bug Triage & Severity Classifier")
    bug_input = st.text_area("Paste Bug Description (from Jira/Logs):", height=150, key="bug_input")
    
    if st.button("Triage Bug"):
        if not bug_input.strip():
            st.warning("⚠️ Please paste a bug description first.")
        else:
            with st.spinner("Analyzing cross-stack impact..."):
                prompt = f"""
                Act as an expert IoT Technical Program Manager. Read the following bug report:
                '{bug_input}'
                Use the KASA Probe risk framework:
                1. Classify the severity (P0 - Blocker, P1 - Critical, P2 - Major, P3 - Minor).
                2. Identify the core domain: Firmware, Cloud, or Mobile App.
                3. Provide a 1-sentence technical hypothesis for the engineering team.
                Output in clean, concise bullet points.
                """
                # Reverted: Removed safety settings
                response = model.generate_content(prompt)
                st.success("Triage Complete")
                st.write(response.text)

# --- TOOL 2: TEST CASE GENERATOR ---
with tab2:
    st.header("E2E Test Case Generator")
    feature_input = st.text_area("Describe the Feature or PR:", height=150, key="feature_input")
    
    if st.button("Generate Test Plan"):
        if not feature_input.strip():
            st.warning("⚠️ Please describe a feature first.")
        else:
            with st.spinner("Generating hardware/software edge cases..."):
                prompt = f"""
                Act as a Senior Validation Engineer for consumer connected devices.
                Based on this feature: '{feature_input}'
                Generate 5 critical End-to-End test cases. Focus heavily on hardware-software edge cases (network drops, latency, sensor failures).
                """
                # Reverted: Removed safety settings
                response = model.generate_content(prompt)
                st.success("Test Plan Generated")
                st.write(response.text)

# --- TOOL 3: SPRINT RISK SUMMARISER ---
with tab3:
    st.header("Sprint Risk & Blocker Summariser")
    sprint_input = st.text_area("Paste rough sprint notes or Jira dumps:", height=150, key="sprint_input")
    
    if st.button("Analyze Sprint Risks"):
        if not sprint_input.strip():
            st.warning("⚠️ Please paste sprint notes first.")
        else:
            with st.spinner("Identifying dependencies..."):
                prompt = f"""
                Act as a Lead TPM overseeing a global hardware and software release. Analyze these raw sprint updates: 
                '{sprint_input}'
                1. Identify any hidden blockers or cross-team dependencies.
                2. Highlight any direct risks to the critical path.
                3. Provide an overall sprint health status.
                """
                # Reverted: Removed safety settings
                response = model.generate_content(prompt)
                st.success("Risk Analysis Complete")
                st.write(response.text)
