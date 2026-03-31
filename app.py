import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION & SECRETS ---
try:
    # Pulls the API key securely from Streamlit Cloud Secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("⚠️ API Key missing. Please add GEMINI_API_KEY to your Streamlit secrets.")
    st.stop()

# Using the updated, active Flash model
model = genai.GenerativeModel('gemini-2.5-flash')

# Define the corrected safety settings dictionary to prevent crashes on engineering logs
custom_safety = {
    "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE"
}

# --- APP UI ---
st.set_page_config(page_title="TPM Ops Toolkit", layout="wide")
st.title("🚀 AI-Powered TPM Ops Toolkit 2026")
st.markdown("Automating execution and edge-case validation for Hardware/Software IoT Ecosystems.")

# Create 3 Tabs
tab1, tab2, tab3 = st.tabs(["🪲 Bug Triage Classifier", "🧪 Test Case Gen", "⚠️ Sprint Risk Summariser"])

# --- TOOL 1: BUG TRIAGE (KASA Probe Inspired) ---
with tab1:
    st.header("Bug Triage & Severity Classifier")
    st.markdown("Context: Evaluates bugs using the KASA Probe connected-device risk framework.")
    bug_input = st.text_area("Paste Bug Description (from Jira/Logs):", height=150, key="bug_input")
    
    if st.button("Triage Bug"):
        if not bug_input.strip():
            st.error("⚠️ Please paste a bug description first.")
        else:
            with st.spinner("Analyzing cross-stack impact..."):
                prompt = f"""
                Act as an expert IoT Technical Program Manager. Read the following bug report:
                '{bug_input}'
                
                Use the KASA Probe risk framework:
                1. Classify the severity (P0 - Blocker, P1 - Critical, P2 - Major, P3 - Minor). Note: If the bug mentions protocol-level synchronization drops or missed critical hardware notifications, automatically flag it as P1 or P0.
                2. Identify the core domain: Firmware, Cloud, or Mobile App.
                3. Provide a 1-sentence technical hypothesis or recommended next action for the engineering team.
                
                Output in clean, concise bullet points.
                """
                response = model.generate_content(prompt, safety_settings=custom_safety)
                st.success("Triage Complete")
                st.write(response.text)

# --- TOOL 2: TEST CASE GENERATOR (M63 W2 Inspired) ---
with tab2:
    st.header("E2E Test Case Generator")
    st.markdown("Context: Generates distributed-system edge cases for M63-style connected platforms.")
    feature_input = st.text_area("Describe the Feature or PR (e.g., Vision AI Dirty Lens, OTA Update):", height=150, key="feature_input")
    
    if st.button("Generate Test Plan"):
        if not feature_input.strip():
            st.error("⚠️ Please describe a feature first.")
        else:
            with st.spinner("Generating hardware/software edge cases..."):
                prompt = f"""
                Act as a Senior Validation Engineer for consumer connected devices (like the M63 Vision AI platform). 
                Based on this feature: '{feature_input}'
                
                Generate 5 critical End-to-End test cases. You MUST focus heavily on hardware-software edge cases. 
                Include scenarios testing:
                - Mid-cycle network interruptions (ghost states)
                - High latency and race conditions (cloud vs. physical buttons)
                - Memory constraints or hardware sensor failures
                
                Format as a professional validation test plan.
                """
                response = model.generate_content(prompt, safety_settings=custom_safety)
                st.success("Test Plan Generated")
                st.write(response.text)

# --- TOOL 3: SPRINT RISK SUMMARISER ---
with tab3:
    st.header("Sprint Risk & Blocker Summariser")
    st.markdown("Context: Parses daily standup notes to flag cross-org dependency friction.")
    sprint_input = st.text_area("Paste rough sprint notes, Slack updates, or Jira dumps:", height=150, key="sprint_input")
    
    if st.button("Analyze Sprint Risks"):
        if not sprint_input.strip():
            st.error("⚠️ Please paste sprint notes first.")
        else:
            with st.spinner("Identifying dependencies..."):
                prompt = f"""
                Act as a Lead TPM overseeing a global hardware and software release. Analyze these raw sprint updates: 
                '{sprint_input}'
                
                1. Identify any hidden blockers or cross-team dependencies (e.g., mobile waiting on firmware).
                2. Highlight any direct risks to the critical path or release schedule.
                3. Provide an overall sprint health status (🟢 Stable, 🟡 At Risk, 🔴 Blocked).
                
                Keep the analysis actionable and brief.
                """
                response = model.generate_content(prompt, safety_settings=custom_safety)
                st.success("Risk Analysis Complete")
                st.write(response.text)
