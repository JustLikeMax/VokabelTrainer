import random

from flask import Flask, abort, redirect, render_template, request, url_for
from flask.typing import ResponseReturnValue

from . import db
from .models import Vokabel


def _get_vokabel_or_abort(vokabel_id: int | str) -> Vokabel:
    try:
        normalized_id = int(vokabel_id)
    except (TypeError, ValueError):
        abort(400, description="Ungültige Vokabel-ID.")

    vokabel = db.session.get(Vokabel, normalized_id)
    if vokabel is None:
        abort(404, description="Vokabel nicht gefunden.")
    return vokabel


def register_routes(app: Flask) -> None:
    @app.route("/")
    def index() -> ResponseReturnValue:
        vokabeln = Vokabel.query.all()
        if not vokabeln:
            return render_template("noVokabeln.html")
        vokabel = random.choice(vokabeln)
        return render_template("index.html", vokabel=vokabel)

    @app.route("/check", methods=["POST"])
    def check() -> ResponseReturnValue:
        vokabel_id = request.form["vokabel_id"]
        eingabe = request.form["eingabe"]
        vokabel = _get_vokabel_or_abort(vokabel_id)
        if not eingabe or not eingabe.strip():
            return render_template("index.html", vokabel=vokabel, wrong=True)
        eingabe_lower = eingabe.lower()
        if eingabe_lower in vokabel.deutsch.lower():  # type: ignore
            return redirect(url_for("next", current_id=vokabel_id))
        return render_template("index.html", vokabel=vokabel, wrong=True)

    @app.route("/next/<int:current_id>")
    def next(current_id: int) -> ResponseReturnValue:
        vokabeln = Vokabel.query.all()
        if not vokabeln:
            return "Es sind keine Vokabeln vorhanden."
        available = [v for v in vokabeln if v.id != current_id]
        if not available:
            return redirect(url_for("index"))
        next_vokabel = random.choice(available)
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

    @app.route("/delete/<int:vokabel_id>", methods=["POST"])
    def delete(vokabel_id: int) -> ResponseReturnValue:
        vokabel = _get_vokabel_or_abort(vokabel_id)
        db.session.delete(vokabel)
        db.session.commit()
        return redirect(url_for("edit"))

    @app.route("/save", methods=["POST"])
    def save() -> ResponseReturnValue:
        ids = request.form.getlist("id[]")
        franzoesisch_liste = request.form.getlist("franzoesisch[]")
        deutsch_liste = request.form.getlist("deutsch[]")
        neu_franzoesisch = request.form.get("neu_franzoesisch")
        neu_deutsch = request.form.get("neu_deutsch")

        if len(ids) != len(franzoesisch_liste) or len(ids) != len(deutsch_liste):
            abort(400, description="Ungültige Formulardaten: Listen haben unterschiedliche Längen.")

        valid_ids: list[int] = []
        for vokabel_id in ids:
            try:
                valid_ids.append(int(vokabel_id))
            except (TypeError, ValueError):
                abort(400, description="Ungültige Vokabel-ID.")

        vokabel_map = {
            v.id: v
            for v in Vokabel.query.filter(Vokabel.id.in_(valid_ids)).all()
        }

        for datensatz_id, franzoesisch, deutsch in zip(valid_ids, franzoesisch_liste, deutsch_liste):
            bereinigtes_franzoesisch = franzoesisch.strip()
            bereinigtes_deutsch = deutsch.strip()
            if not bereinigtes_franzoesisch or not bereinigtes_deutsch:
                continue

            vokabel = vokabel_map.get(datensatz_id)
            if vokabel is None:
                continue

            vokabel.franzoesisch = bereinigtes_franzoesisch
            vokabel.deutsch = bereinigtes_deutsch

        bereinigtes_neu_franzoesisch = (neu_franzoesisch or "").strip()
        bereinigtes_neu_deutsch = (neu_deutsch or "").strip()
        if bereinigtes_neu_franzoesisch and bereinigtes_neu_deutsch:
            neue_vokabel = Vokabel(  # type: ignore
                franzoesisch=bereinigtes_neu_franzoesisch,
                deutsch=bereinigtes_neu_deutsch,
            )
            db.session.add(neue_vokabel)

        db.session.commit()

        return redirect(url_for("edit"))
