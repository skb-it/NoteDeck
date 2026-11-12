import requests
import json

from django.conf import settings

PROMPT_TEMPLATE = """Jesteś asystentem, który tworzy fiszki do nauki.

"options": {"temperature": 0.2}

Na podstawie poniższego fragmentu notatki utwórz od 2 do 5 fiszek.
Zasady:
- każda fiszka sprawdza jedną konkretną informację z tekstu,
- pytanie jest krótkie i jednoznaczne,
- odpowiedź ma najwyżej 2 zdania,
- nie dodawaj informacji, których nie ma w tekście,
- pisz po polsku.

Odpowiedz wyłącznie w formacie JSON, dokładnie w takiej postaci:
{{"cards": [{{"question": "...", "answer": "..."}}]}}

Fragment notatki:
\"\"\"
{text}
\"\"\"
"""

def generate_cards(text: str) -> list[dict]:
    """Sends chunk of note to the model and return list
    [{"question": "...", "answer": "..."}, ...]"""

    prompt = PROMPT_TEMPLATE.format(text=text)

    response = requests.post(
        f"{settings.OLLAMA_URL}/api/generate",
        json={"model": settings.OLLAMA_MODEL, "prompt": prompt, "stream": False, "format": "json"},
        timeout=120,
    )

    response.raise_for_status()
    response_json = response.json()

    try:
        data = json.loads(response_json["response"])
    except json.JSONDecodeError:
        return []

    if not isinstance(data, dict):
        return []

    cards = data.get("cards", [])

    if not isinstance(cards, list):
        return []

    result = []

    for card in cards:
        if not isinstance(card, dict):
            continue
        question = str(card.get("question", "")).strip()
        answer = str(card.get("answer", "")).strip()
        if question and answer:
            result.append({"question": question, "answer": answer})

    return result