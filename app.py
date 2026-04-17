from vokabeltrainer import create_app
from vokabeltrainer.desktop import start_desktop_app


app = create_app()


if __name__ == "__main__":
    start_desktop_app(app, debug=True)
