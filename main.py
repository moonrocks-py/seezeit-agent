from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
import requests as re
from pydantic import BaseModel
from typing import TypedDict, List

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.9
)

class AgentState(TypedDict):
    raw_offer: List[str]


def scrape_content(url):
    response = re.get(
        url=url
    )
    response.raise_for_status()
    txt = response.text
    print(txt)

scrape_content("https://www.das-seeglueck.de/")