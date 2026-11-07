from dotenv import load_dotenv
load_dotenv()
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)
text = [
    "Hello ji what do ypu want",
    "me kiya hello ji",
    "kiys kiya kya kiya"
]
vector = embedding.embed_documents(text)

print(vector)