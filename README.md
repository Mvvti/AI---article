# Generator Artykułów AI

Desktopowa aplikacja w Python + CustomTkinter do generowania artykułów z użyciem AI.

## Funkcje
- Generowanie propozycji tematów
- Generowanie pełnego artykułu
- Zapis artykułu do pliku Word (`.docx`)
- Historia wygenerowanych artykułów (`historia.docx`)

## Wymagania
- Python 3.12+
- Zainstalowane zależności z projektu

## Konfiguracja
1. Skopiuj `.env.example` do `.env` (jeśli jeszcze nie istnieje).
2. Uzupełnij klucz API:

```env
GEMINI_API_KEY=twoj_klucz_api
```

## Uruchamianie
```bash
python main.py
```

## Build EXE
```bash
python -m PyInstaller --noconfirm GeneratorArtykulow.spec
```

Gotowy plik znajduje się w katalogu `dist/`.
