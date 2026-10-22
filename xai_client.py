"""Wrapper for xAI Grok API."""

import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DEFAULT_MODEL = os.getenv("XAI_MODEL", "grok-3-mini")


def generate(
    prompt: str,
    api_key: str | None = None,
    model: str | None = None,
    temperature: float = 0.7,
    on_wait=None
) -> tuple[str, float]:

    api_key = api_key or os.getenv("XAI_API_KEY")

    if not api_key:
        raise ValueError(
            "xAI API key missing. Add XAI_API_KEY in .env"
        )

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )

    start = time.time()

    response = client.chat.completions.create(
        model=model or DEFAULT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature
    )

    text = response.choices[0].message.content

    return text, time.time() - start