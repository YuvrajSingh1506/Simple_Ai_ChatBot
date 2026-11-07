import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# ---------- Page setup ----------
st.set_page_config(page_title="Movie Information Extractor", page_icon="🎬", layout="centered")

st.markdown(
    """
    <style>
        #MainMenu, footer { visibility: hidden; }
        .block-container { max-width: 820px; padding-top: 2.5rem; }
        .hero-title {
            font-size: 2.4rem; font-weight: 800; text-align: center;
            background: linear-gradient(90deg, #6366f1, #ec4899);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }
        .hero-sub { text-align: center; opacity: 0.7; margin-bottom: 2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Model (same as before) ----------
@st.cache_resource
def get_model():
    return ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

model = get_model()

# ---------- Prompt (same as before) ----------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert Movie Information Extraction Assistant.

            Your role is to analyze movie-related paragraphs and extract
            useful, accurate, and relevant information in a well-organized
            plain-text format.

            Extract the following information:

            1. Movie Name
            2. Release Year
            3. Genre
            4. Director
            5. Cast and Characters
            6. Main Characters
            7. Movie Setting
            8. Plot
            9. Quick Summary
            10. Major Themes
            11. Awards and Recognitions
            12. Music Composer
            13. Cinematic and Visual Highlights
            14. Scientific or Historical References
            15. Key Events
            16. Emotional Tone
            17. Unique Features

            Guidelines:
            - Extract information strictly from the provided paragraph.
            - Do not use external knowledge or make assumptions.
            - If information is unavailable, write "Not mentioned".
            - Keep extracted information concise and informative.
            - Generate a quick summary in 2-3 sentences.
            - Avoid unnecessary repetition.
            - Use clear headings and bullet points.
            - Return plain text, not JSON.
            """
    ),
    (
        "human",
        """
        Extract useful information from the following movie description:

        {paragraph}
        """
    ),
])

# ---------- Header ----------
st.markdown('<div class="hero-title">🎬 Movie Information Extractor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Paste a movie paragraph and get organized details instantly.</div>',
    unsafe_allow_html=True,
)

# ---------- Input ----------
para = st.text_area(
    "Give your paragraph",
    height=220,
    placeholder="Paste a movie description here...",
)

extract = st.button("🔍 Extract Information", type="primary", use_container_width=True)

# ---------- Output ----------
if extract:
    if not para.strip():
        st.warning("Please enter a paragraph first.")
    else:
        final_prompt = prompt.invoke({"paragraph": para})
        with st.spinner("Extracting information..."):
            response = model.invoke(final_prompt)

        st.subheader("Extracted Information")
        with st.container(border=True):
            st.markdown(response.content[0]["text"])