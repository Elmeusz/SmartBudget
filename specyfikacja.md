# Specyfikacja Projektu: SmartBudget

## Opis Aplikacji
SmartBudget (Manager Finansów) to intuicyjne webowe narzędzie do śledzenia osobistych wydatków i przychodów. Aplikacja pozwala użytkownikom na łatwe wprowadzanie danych finansowych, kategoryzowanie transakcji oraz monitorowanie stanu swojego budżetu, co pomaga w lepszym zarządzaniu finansami.

## Wymagania Techniczne
- **Backend:** Python z frameworkiem Flask
- **Baza danych:** SQLite
- **Frontend:** HTML, JavaScript (JS) oraz CSS

## Schemat Bazy Danych

System opiera się na relacyjnej bazie danych. Poniżej znajduje się struktura głównych tabel:

### 1. Tabela `Users` (Użytkownicy)
Tabela przechowująca dane użytkowników aplikacji.
- `id` (Primary Key, Integer): Unikalny identyfikator użytkownika.
- `username` (String): Nazwa logowania użytkownika.
- `password_hash` (String): Bezpieczny hash hasła.
- `email` (String): Adres e-mail.
- `created_at` (DateTime): Data i czas utworzenia konta.

### 2. Tabela `Categories` (Kategorie)
Tabela definiująca kategorie przypisywane do transakcji (np. Jedzenie, Czynsz, Wypłata).
- `id` (Primary Key, Integer): Unikalny identyfikator kategorii.
- `user_id` (Foreign Key -> `Users.id`, Integer): Powiązanie z konkretnym użytkownikiem (każdy użytkownik może mieć własne kategorie).
- `name` (String): Nazwa kategorii.
- `type` (String): Typ (np. `income` - przychód, `expense` - wydatek).

### 3. Tabela `Transactions` (Transakcje)
Tabela przechowująca konkretne wpisy finansowe (zarówno przychody, jak i wydatki).
- `id` (Primary Key, Integer): Unikalny identyfikator transakcji.
- `user_id` (Foreign Key -> `Users.id`, Integer): Autor transakcji.
- `category_id` (Foreign Key -> `Categories.id`, Integer): Kategoria, do której należy wpis.
- `amount` (Decimal/Float): Kwota transakcji.
- `description` (Text): Opcjonalny, dodatkowy opis wpisu.
- `date` (Date): Data realizacji transakcji.
