# VokabelTrainer

- Download the code and run `app.py`.

## SECRET_KEY configuration

The application reads the Flask secret key from the `SECRET_KEY` environment variable.

### Local development

For local development (`FLASK_ENV=development` or `FLASK_DEBUG=1`), the app uses a development-only fallback key if `SECRET_KEY` is not set.

### Non-development environments

In non-development environments, `SECRET_KEY` is required. The app raises a `RuntimeError` if it is missing.

### Set `SECRET_KEY`

macOS/Linux:

```bash
export SECRET_KEY="your-long-random-secret"
python app.py
```

Windows PowerShell:

```powershell
$env:SECRET_KEY = "your-long-random-secret"
python app.py
```
