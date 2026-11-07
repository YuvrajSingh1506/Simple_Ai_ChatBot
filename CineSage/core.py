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
    )]
)
para = input("Give your paragraph")
final_prompt = prompt.invoke(
    {
        "paragraph" : para
    }
)

response = model.invoke(final_prompt)

print(response.content[0]['text'])