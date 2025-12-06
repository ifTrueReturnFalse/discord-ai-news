from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from discord import DiscordEmbed
from typing import List
from pydantic import TypeAdapter

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def ask_gemini(query: str, persona: str, language: str) -> List[DiscordEmbed]:
    client = genai.Client(api_key=GEMINI_API_KEY)
    adapter = TypeAdapter(List[DiscordEmbed])
    grounding_tool = types.Tool(google_search=types.GoogleSearch())

    try:
        research_response = client.models.generate_content(  # type: ignore
            model="gemini-2.5-flash",
            contents=f"Act as a search engine. Search and respond in this language: {language}. {persona}. Answer to this request: {query}. Make sure the URL are valid.",
            config=types.GenerateContentConfig(tools=[grounding_tool]),
        )

        raw_info = research_response.text

        if not raw_info:
            return []
    except Exception as e:
        print(f"Gemini error on step 1 (search): {e}")
        return []

    try:
        formatting_response = client.models.generate_content(  # type: ignore
            model="gemini-2.5-flash",
            contents=f"Here are some raw informations: \n---\n{raw_info}\n---\n Transform this informations in a valid list of DiscordEmbed. Keep the language used in the informations. Make sure the URL are valid. Embed colors are in integer / hexadecimal format (example: 0x7d34eb), pick a random color for each embed. Use the article date for the timestamp, if not found do not use this propertie.",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=adapter.json_schema(),
            ),
        )

        data = adapter.validate_json(formatting_response.text)  # type: ignore
        return data
    except Exception as e:
        print(f"Gemini error on step 2 (format): {e}")
        return []
