from dotenv import load_dotenv

load_dotenv()

# from langchain.chat_models import init_chat_model

# model = init_chat_model("google_genai:gemini-3.8-flash")# print(model)

from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model="gemini-3.8-flash")

response = model.invoke("is indian cricket team is best in world")
# print(response.content)
for block in response.content:
    if block["type"] == "text":
        print(block["text"])