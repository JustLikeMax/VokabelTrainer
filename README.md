# VokabelTrainer

Ein kleiner Flask-basierter Vokabeltrainer mit SQLite und Desktop-Start über `pywebview`.

## Projektstruktur

```text
.
├── app.py                     # Einstiegspunkt für Desktop-Start
├── templates/                 # HTML-Templates
├── static/                    # CSS/Assets
└── vokabeltrainer/
    ├── __init__.py            # create_app() + zentrale App-Konfiguration
    ├── models.py              # SQLAlchemy-Modelle
    ├── routes.py              # HTTP-Routen
    └── desktop.py             # pywebview-Startlogik
```

## Startbefehle

### 1) Desktop-App (pywebview)

```bash
python app.py
```

### 2) Flask-Entwicklungsserver (ohne WebView)

```bash
flask --app "vokabeltrainer:create_app" run --debug
```

## Hinweise zur Initialisierung

- Die Flask-App wird per Application Factory (`create_app`) erstellt.
- `db = SQLAlchemy()` ist ohne direktes App-Binding definiert und wird in `create_app()` mit `db.init_app(app)` gebunden.
- Die Datenbanktabellen werden beim Desktop-Start in `start_desktop_app(...)` erstellt.
