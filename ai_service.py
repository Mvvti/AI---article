import os
import re
import time
from pathlib import Path

from google import genai


_ENV_LOADED = False


def _load_local_env_file():
    global _ENV_LOADED
    if _ENV_LOADED:
        return

    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        _ENV_LOADED = True
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value

    _ENV_LOADED = True


def _get_api_key():
    _load_local_env_file()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Brak GEMINI_API_KEY")
    return api_key


def _get_tone_instruction(content_type):
    if content_type == "Facebook":
        return (
            "Styl: lekki, angażujący i naturalny, z prostym językiem, "
            "krótszymi zdaniami i bardziej rozmownym tonem."
        )
    if content_type == "LinkedIn":
        return (
            "Styl: profesjonalny i ekspercki, z konkretnymi wnioskami, "
            "biznesowym językiem i wiarygodnym tonem."
        )
    return "Styl: klasyczny artykuł blogowy, przejrzysty i merytoryczny."


def generate_topic_proposals(topic, content_type="Blog"):
    api_key = _get_api_key()

    client = genai.Client(api_key=api_key)
    tone_instruction = _get_tone_instruction(content_type)
    prompt = (
        f"Typ treści: {content_type}. "
        f"{tone_instruction} "
        f"Podaj dokładnie 3 różne propozycje tytułów artykułów na temat: {topic}. "
        "Zwróć wyłącznie 3 gotowe tytuły: bez wstępu, bez nagłówków, bez numeracji, bez komentarzy. "
        "Każdy tytuł w osobnej linii."
    )
    max_retries = 3
    response = None

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
            )
            break
        except Exception as e:
            error_text = str(e)
            print(f"Błąd generowania propozycji (próba {attempt}/{max_retries}): {e}")

            is_unavailable = "503" in error_text or "UNAVAILABLE" in error_text.upper()
            if is_unavailable and attempt < max_retries:
                time.sleep(2)
                continue

            if is_unavailable:
                raise RuntimeError("Usługa AI jest chwilowo przeciążona. Spróbuj ponownie za chwilę.")

            raise RuntimeError(f"Błąd generowania propozycji: {e}")

    response_text = (response.text or "").strip()
    if not response_text:
        raise ValueError("Pusta odpowiedź")

    lines = [line.strip() for line in response_text.splitlines() if line.strip()]
    proposals = []
    intro_line_pattern = re.compile(
        r"^\s*(?:oto|propozycje|proponowane|poniżej|tytuły|3\s+propozycje)\b.*:?\s*$",
        re.IGNORECASE,
    )

    for line in lines:
        cleaned_line = re.sub(r"^\s*(?:[-*•]\s*)?", "", line)
        cleaned_line = re.sub(r"^\s*\d+[\).:-]?\s*", "", cleaned_line).strip()
        if not cleaned_line:
            continue
        if intro_line_pattern.match(cleaned_line):
            continue
        if cleaned_line:
            proposals.append(cleaned_line)
        if len(proposals) == 3:
            break

    while len(proposals) < 3:
        fallback_no = len(proposals) + 1
        if fallback_no == 1:
            proposals.append(f"{topic}: najważniejsze informacje")
        elif fallback_no == 2:
            proposals.append(f"{topic}: praktyczny poradnik krok po kroku")
        else:
            proposals.append(f"{topic}: błędy, których warto unikać")

    return proposals


def generate_article_text(topic, content_type="Blog"):
    api_key = _get_api_key()

    client = genai.Client(api_key=api_key)
    tone_instruction = _get_tone_instruction(content_type)
    prompt = (
        f"Napisz po polsku treść na temat: {topic}.\n"
        f"Typ treści: {content_type}.\n"
        f"{tone_instruction}\n"
        "Treść ma mieć około 300-500 słów i dokładnie tę strukturę:\n"
        "Tytuł\n"
        "Wstęp\n"
        "Rozwinięcie\n"
        "Podsumowanie\n"
        "Zwróć sam gotowy tekst."
    )

    max_retries = 3
    response = None

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
            )
            break
        except Exception as e:
            error_text = str(e)
            print(f"Błąd generowania artykułu (próba {attempt}/{max_retries}): {e}")

            is_unavailable = "503" in error_text or "UNAVAILABLE" in error_text.upper()
            if is_unavailable and attempt < max_retries:
                time.sleep(2)
                continue

            raise RuntimeError(f"Błąd generowania artykułu: {e}")

    article_text = (response.text or "").strip()
    if not article_text:
        raise ValueError("Pusta odpowiedź")

    return article_text


def stream_article_text(topic, content_type="Blog"):
    api_key = _get_api_key()

    client = genai.Client(api_key=api_key)
    tone_instruction = _get_tone_instruction(content_type)
    prompt = (
        f"Napisz po polsku treść na temat: {topic}.\n"
        f"Typ treści: {content_type}.\n"
        f"{tone_instruction}\n"
        "Treść ma mieć około 300-500 słów i dokładnie tę strukturę:\n"
        "Tytuł\n"
        "Wstęp\n"
        "Rozwinięcie\n"
        "Podsumowanie\n"
        "Zwróć sam gotowy tekst."
    )

    max_retries = 3

    for attempt in range(1, max_retries + 1):
        got_any_text = False
        try:
            response_stream = client.models.generate_content_stream(
                model="gemini-2.5-flash-lite",
                contents=prompt,
            )
            for chunk in response_stream:
                chunk_text = chunk.text or ""
                if chunk_text:
                    got_any_text = True
                    yield chunk_text

            if not got_any_text:
                raise ValueError("Pusta odpowiedź")

            return
        except Exception as e:
            error_text = str(e)
            print(f"Błąd streamingu artykułu (próba {attempt}/{max_retries}): {e}")

            is_unavailable = "503" in error_text or "UNAVAILABLE" in error_text.upper()
            can_retry = is_unavailable and attempt < max_retries and not got_any_text
            if can_retry:
                time.sleep(2)
                continue

            raise RuntimeError(f"Błąd generowania artykułu: {e}")
