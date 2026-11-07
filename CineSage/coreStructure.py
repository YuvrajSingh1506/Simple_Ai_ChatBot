from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel
from typing import Optional,List
from langchain_core.output_parsers import PydanticOutputParser

from langchain_core.prompts import ChatPromptTemplate,PromptTemplate

from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model ="gemini-3.5-flash-lite")
class Movie(BaseModel):
    title : str
    release_year : Optional[int]
    genre : List[str]
    director : Optional[str]
    cast : List[str]
    rating : Optional[float]
    summary : str


parser = PydanticOutputParser(pydantic_object=Movie)

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
   )
   ]
)
para = input("Give your paragraph : ")
final_prompt = prompt.invoke(
    {
        "paragraph" : para,
        "format_instructions" : parser.get_format_instructions()
    }
)

response = model.invoke(final_prompt)

print(response.content[0]['text'])