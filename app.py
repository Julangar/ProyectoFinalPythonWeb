import os.path

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

dir_folder = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(dir_folder, "inventario.db"))

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo Tabla Articulos
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    marca = db.Column(db.Text)
    precio = db.Column(db.Integer)
    #imagen = db.Column(db.Text)
    nombre = db.Column(db.Text)
    #mimetype = db.Column(db.Text)
    approved = db.Column(db.Boolean)

# Modelo Tabla Cliente
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cedula = db.Column(db.Text)
    nombre = db.Column(db.Text)
    apellido = db.Column(db.Text)
    compra = db.Column(db.Text)
    approved = db.Column(db.Boolean)

# Funciones CRUD
def create_article(mar, pre, nom):
    article = Article(marca=mar, precio=pre, nombre=nom)
    db.session.add(article)
    db.session.commit()
    db.session.refresh(article)


def create_client(ced, nom, ape):
    client = Client(cedula=ced, nombre=nom, apellido=ape, compra="")
    db.session.add(client)
    db.session.commit()
    db.session.refresh(client)


def read_articles():
    return db.session.query(Article).all()


def read_clients():
    return db.session.query(Client).all()


def update_article(article_id, precio):
    db.session.query(Article).filter_by(id=article_id).update({
        "precio": precio
    })
    db.session.commit()


def delete_article(article_id):
    db.session.query(Article).filter_by(id=article_id).delete()
    db.session.commit()


def update_client(client_id, nombre):
    db.session.query(Client).filter_by(id=client_id).update({
        "nombre": nombre
    })
    db.session.commit()


def update_compra(client_id, compra):
    db.session.query(Client).filter_by(id=client_id).update({
        "compra": compra
    })
    db.session.commit()


def delete_client(client_id):
    db.session.query(Client).filter_by(id=client_id).delete()
    db.session.commit()

# Rutas
@app.route("/", methods=["POST", "GET"])
def view_index():
    return render_template("index.html", articles=read_articles(), clients=read_clients())


@app.route("/articulos", methods=["POST", "GET"])
def view_articles():
    if request.method == "POST":
        create_article(request.form["mar"], request.form["pre"], request.form["nom"])
    return render_template("articulos.html", articles=read_articles())

"""@app.route("/upload_image", methods=["POST"])
def upload_image():
    imagen = request.files["imagen"]

    if not imagen:
        return "Imagen no cargada", 400

    filename = secure_filename(imagen.filename)
    mimetype = imagen.mimetype

    article = Article(imagen=imagen.read(), mimetype=mimetype,nombre=filename)
    db.session.add(article)
    db.session.commit()

    return "Imagen cargada", 200"""


@app.route("/clientes", methods=["POST", "GET"])
def view_clients():
    if request.method == "POST":
        create_client(request.form["ced"], request.form["nom"], request.form["ape"])
    return render_template("clientes.html", clients=read_clients())


@app.route("/edit_article/<article_id>", methods=["POST", "GET"])
def edit_article(article_id):
    if request.method == "POST":
        update_article(article_id, precio=request.form['pre'])
    elif request.method == "GET":
        delete_article(article_id)
    return redirect("/articulos", code=302)


@app.route("/edit_client/<client_id>", methods=["POST", "GET"])
def edit_client(client_id):
    if request.method == "POST":
        update_client(client_id, nombre=request.form['nom'])
    elif request.method == "GET":
        delete_client(client_id)
    return redirect("/clientes", code=302)


@app.route("/update_compra/<client_id>", methods=["POST", "GET"])
def update_com(client_id):
    if request.method == "POST":
        update_compra(client_id, compra=request.form['com'])

    return redirect("/", code=302)

# Init
if __name__ == "__main__":
    db.create_all()
    app.run()
