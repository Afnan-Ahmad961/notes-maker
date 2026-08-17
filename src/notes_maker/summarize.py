"""Gemini summarization call."""

import os
import sys

from google import genai

from . import config


def summarize(text: str, system_prompt: str) -> str:
    """Send ``text`` to Gemini with ``system_prompt`` and return the Markdown result."""
    api_key = os.getenv(config.GEMINI_API_KEY)
    if not api_key:
        print("Error: no Gemini API key configured.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    print("Sending to Gemini for summarization...")
    response = client.models.generate_content(
        model=config.MODEL,
        contents=text,
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.3,
        ),
    )

    summary = response.text
    if not summary:
        print("Error: Gemini returned an empty response.")
        sys.exit(1)

    return summary
