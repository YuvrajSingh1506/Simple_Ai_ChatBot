import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel
from typing import Optional, List
from langchain_core.output_parsers import PydanticOutputParser
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

# ---------- Schema and parser (same as before) ----------
class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str


parser = PydanticOutputParser(pydantic_object=Movie)

# ---------- Prompt (same as before) ----------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
            Extract movie information from paragraph
            {format_instructions}
        """
    ),
    (
        "human",
        """
            {paragraph}
        """
    ),
])

# ---------- Header ----------
st.markdown('<div class="hero-title">🎬 Movie Information Extractor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Paste a movie paragraph and get its details as structured data.</div>',
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
        final_prompt = prompt.invoke(
            {
                "paragraph": para,
                "format_instructions": parser.get_format_instructions(),
            }
        )
        with st.spinner("Extracting information..."):
            response = model.invoke(final_prompt)

        st.subheader("Extracted Information")
        st.code(parser.parse(response.content[0]["text"]), language="json")