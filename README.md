# SmartBudget

## Cel projektu
SmartBudget to prosta, ale skuteczna aplikacja webowa pełniąca rolę osobistego managera finansów. Jej głównym celem jest umożliwienie użytkownikom łatwego i regularnego śledzenia swoich wydatków oraz przychodów, kategoryzowania ich i lepszego kontrolowania domowego budżetu.

## Technologie
Projekt został zbudowany przy użyciu następujących technologii:
- **Backend:** Python z frameworkiem webowym Flask
- **Baza danych:** SQLite
- **Wizualizacja danych:** Chart.js (JavaScript)
- **Frontend:** HTML, CSS, JavaScript

## Instrukcja uruchomienia

Postępuj zgodnie z poniższymi krokami, aby uruchomić aplikację w środowisku lokalnym.

### 1. Stworzenie wirtualnego środowiska (venv)
Otwórz terminal w folderze projektu i wpisz poniższe polecenie:
```bash
python -m venv venv
```
Po utworzeniu aktywuj je:
- **Na systemie Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Na systemach Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```

### 2. Instalacja zależności (Flask)
Przy aktywowanym wirtualnym środowisku zainstaluj framework Flask (oraz ewentualnie inne potrzebne paczki):
```bash
pip install Flask
```

### 3. Uruchomienie aplikacji
Aby uruchomić serwer developerski i włączyć aplikację, wykonaj w terminalu:
```bash
python app.py
```
Aplikacja powinna uruchomić się lokalnie – w terminalu pojawi się adres (najpewniej `http://127.0.0.1:5000/`), który wystarczy otworzyć w przeglądarce.
