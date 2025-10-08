from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
import requests as re
from pydantic import BaseModel
from typing import TypedDict, List
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.9
)

class AgentState(TypedDict):
    raw_offer: List[str]


def scrape_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        response = re.get(
            url=url,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )
        articles = soup.find_all(
            "div",
            class_="article"
        )
        print(f"Found {len(articles)} articles")
        for i, article in enumerate(articles):
            print(f"Article {i+1}: {article.get_text()[:100]}...")
            
    except re.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Status Code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        if response.status_code == 500:
            print("Server error - the website might be experiencing issues or blocking requests")
        elif response.status_code == 403:
            print("Access forbidden - the website might be blocking automated requests")
        elif response.status_code == 404:
            print("Page not found - the URL might be incorrect")
    except re.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

scrape_content("https://seezeit.com/Community/AnzeigeSelectJobangebot.do")

