"""Wrapper around Groq API."""

import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

DEFAULT_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)


def generate(
    prompt: str,
    api_key: str | None = None,
    model: str | None = None,
    temperature: float = 0.7,
    on_wait=None
) -> tuple[str, float]:

    api_key = api_key or os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "Groq API key missing. Add GROQ_API_KEY in .env"
        )

    client = Groq(api_key=api_key)

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