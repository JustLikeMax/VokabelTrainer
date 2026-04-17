import webview

from . import db


def start_desktop_app(app, debug: bool = True) -> None:
    with app.app_context():
        db.create_all()

    webview.create_window(
        "Vokabeltrainer",
        app,  # type: ignore[arg-type]
    )
    webview.start(debug=debug)
