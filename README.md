# AI Article Generator

A desktop application built with Python + CustomTkinter for generating articles using AI.

## Features
- Generate topic proposals
- Generate full articles
- Save articles to Word files (`.docx`)
- Browse article history (`historia.docx`)

## Requirements
- Python 3.12+
- Installed project dependencies

## Configuration
1. Copy `.env.example` to `.env` (if it does not exist yet).
2. Add your API key:

```env
GEMINI_API_KEY=your_api_key
```

## Run
```bash
python main.py
```

## Build EXE
```bash
python -m PyInstaller --noconfirm GeneratorArtykulow.spec
```

The generated executable is available in the `dist/` directory.
