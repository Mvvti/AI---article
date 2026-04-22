# Higma-Service Design System
> Wersja 1.0 | Obowiązuje dla wszystkich aplikacji desktopowych Higma Automate
> Technologia: Python / Flet / Windows Desktop

---

## 1. KOLORY

### Paleta główna

| Nazwa         | Hex       | Zastosowanie                                      |
|---------------|-----------|---------------------------------------------------|
| Primary       | `#2A95CF` | TopBar, Primary Button, akcenty, linki aktywne    |
| Accent        | `#6EC1E4` | Secondary Button border, ikony pomocnicze         |
| Primary Hover | `#5AB3DC` | Hover state na Primary Button i elementach TopBar |
| Text          | `#7A7A7A` | Body text, etykiety, opisy                        |
| Secondary     | `#54595F` | Nagłówki sekcji, ważniejszy tekst                 |
| Background    | `#FFFFFF` | Główne tło aplikacji                              |
| Surface       | `#F8FAFC` | Tło sekcji logów, tło inputów read-only           |
| Border        | `#E2E8F0` | Obramowania inputów, separatory, karty            |
| White         | `#FFFFFF` | Tekst na TopBarze, tekst na Primary Button        |

### Kolory semantyczne (stany)

| Nazwa           | Hex       | Zastosowanie                            |
|-----------------|-----------|-----------------------------------------|
| Success         | `#22C55E` | Komunikaty sukcesu, status OK           |
| Success Light   | `#DCFCE7` | Tło komunikatu sukcesu                  |
| Warning         | `#F59E0B` | Ostrzeżenia, stany wymagające uwagi     |
| Warning Light   | `#FEF3C7` | Tło komunikatu ostrzeżenia              |
| Error           | `#EF4444` | Błędy, walidacja, stany krytyczne       |
| Error Light     | `#FEE2E2` | Tło komunikatu błędu                    |
| Disabled BG     | `#F3F4F6` | Tło elementów nieaktywnych              |
| Disabled Text   | `#9CA3AF` | Tekst elementów nieaktywnych            |
| Disabled Border | `#D1D5DB` | Obramowanie elementów nieaktywnych      |

---

## 2. TYPOGRAFIA

**Font główny:** Roboto (importowany lub systemowy fallback: Segoe UI → Arial → sans-serif)  
**Font mono:** Roboto Mono (logi, ścieżki plików, kod)

| Rola                  | Rozmiar | Waga | Kolor             | Zastosowanie                        |
|-----------------------|---------|------|-------------------|-------------------------------------|
| App Title (TopBar)    | 18px    | 600  | `#FFFFFF`         | Nazwa aplikacji w TopBarze          |
| TopBar items          | 14px    | 400  | `#FFFFFF`         | Przyciski nawigacji w TopBarze      |
| Section Heading       | 16px    | 600  | `#54595F`         | Nagłówki sekcji w aplikacji         |
| Page Title            | 28px    | 700  | `#54595F`         | Główny tytuł ekranu                 |
| Label                 | 14px    | 400  | `#54595F`         | Etykiety pól formularza             |
| Body                  | 14px    | 400  | `#7A7A7A`         | Teksty opisowe, paragrafy           |
| Input text            | 14px    | 400  | `#54595F`         | Tekst wpisany w polu                |
| Placeholder           | 14px    | 400  | `#9CA3AF`         | Placeholder w pustym polu           |
| Button label          | 14px    | 600  | zależny od typu   | Tekst przycisku                     |
| Status text           | 13px    | 400  | semantyczny       | Komunikaty statusu                  |
| Log text              | 12px    | 400  | `#374151`         | Tekst w obszarze logów (mono)       |
| Caption / Helper      | 12px    | 400  | `#9CA3AF`         | Teksty pomocnicze pod polami        |

---

## 3. SPACING (siatka 4px)

| Nazwa    | Wartość | Zastosowanie                                      |
|----------|---------|---------------------------------------------------|
| xs       | 4px     | Wewnętrzny margines małych elementów              |
| sm       | 8px     | Gap między label a polem, między ikonką a tekstem |
| md       | 12px    | Gap między elementami w wierszu formularza        |
| lg       | 16px    | Gap między wierszami formularza                   |
| xl       | 24px    | Gap między sekcjami, marginesy strony             |
| xxl      | 32px    | Duże separatory, odstępy między blokami           |
| page     | 24px    | Margines zewnętrzny aplikacji (wszystkie strony)  |

---

## 4. WYMIARY KOMPONENTÓW

| Komponent           | Wysokość | Border Radius | Uwagi                                  |
|---------------------|----------|---------------|----------------------------------------|
| TopBar              | 80px     | 0             | Rozciąga się na pełną szerokość okna   |
| Button (wszystkie)  | 40px     | 8px           | Szerokość: auto (dopasowana do tekstu) |
| Input / TextField   | 40px     | 6px           | Szerokość: zależna od layoutu          |
| Input read-only     | 40px     | 6px           | Jak input, tło Surface                 |
| Progress Bar        | 8px      | 4px           | Pełna szerokość kontenera              |
| Status Bar          | 32px     | 0             | Dolna belka aplikacji (opcjonalna)     |

> **Szerokość przycisków jest zawsze elastyczna (auto/fit-content).**
> Padding poziomy przycisku: zawsze 20px z każdej strony.
> Tekst przycisku determinuje szerokość — krótki tekst = wąski button, długi = szeroki.
> Nigdy nie ustawiaj stałej szerokości przycisku.

---

## 5. STANY KOMPONENTÓW

### 5.1 TopBar — elementy nawigacji (tekst/przyciski)

| Stan     | Wygląd                                                    |
|----------|-----------------------------------------------------------|
| Default  | Tekst biały `#FFFFFF`, bez podkreślenia, bez tła          |
| Hover    | Tekst biały `#FFFFFF` + **underline**, kursor pointer     |
| Active   | Tekst biały `#FFFFFF` + **underline bold**                |
| Disabled | Tekst `rgba(255,255,255,0.4)`, kursor default             |

### 5.2 Primary Button

| Stan     | Tło        | Tekst     | Border     | Kursor  | Inne                        |
|----------|------------|-----------|------------|---------|------------------------------|
| Default  | `#2A95CF`  | `#FFFFFF` | brak       | pointer | —                            |
| Hover    | `#5AB3DC`  | `#FFFFFF` | brak       | pointer | Przejście płynne 150ms       |
| Active   | `#1a7fb5`  | `#FFFFFF` | brak       | pointer | Lekkie wciśnięcie (scale 0.98)|
| Disabled | `#F3F4F6`  | `#9CA3AF` | `#D1D5DB`  | default | Opacity 0.6, nie reaguje     |
| Loading  | `#5AB3DC`  | `#FFFFFF` | brak       | default | Spinner + tekst "Ładowanie…" |

### 5.3 Secondary Button

| Stan     | Tło        | Tekst     | Border           | Kursor  | Inne                   |
|----------|------------|-----------|------------------|---------|------------------------|
| Default  | `#FFFFFF`  | `#2A95CF` | `1.5px #6EC1E4`  | pointer | —                      |
| Hover    | `#F0F9FF`  | `#2A95CF` | `1.5px #2A95CF`  | pointer | Przejście płynne 150ms |
| Active   | `#E0F2FE`  | `#1a7fb5` | `1.5px #1a7fb5`  | pointer | Scale 0.98             |
| Disabled | `#F3F4F6`  | `#9CA3AF` | `1.5px #D1D5DB`  | default | Opacity 0.6            |
| Loading  | `#F0F9FF`  | `#2A95CF` | `1.5px #6EC1E4`  | default | Spinner widoczny       |

### 5.4 Input / TextField

| Stan      | Tło        | Border             | Tekst     | Kursor | Inne                              |
|-----------|------------|--------------------|-----------|--------|-----------------------------------|
| Default   | `#FFFFFF`  | `1px #E2E8F0`      | `#54595F` | text   | —                                 |
| Focus     | `#FFFFFF`  | `1.5px #2A95CF`    | `#54595F` | text   | Subtelny cień: `0 0 0 3px rgba(42,149,207,0.15)` |
| Filled    | `#FFFFFF`  | `1px #E2E8F0`      | `#54595F` | text   | —                                 |
| Error     | `#FFFFFF`  | `1.5px #EF4444`    | `#54595F` | text   | Komunikat błędu pod polem (12px, czerwony) |
| Disabled  | `#F3F4F6`  | `1px #D1D5DB`      | `#9CA3AF` | default| Nie przyjmuje focusu              |
| Read-only | `#F8FAFC`  | `1px #E2E8F0`      | `#54595F` | default| Tło Surface, nie edytowalne       |

### 5.5 Progress Bar

| Stan        | Kolor wypełnienia | Kolor tła  | Inne                              |
|-------------|-------------------|------------|-----------------------------------|
| Idle (0%)   | brak              | `#E2E8F0`  | Pusty pasek                       |
| In progress | `#2A95CF`         | `#E2E8F0`  | Animacja wypełnienia              |
| Success     | `#22C55E`         | `#DCFCE7`  | Po zakończeniu                    |
| Error       | `#EF4444`         | `#FEE2E2`  | Przy błędzie                      |

### 5.6 Status Label (tekst statusu nad/pod progress barem)

| Stan        | Kolor tekstu | Przykład                    |
|-------------|--------------|-----------------------------|
| Idle        | `#9CA3AF`    | "Gotowy do uruchomienia"    |
| Running     | `#2A95CF`    | "Przetwarzanie… (45%)"      |
| Success     | `#22C55E`    | "Zakończono pomyślnie"      |
| Warning     | `#F59E0B`    | "Zakończono z ostrzeżeniami"|
| Error       | `#EF4444`    | "Błąd: nie znaleziono pliku"|

### 5.7 Log Area

| Właściwość    | Wartość                                      |
|---------------|----------------------------------------------|
| Tło           | `#F8FAFC`                                    |
| Border        | `1px solid #E2E8F0`                          |
| Border radius | `8px`                                        |
| Font          | Roboto Mono, 12px                            |
| Kolor tekstu  | `#374151`                                    |
| Padding       | `12px`                                       |
| Overflow      | Scroll pionowy, auto                         |
| Min-height    | `160px`                                      |
| Linia logu — info    | `#374151`                             |
| Linia logu — sukces  | `#22C55E`                             |
| Linia logu — błąd    | `#EF4444`                             |
| Linia logu — warning | `#F59E0B`                             |

---

## 6. TOPBAR — SPECYFIKACJA SZCZEGÓŁOWA

```
┌─────────────────────────────────────────────────────────────┐
│ [Nazwa Aplikacji]   [opcjonalne przyciski]  [Instrukcja] [Pomoc]  [hslogo] │
└─────────────────────────────────────────────────────────────┘
```

| Właściwość              | Wartość                                              |
|-------------------------|------------------------------------------------------|
| Wysokość                | 80px                                                 |
| Tło                     | `#2A95CF`                                            |
| Padding poziomy         | 20px                                                 |
| Kolor wszystkich tekstów| `#FFFFFF`                                            |
| Font nazwy aplikacji    | 18px, weight 600                                     |
| Font przycisków         | 14px, weight 400                                     |
| Hover każdego elementu  | underline, bez zmiany koloru                         |
| Separator między przyciskami | opcjonalny `│` w kolorze `rgba(255,255,255,0.3)` |

**Stałe elementy (zawsze obecne, zawsze w tej kolejności od prawej):**
1. `hslogo` — logo firmy, klik → otwiera `https://higma-service.pl` w przeglądarce
2. `Pomoc` — klik → otwiera klienta mailowego z adresem `higmautomate@higma-service.pl`
3. `Instrukcja` — klik → przejście do ekranu Instrukcji

**Elementy zmienne (między nazwą aplikacji a Instrukcją):**
- Definiowane per aplikacja
- Przekazywane jako lista dodatkowych przycisków/akcji
- Ten sam styl co pozostałe elementy TopBaru

**Logo `hslogo`:**
- Preferowany format: `.svg`, fallback: `.png`
- wysokośc logo: 44px
- Lokalizacja: zawsze `assets/hslogo.svg` lub `assets/hslogo.png` względem projektu
- Jeśli plik nie istnieje: aplikacja wyświetla w miejscu logo tekst `[brak logo]` w kolorze `rgba(255,255,255,0.5)` i loguje ostrzeżenie w konsoli
- Klik w logo → otwiera `https://higma-service.pl` w domyślnej przeglądarce systemowej

---

## 7. EKRAN INSTRUKCJI — SPECYFIKACJA

| Właściwość       | Wartość                                              |
|------------------|------------------------------------------------------|
| Tło              | `#FFFFFF`                                            |
| Padding          | 24px (wszystkie strony)                              |
| Tytuł ekranu     | "Instrukcja — [Nazwa Aplikacji]", 28px, weight 700   |
| Kolor tytułu     | `#54595F`                                            |
| Treść            | Roboto 14px, kolor `#7A7A7A`, line-height 1.6        |
| Przycisk "Wróć"  | Secondary Button, lewym górnym rogu pod TopBarem     |

**Kiedy Codex pisze treść instrukcji:**
- Dopiero po akceptacji wszystkich funkcjonalności aplikacji przez właściciela projektu
- Instrukcja musi opisywać: cel aplikacji, jak jej używać krok po kroku (user journey), co oznaczają poszczególne pola i przyciski
- Język: polski, prosty, zrozumiały dla pracownika biurowego (nie technika)

---

## 8. LAYOUT APLIKACJI — OGÓLNA STRUKTURA

```
┌──────────────────────────────────────────┐
│              TOPBAR (80px)               │  ← stały, zawsze na górze
├──────────────────────────────────────────┤
│                                          │
│           GŁÓWNA ZAWARTOŚĆ               │  ← zmienna, per aplikacja
│         (padding: 24px wszędzie)         │
│                                          │
│                                          │
└──────────────────────────────────────────┘
```

- Minimalna szerokość okna: `900px`
- Minimalna wysokość okna: `700px`
- Domyślny rozmiar: `980 x 760px`
- Tło głównej zawartości: `#FFFFFF`
- Padding zawartości od TopBaru: `24px`

---

## 9. ZASADY OGÓLNE

1. **Spójność ponad kreatywność** — jeśli komponent istnieje w tym design systemie, używasz go bez modyfikacji koloru ani rozmiaru.
2. **Szerokość przycisków jest zawsze elastyczna** — nigdy nie ustawiaj stałej szerokości. Padding 20px z każdej strony + auto width.
3. **Tekst na niebieskim tle zawsze biały** — dotyczy TopBaru i Primary Button.
4. **Każdy interaktywny element ma zdefiniowany stan hover** — brak "nagłych" zmian, przejścia 150ms.
5. **Brakujące logo = ostrzeżenie, nie crash** — aplikacja działa dalej, informuje o brakującym pliku.
6. **Instrukcja zawsze istnieje** — każda aplikacja musi mieć wypełniony ekran instrukcji przed wdrożeniem.
7. **Hierarchia kolorów CTA**: Primary Button dla głównej akcji (np. Start), Secondary dla akcji pomocniczych (np. Otwórz wynik).
