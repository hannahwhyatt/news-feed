from openai import OpenAI
from pydantic import BaseModel
from enum import Enum
from typing import List
import os
import dotenv
import json

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class UIType(str, Enum):
    div = "div"

class Attribute(BaseModel):
    name: str
    value: str

class UI(BaseModel):
    type: UIType
    label: str
    children: List["UI"] 
    attributes: List[Attribute]

UI.model_rebuild() # This is required to enable recursive types

class Response(BaseModel):
    ui: UI

def summarise_news(news):
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a news summariser."},
            {
                "role": "user",
                "content": "Summarise the following news headlines into 5 bullet points. The bullet points should be sentences that comprehensively explain the news. Return ONLY the bullet points as a list, no headers." +
                           '\n'.join([article['title'] + ": " + article['summary'] for article in news])
            }
        ],
        response_format=Response
    )
    return response.choices[0].message.parsed



if __name__ == "__main__":
    with open("data/news.json", "r") as f:
        news = json.load(f)
    summarised_news = summarise_news(news)
    with open("data/summarised_news.json", "w") as f:
        json.dump(summarised_news.model_dump(), f, indent=2)
