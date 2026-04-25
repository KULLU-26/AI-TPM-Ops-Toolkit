import streamlit as st
import time
from streamlit_lottie import st_lottie
import requests

# Page Config
st.set_page_config(page_title="A Little Sukoon for You", page_icon="☕")

# Helper function for animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load cute animations
lottie_chai = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_q7796nka.json") # Tea pouring
lottie_heart = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_028qdr9g.json") # Floating hearts

# Custom CSS for the "Vibe"
st.markdown("""
    <style>
    .main {
        background-color: #FFF9F0;
    }
    h1 {
        color: #6F4E37;
        font-family: 'Georgia', serif;
    }
    .stButton>button {
        background-color: #6F4E37;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
    }
    </style>
    """, unsafe_allow_html=True)

# Session State to track progress
if 'step' not in st.session_state:
    st.session_state.step = 0

# --- APP LOGIC ---

if st.session_state.step == 0:
    st.title("Hey you... ✨")
    st.write("I know things are super hectic in Gwalior right now with all the wedding functions, poojas, and relatives...")
    st.write("I can't bring you actual ginger chai from Pune yet, but I made this 2-minute 'Virtual Escape' just for you.")
    
    if st.button("I need a break! 🙋‍♀️"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.title("The Stress-o-Meter 📉")
    stress_level = st.select_slider(
        "On a scale of 'Happy' to 'Haldi-overload', how tired are you?",
        options=["Energetic", "Tired", "Need Nap", "Save Me", "Fully Exhausted"]
    )
    
    if st.button("Fix my mood!"):
        with st.spinner("Brewing something special..."):
            time.sleep(2)
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.title("Virtual Chai Break ☕")
    st_lottie(lottie_chai, height=300)
    
    st.subheader("Pick your mood-fixer:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Adrak Wali Chai"):
            st.info("Strong & refreshing—just like your energy at the wedding! 💃")
    with col2:
        if st.button("Elaichi Chai"):
            st.success("Sweet & calming—breathe in, the functions are almost over! 🌸")
    with col3:
        if st.button("Masala Chai"):
            st.warning("A bit of everything—hang in there, you're doing great! 💪")

    st.write("---")
    if st.button("Okay, I feel a bit better. What's next?"):
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    st.title("A Little Reminder... 💌")
    st_lottie(lottie_heart, height=200)
    
    st.markdown(f"""
    ### While you're busy being the best sister at the wedding:
    * Don't forget to actually eat between the ceremonies.
    * You're doing an amazing job handling everything.
    * I'm right here in Pune, waiting to hear all the gossip once you're free.
    
    **I'm genuinely so proud of how you're managing it all.** """)
    
    if st.button("Click for a final surprise 🎁"):
        st.balloons()
        st.toast("You're my favorite person to talk to!", icon='❤️')
        time.sleep(2)
        st.markdown("#### Can't wait to grab a *real* chai with you when you're back. ☕✨")
        st.write("- [Your Name]")