from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
model = ChatGoogleGenerativeAI(model ="gemini-3.5-flash-lite",
                                max_output_tokens=300,
    timeout=30,
    max_retries=1)

print("choose you AI mode")
print("Enter 1 for Angry mode")
print("Enter 2 for Funny mode")
print("Enter 3 for sad mode")

choice = int(input("tell your response :-"))

if choice == 1:
    mode = "You are a Angry AI Agent. You respond aggressivley and impatiently"
elif choice == 2:
    mode = "You are a Funny AI Agent. You respond with humor and jokes."
elif choice == 3:
    mode = "You are a Sad AI Agent. You respond with depressed and emotional."
message =[
    SystemMessage(content="You are a funny AI Agent ")
]

print("__________ welcome type 0 to exit the application__________")
while True:
    prompt = input("You: ") 
    message.append(HumanMessage(content=prompt))
    if prompt == "0":
        break
    response = model.invoke(message)
    message.append(AIMessage(content = response.content[0]["text"]))
    print("Bot: ",response.content[0]["text"])

print(message)