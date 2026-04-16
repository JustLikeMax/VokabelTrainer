import random
from flask import Flask, abort, redirect, render_template, request, url_for
from flask.typing import ResponseReturnValue
from flask_sqlalchemy import SQLAlchemy
import webview

app = Flask(__name__)
app.secret_key = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vokabeln.db"
db = SQLAlchemy(app)
window = webview.create_window(
    "Vokabeltrainer",
    app,  # type: ignore
)


class Vokabel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    franzoesisch = db.Column(db.String(100))
    deutsch = db.Column(db.String(100))


def _get_vokabel_or_abort(vokabel_id: int | str) -> Vokabel:
    try:
        normalized_id = int(vokabel_id)
    except (TypeError, ValueError):
        abort(400, description="Ungültige Vokabel-ID.")

    vokabel = db.session.get(Vokabel, normalized_id)
    if vokabel is None:
        abort(404, description="Vokabel nicht gefunden.")
    return vokabel


@app.route("/")
def index() -> ResponseReturnValue:
    vokabeln = Vokabel.query.all()
    if not vokabeln:
        return render_template("noVokabeln.html")
    vokabel_id = random.choice([v.id for v in vokabeln])
    vokabel = _get_vokabel_or_abort(vokabel_id)
    return render_template("index.html", vokabel=vokabel)


@app.route("/check", methods=["POST"])
def check() -> ResponseReturnValue:
    vokabel_id = request.form["vokabel_id"]
    eingabe = request.form["eingabe"]
    vokabel = _get_vokabel_or_abort(vokabel_id)
    if eingabe.lower() is None or eingabe.lower() == "":
        return render_template("index.html", vokabel=vokabel, wrong=True)
    if eingabe.lower() in vokabel.deutsch.lower():  # type: ignore
        return redirect(url_for("next", current_id=vokabel_id))
    else:
        return render_template("index.html", vokabel=vokabel, wrong=True)


@app.route("/next/<int:current_id>")
def next(current_id: int) -> ResponseReturnValue:
    vokabeln = Vokabel.query.all()
    if not vokabeln:
        return "Es sind keine Vokabeln vorhanden."
    available_vokabel_ids = [v.id for v in vokabeln if v.id != current_id]
    if not available_vokabel_ids:
        return redirect(url_for("index"))
    next_id = random.choice(available_vokabel_ids)
    next_vokabel = _get_vokabel_or_abort(next_id)
    return render_template("index.html", vokabel=next_vokabel)


@app.route("/edit")
def edit() -> ResponseReturnValue:
    vokabeln = Vokabel.query.all()
    return render_template("edit.html", vokabeln=vokabeln)


@app.route("/add", methods=["POST"])
def add() -> ResponseReturnValue:
    franzoesisch = request.form["franzoesisch"]
    deutsch = request.form["deutsch"]
    vokabel = Vokabel(franzoesisch=franzoesisch, deutsch=deutsch)  # type: ignore
    db.session.add(vokabel)
    db.session.commit()
    return redirect(url_for("edit"))


@app.route("/delete/<int:vokabel_id>")
def delete(vokabel_id: int) -> ResponseReturnValue:
    vokabel = _get_vokabel_or_abort(vokabel_id)
    db.session.delete(vokabel)
    db.session.commit()
    return redirect(url_for("edit"))


@app.route("/save", methods=["POST"])
def save() -> ResponseReturnValue:
    neu_franzoesisch = request.form.get("neu_franzoesisch")
    neu_deutsch = request.form.get("neu_deutsch")

    if neu_franzoesisch and neu_deutsch:
        neue_vokabel = Vokabel(franzoesisch=neu_franzoesisch, deutsch=neu_deutsch)  # type: ignore
        db.session.add(neue_vokabel)
        db.session.commit()

    return redirect("/edit")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    webview.start(debug=True)
