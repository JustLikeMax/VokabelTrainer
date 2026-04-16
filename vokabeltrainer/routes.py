import random

from flask import Flask, redirect, render_template, request, url_for

from . import db
from .models import Vokabel


def register_routes(app: Flask) -> None:
    @app.route("/")
    def index():
        vokabeln = Vokabel.query.all()
        if not vokabeln:
            return render_template("noVokabeln.html")
        vokabel_id = random.choice([v.id for v in vokabeln])
        vokabel = Vokabel.query.get(vokabel_id)
        return render_template("index.html", vokabel=vokabel)

    @app.route("/check", methods=["POST"])
    def check():
        vokabel_id = request.form["vokabel_id"]
        eingabe = request.form["eingabe"]
        vokabel = Vokabel.query.get(vokabel_id)
        if eingabe.lower() is None or eingabe.lower() == "":
            return render_template("index.html", vokabel=vokabel, wrong=True)
        if eingabe.lower() in vokabel.deutsch.lower():  # type: ignore
            return redirect(url_for("next", current_id=vokabel_id))
        return render_template("index.html", vokabel=vokabel, wrong=True)

    @app.route("/next/<int:current_id>")
    def next(current_id):
        vokabeln = Vokabel.query.all()
        if not vokabeln:
            return "Es sind keine Vokabeln vorhanden."
        available_vokabel_ids = [v.id for v in vokabeln if v.id != current_id]
        if not available_vokabel_ids:
            return redirect(url_for("index"))
        next_id = random.choice(available_vokabel_ids)
        next_vokabel = Vokabel.query.get(next_id)
        return render_template("index.html", vokabel=next_vokabel)

    @app.route("/edit")
    def edit():
        vokabeln = Vokabel.query.all()
        return render_template("edit.html", vokabeln=vokabeln)

    @app.route("/add", methods=["POST"])
    def add():
        franzoesisch = request.form["franzoesisch"]
        deutsch = request.form["deutsch"]
        vokabel = Vokabel(franzoesisch=franzoesisch, deutsch=deutsch)  # type: ignore
        db.session.add(vokabel)
        db.session.commit()
        return redirect(url_for("edit"))

    @app.route("/delete/<int:vokabel_id>")
    def delete(vokabel_id):
        vokabel = Vokabel.query.get(vokabel_id)
        db.session.delete(vokabel)
        db.session.commit()
        return redirect(url_for("edit"))

    @app.route("/save", methods=["POST"])
    def save():
        neu_franzoesisch = request.form.get("neu_franzoesisch")
        neu_deutsch = request.form.get("neu_deutsch")

        if neu_franzoesisch and neu_deutsch:
            neue_vokabel = Vokabel(franzoesisch=neu_franzoesisch, deutsch=neu_deutsch)  # type: ignore
            db.session.add(neue_vokabel)
            db.session.commit()

        return redirect("/edit")
