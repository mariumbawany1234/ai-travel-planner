"""Thin wrapper around the Google Gemini API (google-genai SDK)."""
import os
import re
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

load_dotenv()

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
# Optional: comma-separated backup models tried if the main one stays unavailable
FALLBACK_MODELS = [m.strip() for m in os.getenv("GEMINI_FALLBACK_MODELS", "").split(",") if m.strip()]

OVERLOAD_CODES = {500, 503, 504}   # temporary server problems -> short backoff
QUOTA_CODE = 429                   # rate limit -> wait the time Google tells us
MAX_RETRIES = 4
MAX_QUOTA_WAIT = 90                # seconds


def _retry_delay(err) -> float:
    """Read 'retry in 45.4s' / retryDelay '45s' from a 429 error."""
    text = str(err)
    m = re.search(r"retry in ([\d.]+)s", text) or re.search(r"retryDelay['\"]?:\s*['\"]([\d.]+)s", text)
    return min(float(m.group(1)) + 1, MAX_QUOTA_WAIT) if m else 30.0


def _call(client, model, prompt, temperature, on_wait=None):
    for attempt in range(MAX_RETRIES):
        try:
            return client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=temperature),
            )
        except errors.APIError as e:
            last = attempt == MAX_RETRIES - 1
            if e.code == QUOTA_CODE and not last:
                wait = _retry_delay(e)
                if on_wait:
                    on_wait(f"Rate limit reached (free tier). Waiting {wait:.0f}s before retrying...")
                time.sleep(wait)
            elif e.code in OVERLOAD_CODES and not last:
                time.sleep(2 ** attempt)
            else:
                raise


def generate(prompt: str, api_key: str | None = None, model: str | None = None,
             temperature: float = 0.7, on_wait=None) -> tuple[str, float]:
    """Send a prompt to Gemini. Returns (text, seconds_taken)."""
    api_key = api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Gemini API key missing. Set GEMINI_API_KEY in .env or enter it in the app.")

    client = genai.Client(api_key=api_key)
    start = time.time()
    last_error = None
    for m in [model or DEFAULT_MODEL] + FALLBACK_MODELS:
        try:
            response = _call(client, m, prompt, temperature, on_wait)
            return (response.text or "No response returned."), time.time() - start
        except errors.APIError as e:
            last_error = e
            if e.code not in OVERLOAD_CODES and e.code != QUOTA_CODE:
                raise
    raise last_error
