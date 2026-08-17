"""Gemini summarization call."""

import logging
import os
import sys

from google import genai
from google.genai import errors as genai_errors

from . import config

# The google-genai SDK emits a noisy advisory about "automatic function calling"
# on every generate_content call. We don't use function calling, so silence it.
logging.getLogger("google_genai").setLevel(logging.ERROR)


def summarize(text: str, system_prompt: str) -> str:
    """Send ``text`` to Gemini with ``system_prompt`` and return the Markdown result."""
    api_key = os.getenv(config.GEMINI_API_KEY)
    if not api_key:
        print("Error: no Gemini API key configured.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    print("Sending to Gemini for summarization...")
    try:
        response = client.models.generate_content(
            model=config.MODEL,
            contents=text,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.3,
            ),
        )
    except genai_errors.APIError as e:
        print(f"Gemini API error [{e.code}]: {e.message}")
        sys.exit(1)

    summary = response.text
    if not summary:
        print("Error: Gemini returned an empty response.")
        sys.exit(1)

    return summary
