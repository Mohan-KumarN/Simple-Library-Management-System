# Library Management System

A simple Library Management System built with **Flask (Python)** and **MySQL**.

## Features
- Dashboard (total books, total members, currently issued books, recent unreturned issues)
- Books management (add books, view status, return issued books)
- Members management (add members, view member list)
- Issue/Return flow (issues update book status + transactions)

## Project Structure
- `app.py` - Flask application and routes
- `templates/` - Jinja templates for the UI pages
  - `index.html` (dashboard)
  - `books.html`
  - `members.html`
  - `issue.html`
  - `base.html` (layout)
- `frontend/` - Node folder present in repo (but not runnable in current state)
- `library_db/` - database-related files (as provided)
- `backend/` - additional folder (contains `library.db` in this repo)

## Requirements
- Python 3.10+
- MySQL Server
- Python packages (install via pip)

## Setup
### 1) Install Python dependencies
```bash
pip install flask mysql-connector-python
```

### 2) Configure MySQL connection
Update `db_config` in `app.py`:
```py
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'library_db'
}
```

### 3) Create database tables
Create database `library_db` and the required tables.

> Note: This repo does not include the SQL schema as a plain text file in the visible files. If you already have a schema/DB, you can skip this step.

### 4) Run the app
```bash
python app.py
```

Server starts at:
- `http://127.0.0.1:5000/`

## Usage
- Open `http://127.0.0.1:5000/`
- Add books from `/books`
- Add members from `/members`
- Issue a book from `/issue`
- Return a book using the **Return** link in `/books`

## Frontend (Node/Express)
This repo includes a `frontend/` folder, but it does not contain runnable Node entry files (there is no `package.json` or server script). The working UI is provided by Flask templates.

## Troubleshooting
- **MySQL connection errors**: verify `host/user/password/database` in `app.py`.
- **500 errors on routes**: likely missing tables/columns or a different schema.
- **favicon 404**: harmless (no `favicon.ico` is included). 

