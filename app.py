import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from textblob import TextBlob

# -------------------- LOAD ENV --------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="BrandCraft AI",
    page_icon="🎨",
    layout="wide"
)

# -------------------- CUSTOM UI STYLE --------------------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #1f4037, #99f2c8);
    }
    .stButton>button {
        background-color: #000000;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.title("🎨 BrandCraft")
st.subheader("Generative AI–Powered Branding Automation System")

# -------------------- CHECK API KEY --------------------
if not api_key:
    st.error("⚠️ GROQ_API_KEY not found. Please add it to your .env file.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# -------------------- USER INPUT --------------------
col1, col2 = st.columns(2)

with col1:
    brand_topic = st.text_input("Enter Industry / Theme")
    tone = st.selectbox("Select Brand Tone", 
                        ["Professional", "Playful", "Luxury", "Minimal", "Bold"])

with col2:
    description = st.text_area("Describe Your Brand Vision")

# -------------------- GENERATE BUTTON --------------------
if st.button("🚀 Generate Branding Assets"):

    if not brand_topic or not description:
        st.warning("Please fill all fields.")
    else:
        prompt = f"""
        Generate:
        1. A unique brand name for {brand_topic}
        2. A logo concept description
        3. A tagline
        4. A short Instagram promotional caption
        Tone: {tone}
        Description: {description}
        """

        with st.spinner("Generating branding kit..."):
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

        output = response.choices[0].message.content

        st.success("✨ Branding Assets Generated Successfully!")

        st.markdown("## 🏷️ AI Generated Branding Kit")
        st.write(output)

        # -------------------- SENTIMENT ANALYSIS --------------------
        blob = TextBlob(output)
        sentiment_score = blob.sentiment.polarity

        st.markdown("### 📊 Sentiment Analysis")
        st.write(f"Sentiment Score: {round(sentiment_score, 2)}")

        if sentiment_score > 0:
            st.success("Positive Branding Tone 😊")
        elif sentiment_score < 0:
            st.error("Negative Tone ⚠️")
        else:
            st.info("Neutral Tone 😐")