from flask import Flask, render_template, request, redirect, url_for, flash
import redis, json, os
from dotenv import load_dotenv
import uuid

# Configuración
load_dotenv()
app = Flask(__name__)
app.secret_key = "super_secret"  # para flash

r = redis.Redis(
    host=os.getenv("KEYDB_HOST", "localhost"),
    port=os.getenv("KEYDB_PORT", 6379),
    password=os.getenv("KEYDB_PASS", None),
    decode_responses=True
)

# Ruta principal - lista de libros
@app.route("/")
def index():
    libros = {}
    for key in r.scan_iter("libro:*"):
        libros[key.split(":")[1]] = json.loads(r.get(key))
    return render_template("index.html", libros=libros)

# Agregar libro
@app.route("/agregar", methods=["GET", "POST"])
def agregar_libro():
    if request.method == "POST":
        id_libro = str(uuid.uuid4())
        libro = {
            "titulo": request.form["titulo"],
            "autor": request.form["autor"],
            "genero": request.form["genero"],
            "estado": request.form["estado"]
        }
        r.set(f"libro:{id_libro}", json.dumps(libro))
        flash("Libro agregado correctamente ✅", "success")
        return redirect(url_for("index"))
    return render_template("agregar.html")
