from __future__ import annotations

import os
from io import BytesIO
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_file
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from excel_script import modificar_archivo


ALLOWED_EXTENSIONS = {".xlsx", ".xlsm", ".xltx", ".xltm", ".xml"}
MIME_BY_EXTENSION = {
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xlsm": "application/vnd.ms-excel.sheet.macroEnabled.12",
    ".xltx": "application/vnd.openxmlformats-officedocument.spreadsheetml.template",
    ".xltm": "application/vnd.ms-excel.template.macroEnabled.12",
    ".xml": "application/xml",
}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20 MB
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")


def extension_permitida(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.errorhandler(RequestEntityTooLarge)
def archivo_muy_grande(_error):
    flash("El archivo supera el tamano maximo permitido (20 MB).")
    return redirect("/")


@app.post("/procesar")
def procesar_excel():
    archivo = request.files.get("archivo")

    if archivo is None or archivo.filename == "":
        flash("Debes seleccionar un archivo Excel o XML.")
        return redirect("/")

    nombre_seguro = secure_filename(archivo.filename)
    extension = Path(nombre_seguro).suffix.lower()

    if not extension_permitida(nombre_seguro):
        flash("Formato no soportado. Usa: .xlsx, .xlsm, .xltx, .xltm o .xml")
        return redirect("/")

    contenido = archivo.read()
    if not contenido:
        flash("El archivo está vacío.")
        return redirect("/")

    try:
        salida: BytesIO = modificar_archivo(contenido, extension)
    except ValueError as exc:
        flash(str(exc))
        return redirect("/")

    base = Path(nombre_seguro).stem
    nombre_salida = f"{base}_modificado{extension}"

    return send_file(
        salida,
        as_attachment=True,
        download_name=nombre_salida,
        mimetype=MIME_BY_EXTENSION[extension],
    )


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug)
