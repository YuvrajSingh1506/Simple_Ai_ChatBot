from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import GoogleGenerativeAIEmbeddings


embeddings = GoogleGenerativeAIEmbeddings(
     model = "gemini-embedding-2",
     output_dimensionality = 64
)
text = ["hello my name is yuvraj",
        "what do you want",
          "from where you are"]
# vector = embeddings.embed_query("You are going to learn Gen AI ")
vector = embeddings.embed_documents(text)
print(vector)