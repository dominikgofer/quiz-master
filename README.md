# Platforma Quizowa - Projekt Django MPA

W pełni funkcjonalna platforma quizowa zbudowana z użyciem Django, implementująca architekturę Multi-Page Application (MPA) z szablonami. Projekt spełnia wymagania kursu *Techniki Internetowe*.

## 📋 Spis treści

- [Funkcjonalności](#funkcjonalności)
- [Stos technologiczny](#stos-technologiczny)
- [Instalacja i konfiguracja](#instalacja-i-konfiguracja)
- [Użytkowanie](#użytkowanie)
- [Struktura projektu](#struktura-projektu)
- [Testowe konta użytkowników](#testowe-konta-użytkowników)
- [Rozwój projektu](#rozwój-projektu)
- [Zgodność ze standardami](#zgodność-ze-standardami)

## ✨ Funkcjonalności

### Role użytkowników i autoryzacja
- **Dwupoziomowy system autoryzacji:**
  - **Studenci:** Rozwiązywanie quizów, przeglądanie wyników, historia i rankingi
  - **Nauczyciele:** Tworzenie/edycja quizów, zarządzanie pytaniami, raporty i analityka
- Autoryzacja oparta na sesjach z wbudowanym systemem Django
- Rejestracja użytkowników z wyborem roli
- Zarządzanie profilem z obsługą awatarów

### Zarządzanie quizami (Nauczyciele)
- Tworzenie i edycja quizów z różnymi ustawieniami:
  - Kategorie, poziomy trudności, limity czasowe
  - Próg zaliczenia, maksymalna liczba prób
  - Losowanie pytań, ustawienia wyświetlania odpowiedzi
- Wiele typów pytań:
  - Jednokrotnego wyboru
  - Wielokrotnego wyboru
  - Prawda/Fałsz
  - Krótka odpowiedź (tekst)
- Dodawanie wyjaśnień i obrazów do pytań
- Szczegółowe raporty i analityka

### Rozwiązywanie quizów (Studenci)
- Przeglądanie dostępnych quizów z filtrowaniem i wyszukiwaniem
- Timer w czasie rzeczywistym dla quizów czasowych
- Auto-zapis postępu (localStorage)
- Natychmiastowy feedback po zakończeniu
- Przeglądanie szczegółowych wyników z wyjaśnieniami
- Śledzenie historii i wyników

### Dodatkowe funkcjonalności
- Rankingi (per quiz i globalne)
- Dashboard ze statystykami dla obu ról
- Responsywny design z Bootstrap 5
- Zgodność z HTML5 W3C
- Interaktywne funkcje z vanilla JavaScript

## 🛠 Stos technologiczny

- **Backend:** Django 6.0+ (Python 3.12+)
- **Baza danych:** SQLite (deweloperska)
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Framework CSS:** Bootstrap 5.3
- **Ikony:** Font Awesome 6.4
- **Architektura:** MPA (Multi-Page Application) z szablonami Django
- **Zarządzanie pakietami:** uv (zalecane) lub pip

## 🚀 Instalacja i konfiguracja

### Wymagania wstępne
- Python 3.12 lub nowszy
- uv package manager (zalecane) lub pip
- Git

### Instrukcje instalacji

1. **Sklonuj repozytorium:**
   ```bash
   git clone <repository-url>
   cd techniki-internetowe
   ```

2. **Zainstaluj zależności:**
   ```bash
   # Używając uv (zalecane)
   uv pip install -e .
   
   # Lub używając pip
   pip install -e .
   ```

3. **Zainstaluj zależności deweloperskie (opcjonalnie):**
   ```bash
   uv pip install -e ".[dev]"
   ```

4. **Wykonaj migracje bazy danych:**
   ```bash
   uv run python manage.py migrate
   ```

5. **Załaduj przykładowe dane:**
   ```bash
   uv run python manage.py load_sample_data
   ```
   
   To polecenie utworzy:
   - Przykładowe kategorie (Python, JavaScript, Bazy danych, Web Development)
   - Testowych użytkowników (nauczyciel i student)
   - Przykładowe quizy z pytaniami
   - Przykładowe wyniki

6. **Utwórz superużytkownika (opcjonalnie):**
   ```bash
   uv run python manage.py createsuperuser
   ```

7. **Uruchom serwer deweloperski:**
   ```bash
   # Bezpośrednio
   uv run python manage.py runserver
   
   # Lub używając skryptu pomocniczego
   ./utils/run_django.sh
   ```

8. **Otwórz aplikację w przeglądarce:**
   - Strona główna: http://localhost:8000/
   - Panel administracyjny: http://localhost:8000/admin/

## 📖 Użytkowanie

### Dla studentów

1. **Rejestracja:**
   - Przejdź do strony rejestracji
   - Wybierz rolę "Student"
   - Wypełnij formularz

2. **Rozwiązywanie quizów:**
   - Przeglądaj dostępne quizy na stronie "Browse Quizzes"
   - Kliknij "Take Quiz" aby rozpocząć
   - Odpowiadaj na pytania
   - Zobacz wyniki i wyjaśnienia po zakończeniu

3. **Śledzenie postępów:**
   - Dashboard - statystyki i ostatnie wyniki
   - My History - pełna historia rozwiązanych quizów
   - Leaderboard - rankingi

### Dla nauczycieli

1. **Tworzenie quizu:**
   - Przejdź do "Create Quiz"
   - Wypełnij informacje o quizie (tytuł, opis, kategoria, trudność)
   - Ustaw parametry (limit czasowy, liczba prób, próg zaliczenia)
   - Zapisz quiz

2. **Dodawanie pytań:**
   - Otwórz quiz i kliknij "Manage Questions"
   - Dodaj pytania różnych typów
   - Określ poprawne odpowiedzi
   - Dodaj wyjaśnienia (opcjonalnie)

3. **Analityka:**
   - Przejdź do "Reports" dla wybranego quizu
   - Zobacz statystyki prób
   - Analizuj najtrudniejsze pytania

## 📁 Struktura projektu

```
techniki-internetowe/
├── accounts/              # Aplikacja zarządzania użytkownikami
│   ├── models.py         # Model profilu użytkownika
│   ├── views.py          # Widoki rejestracji, logowania, profilu
│   ├── forms.py          # Formularze użytkownika
│   └── urls.py           # Routing aplikacji accounts
├── quizzes/              # Główna aplikacja quizów
│   ├── models.py         # Modele: Quiz, Question, Answer, Result
│   ├── views.py          # Widoki quizów, pytań, wyników
│   ├── forms.py          # Formularze quizów i pytań
│   ├── urls.py           # Routing aplikacji quizzes
│   └── management/       # Komendy Django
│       └── commands/
│           └── load_sample_data.py
├── quiz_platform/        # Ustawienia projektu
│   ├── settings.py       # Konfiguracja Django
│   ├── urls.py           # Główny routing
│   └── wsgi.py           # WSGI config
├── templates/            # Szablony HTML
│   ├── base.html         # Szablon bazowy
│   ├── accounts/         # Szablony kont użytkowników
│   └── quizzes/          # Szablony quizów
├── static/               # Pliki statyczne
│   ├── css/
│   │   └── style.css     # Niestandardowe style
│   └── js/
│       └── main.js       # JavaScript aplikacji
├── utils/                # Narzędzia pomocnicze
│   └── run_django.sh     # Skrypt uruchamiający serwer
├── specification/        # Dokumentacja projektu
├── manage.py             # Narzędzie Django CLI
├── pyproject.toml        # Konfiguracja projektu i zależności
└── README.md             # Ten plik
```

## 👥 Testowe konta użytkowników

Po załadowaniu przykładowych danych dostępne są następujące konta:

### Nauczyciel
- **Login:** teacher
- **Hasło:** teacher123
- **Uprawnienia:** Tworzenie quizów, zarządzanie pytaniami, przeglądanie raportów

### Student
- **Login:** student
- **Hasło:** student123
- **Uprawnienia:** Rozwiązywanie quizów, przeglądanie wyników, rankingi

## 🔧 Rozwój projektu

### Komendy deweloperskie

**Uruchomienie serwera:**
```bash
uv run python manage.py runserver
# lub
./utils/run_django.sh
```

**Tworzenie migracji:**
```bash
uv run python manage.py makemigrations
```

**Aplikowanie migracji:**
```bash
uv run python manage.py migrate
```

**Tworzenie superużytkownika:**
```bash
uv run python manage.py createsuperuser
```

**Zbieranie plików statycznych (produkcja):**
```bash
uv run python manage.py collectstatic
```

**Walidacja HTML:**
```bash
uv run python validate_html.py
```

**Testy:**
```bash
uv run python manage.py test
```

### Struktura bazy danych

**Główne modele:**

- **User** - Wbudowany model Django
- **Profile** - Rozszerzenie użytkownika (rola, awatar, statystyki)
- **Category** - Kategorie quizów
- **Quiz** - Quizy z ustawieniami
- **Question** - Pytania quizowe
- **Answer** - Odpowiedzi do pytań
- **QuizAttempt** - Próby rozwiązania quizu
- **UserAnswer** - Odpowiedzi użytkownika

### Główne ścieżki URL

- `/` - Strona główna z wyróżnionymi quizami
- `/quizzes/` - Przeglądaj wszystkie quizy
- `/quiz/<id>/` - Szczegóły quizu
- `/quiz/<id>/take/` - Rozwiąż quiz
- `/quiz/<id>/result/<attempt_id>/` - Wyniki
- `/dashboard/` - Panel użytkownika
- `/accounts/login/` - Logowanie
- `/accounts/register/` - Rejestracja
- `/accounts/profile/` - Profil użytkownika
- `/admin/` - Panel administracyjny Django

### Funkcje bezpieczeństwa

- Ochrona CSRF na wszystkich formularzach
- Zapobieganie SQL injection (Django ORM)
- Zapobieganie XSS (auto-escape w szablonach)
- Hashowanie haseł (wbudowane w Django)
- Bezpieczeństwo sesji
- Sprawdzanie uprawnień dla widoków nauczycieli

## 📝 Zgodność ze standardami

- **HTML5:** Wszystkie szablony są zgodne z HTML5
- **W3C Validation:** Kod HTML przechodzi walidację W3C
- **Responsywność:** Aplikacja działa na urządzeniach mobilnych, tabletach i desktopach
- **Dostępność:** Przestrzeganie podstawowych zasad dostępności
- **Kodowanie:** Wszystkie pliki używają UTF-8
- **Przeglądarki:** Testowane w Firefox, Chrome, Edge

### Walidacja HTML5

Projekt zawiera skrypt do sprawdzania zgodności z HTML5:

```bash
uv run python validate_html.py
```

Skrypt:
- Renderuje szablony Django
- Waliduje zgodność ze standardem HTML5 W3C
- Wyświetla błędy i ostrzeżenia z numerami linii
- Generuje raport podsumowujący

## 🎨 Dostosowywanie

### Dodawanie nowych kategorii

**Przez panel administracyjny:**
1. Przejdź do `/admin/` → Categories → Add category

**Przez Django shell:**
```python
from quizzes.models import Category
Category.objects.create(
    name="Matematyka",
    description="Quizy matematyczne",
    color="#3498db",
    icon="fas fa-calculator"
)
```

### Tworzenie quizów

1. Zaloguj się jako nauczyciel
2. Kliknij "Create Quiz" w nawigacji
3. Wypełnij szczegóły i ustawienia quizu
4. Dodaj pytania i odpowiedzi
5. Opublikuj gdy gotowe

## 🚀 Wdrożenie produkcyjne

Dla wdrożenia produkcyjnego:

1. **Konfiguracja Django:**
   - Ustaw `DEBUG = False`
   - Skonfiguruj `ALLOWED_HOSTS`
   - Użyj zmiennych środowiskowych dla sekretów

2. **Baza danych:**
   - Przejdź na PostgreSQL lub MySQL
   - Skonfiguruj connection pooling

3. **Pliki statyczne:**
   - Uruchom `collectstatic`
   - Skonfiguruj CDN (opcjonalnie)

4. **Serwer WWW:**
   - Użyj Gunicorn jako WSGI server
   - Skonfiguruj Nginx jako reverse proxy
   - Ustaw certyfikat SSL

5. **Bezpieczeństwo:**
   - Włącz HTTPS
   - Skonfiguruj nagłówki bezpieczeństwa
   - Włącz rate limiting

## ✅ Zgodność z wymaganiami projektu

✅ **Architektura MPA:** Django templates z renderowaniem po stronie serwera  
✅ **Baza danych:** SQLite (deweloperska), możliwość zmiany na PostgreSQL/MySQL  
✅ **Autoryzacja:** Dwupoziomowy system ról (Student/Nauczyciel)  
✅ **Zarządzanie sesjami:** Framework sesji Django  
✅ **Walidacja HTML5:** Zgodność z W3C, zawiera skrypt walidacyjny  
✅ **Kodowanie UTF-8:** Wszystkie pliki używają UTF-8  
✅ **Responsywny design:** Działa w Firefox, Chrome, Edge  
✅ **Ulepszenia po stronie klienta:** JavaScript dla timerów, auto-zapisu, walidacji  

## 🐛 Znane ograniczenia

- SQLite jako baza danych (zalecane PostgreSQL dla produkcji)
- Brak cache'owania (zalecane Redis dla produkcji)
- Obrazy przechowywane lokalnie (zalecane CDN dla produkcji)
- Brak eksportu wyników do CSV/PDF (w planach)

## 🤝 Wkład w projekt

1. Fork repozytorium
2. Utwórz branch z funkcją (`git checkout -b feature/nazwa-funkcji`)
3. Commituj zmiany (`git commit -m 'Dodaj: opis funkcji'`)
4. Push do brancha (`git push origin feature/nazwa-funkcji`)
5. Otwórz Pull Request

## 📄 Licencja

Projekt edukacyjny dla kursu *Techniki Internetowe*.

## 📞 Kontakt

W przypadku pytań dotyczących projektu, skontaktuj się z prowadzącym kurs.

---

**Projekt:** Techniki Internetowe  
**Data:** Styczeń 2026  
**Wersja:** 1.0

