# Capacitaciones +

Aplicación Django para explorar cursos, inscribirse, registrar el progreso, valorar cursos y administrar materiales de aprendizaje.

## Requisitos

- Python 3.10 o superior
- Git (opcional, para clonar el repositorio)

## Instalación local en Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requerimientos.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Abre `http://127.0.0.1:8000/` en el navegador. Sin `DB_NAME`, la aplicación usa SQLite y crea `db.sqlite3` al ejecutar las migraciones.

## Usar MySQL

Completa `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` y `DB_PORT` en `.env`, e instala el controlador:

```powershell
.\.venv\Scripts\python.exe -m pip install mysqlclient
.\.venv\Scripts\python.exe manage.py migrate
```

En producción, configura una `SECRET_KEY` aleatoria, `DEBUG=false` y `ALLOWED_HOSTS` con los dominios de la aplicación.
