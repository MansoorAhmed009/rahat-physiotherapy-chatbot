import os
import re
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types
from knowledge_base import build_system_prompt

load_dotenv()

logger = logging.getLogger(__name__)

client = None

def get_client():
    global client
    if client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your-gemini-api-key-here":
            raise ValueError(
                "GEMINI_API_KEY is not set. "
                "Create a .env file in the backend folder with: GEMINI_API_KEY=your-key-here\n"
                "Get a free key at: https://aistudio.google.com/app/apikey"
            )
        client = genai.Client(api_key=api_key)
    return client

INTENT_KEYWORDS = {
    "appointment": ["book", "appointment", "schedule", "visit", "come in", "see a physio", "see a therapist"],
    "lead": ["interested in", "want", "looking for", "need", "how much", "pricing", "cost", "price"],
}


def detect_intent(message: str) -> str | None:
    msg_lower = message.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(kw in msg_lower for kw in keywords):
            return intent
    return None


MAX_HISTORY_MESSAGES = 20


def trim_history(history: list[dict]) -> list[dict]:
    if len(history) > MAX_HISTORY_MESSAGES:
        return history[-MAX_HISTORY_MESSAGES:]
    return history


def strip_markdown(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    return text


def get_chat_response(message: str, conversation_history: list[dict]) -> str:
    try:
        ai_client = get_client()
        system_prompt = build_system_prompt()

        trimmed = trim_history(conversation_history)
        contents = []
        for entry in trimmed:
            role = "user" if entry["role"] == "user" else "model"
            contents.append(
                types.Content(role=role, parts=[types.Part(text=entry["content"])])
            )
        contents.append(
            types.Content(role="user", parts=[types.Part(text=message)])
        )

        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config={
                "system_instruction": system_prompt,
                "max_output_tokens": 800,
            },
        )
        return strip_markdown(response.text.strip())

    except Exception as e:
        logger.exception("Gemini API call failed")
        return (
            "I'm sorry, I'm having trouble connecting right now. "
            "Please try again in a moment or call us directly at (555) 123-4567."
        )
