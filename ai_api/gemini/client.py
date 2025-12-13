from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from discord import DiscordPayload
import time
from pydantic import ValidationError

# Loading the API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def ask_gemini(query: str, persona: str, language: str) -> DiscordPayload | None:
    print("Started Gemini sequence")
    # Creation of the client
    client = genai.Client(api_key=GEMINI_API_KEY)
    # Preparation of the search tool
    grounding_tool = types.Tool(google_search=types.GoogleSearch())

    try:
        research_prompt = f"""
        Act as a **specialized subject matter expert** for the following topic: {persona}. 
        Search and retrieve a maximum of **5 most recent and relevant articles** for the query: '{query}'.

        For each article, provide only the following information:
        1.  A **concise headline**.
        2.  A **brief summary** (2-3 sentences max).
        3.  The **full, valid URL** of the source.
        4.  **Crucially, strictly avoid redundancy:** If multiple articles discuss the exact same news or offer, provide only the most comprehensive one. Ensure the final list contains unique news items.

        Present the result as a raw, numbered Markdown list. The output language must be: {language}.
        Make sure the information is up-to-date and the URLs are valid.
        Current date and time: {time.strftime('%Y-%m-%d %H:%M:%S')}
        """

        print("🤖 Sending the first query")

        # First query to Gemini, to scrap the internet
        research_response = client.models.generate_content(  # type: ignore
            model="gemini-2.5-flash",
            contents=research_prompt,
            config=types.GenerateContentConfig(tools=[grounding_tool]),
        )

        # Get only the sent text
        raw_info = research_response.text

        if not raw_info:
            raise Exception("No response from Gemini.")
    # Error during the first request
    except Exception as e:
        print(f"Gemini error on step 1 (search): {e}")
        return None

    try:
        format_prompt = f"""
        You are a **Discord Payload Generator**. 
        Your only task is to transform the provided raw information into a **valid JSON Discord payload**.

        Here is the raw information: \n---\n{raw_info}\n---\n

        **JSON Output Constraints:**
        * The output must be a single JSON object containing the `embeds` array and a small description in `content`.
        * The array must contain one embed per news item.
        * The `color` field must be a **random positive integer in hex form** (e.g., `0x123456`).
        * The `url` field must be the source URL from the raw info.
        * Use **Markdown** (`**bold**`, `*italic*`) within the `title` and `description` fields.
        * The language of the output must match the source information.

        **RESPOND WITH THE JSON CODE ONLY. DO NOT INCLUDE ANY ADDITIONAL TEXT, EXPLANATIONS, OR MARKDOWN OUTSIDE OF THE JSON BLOCK.**
        """

        print("🤖 Sending the second query")

        # Second query to Gemini, to format the first answer with the given model
        formatting_response = client.models.generate_content(  # type: ignore
            model="gemini-2.5-flash",
            contents=format_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=DiscordPayload.model_json_schema(),
            ),
        )

        if formatting_response.text is None:
            raise Exception("No response from Gemini.")

        try:
            print("❔ Validation of the result")
            # Validate the received answer
            data: DiscordPayload = DiscordPayload.model_validate_json(
                formatting_response.text
            )
            return data
        # Error if the answer is not in the correct format
        except ValidationError as e:
            print(f"Error while validation: {e}")
            return None
    # Error during the process of the second request
    except Exception as e:
        print(f"Gemini error on step 2 (format): {e}")
        return None
