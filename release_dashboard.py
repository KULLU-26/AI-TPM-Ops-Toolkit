import streamlit as st
import requests
import plotly.graph_objects as go

# --- UI & CONFIG ---
st.set_page_config(page_title="Release Intelligence Dashboard", layout="wide")
st.title("📊 Release Intelligence Dashboard")
st.markdown("Automated Release Health Scoring (Mirrors Google TPM Launch Readiness Methodology)")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("Target Repository")
    repo_input = st.text_input("GitHub Repo (Format: owner/repo)", value="streamlit/streamlit")
    st.markdown("---")
    st.markdown("**Release Criteria (Weights)**")
    
    # FIX 1: Capturing the slider values dynamically
    bug_weight = st.slider("Bug Penalty Weight", 1, 20, 15)
    pr_weight = st.slider("Stale PR Penalty", 1, 10, 2)
    
# --- GITHUB API DATA FETCHING ---
@st.cache_data(ttl=300) 
def fetch_github_data(repo):
    api_url = f"https://api.github.com/repos/{repo}"
    pulls_url = f"https://api.github.com/repos/{repo}/pulls?state=open"
    issues_url = f"https://api.github.com/repos/{repo}/issues?state=open&labels=bug"
    
    # FIX 2: Securely attaching the GitHub Token
    headers = {}
    if "GITHUB_TOKEN" in st.secrets:
        headers["Authorization"] = f"token {st.secrets['GITHUB_TOKEN']}"
    
    try:
        repo_data = requests.get(api_url, headers=headers).json()
        prs = requests.get(pulls_url, headers=headers).json()
        bugs = requests.get(issues_url, headers=headers).json()
        
        if 'message' in repo_data and 'Not Found' in repo_data['message']:
            return None, None, None
            
        return repo_data, prs, bugs
    except Exception as e:
        return None, None, None

with st.spinner("Ingesting live telemetry from GitHub..."):
    repo_info, open_prs, open_bugs = fetch_github_data(repo_input)

# --- TPM SCORING ALGORITHM ---
if repo_info is not None:
    stars = repo_info.get("stargazers_count", 0)
    pr_count = len(open_prs) if isinstance(open_prs, list) else 0
    bug_count = len(open_bugs) if isinstance(open_bugs, list) else 0
    
    # FIX 3: Using the dynamic slider variables in the math, not hardcoded numbers
    base_score = 100
    bug_penalty_total = bug_count * bug_weight
    pr_penalty_total = pr_count * pr_weight
    
    health_score = base_score - bug_penalty_total - pr_penalty_total
    health_score = max(0, min(100, health_score))
    
    # Determine Status
    if health_score >= 80:
        status, color = "GO FOR LAUNCH", "green"
    elif health_score >= 50:
        status, color = "PROCEED WITH CAUTION", "orange"
    else:
        status, color = "NO-GO (CRITICAL RISKS)", "red"

    # --- DASHBOARD RENDERING ---
    col1, col2 = st.columns([1, 2])
    
    with col1:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = health_score,
            title = {'text': "Release Health Score"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightcoral"},
                    {'range': [50, 80], 'color': "navajowhite"},
                    {'range': [80, 100], 'color': "lightgreen"}],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': 80}
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"<h3 style='text-align: center; color: {color};'>{status}</h3>", unsafe_allow_html=True)

    with col2:
        st.subheader("Live Repo Telemetry")
        st.markdown("Real-time signals ingested via GitHub REST API.")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Open Release-Blocking Bugs", f"{bug_count}", f"-{bug_penalty_total} pts" if bug_count > 0 else "Clear")
        m2.metric("Open PR Backlog", f"{pr_count}", f"-{pr_penalty_total} pts")
        m3.metric("Repo Stars (Scale)", f"{stars:,}")
        
        st.markdown("---")
        st.subheader("TPM Risk Analysis")
        if bug_count > 0:
            st.error(f"⚠️ **Blocker:** There are {bug_count} open bugs tagged in this repository. Launch is blocked until these are triaged or resolved.")
        if pr_count > 10:
            st.warning(f"🟡 **Velocity Risk:** High volume of open PRs ({pr_count}) indicates an integration bottleneck. Suggest code-freeze to clear backlog.")
        if health_score >= 80:
            st.success("✅ **System Stable:** Bug count is within SLO thresholds. Integration velocity is stable. Authorized for production deployment.")

else:
    st.error("Could not fetch data. Please check the repo format (e.g., 'facebook/react') or check your GitHub Token.")
