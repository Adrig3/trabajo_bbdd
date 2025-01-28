# imports
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# bbdd
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(20))
    autor = db.Column(db.String(20))
    genero = db.Column(db.String(10))
    fecha_publicacion = db.Column(db.String(20))

    def __repr__(self):
        return f'Libro {self.titulo}'

# endpoint de testing
@app.route('/prueba')
def prueba():
    return render_template("prueba.html")

# endpoint principal - lista de libros
@app.route('/book')
def get_books():
    books = Book.query.all()
    return render_template("books.html", books=books)

# endpoint para añadir
@app.route('/add_book/', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        genero = request.form.get('genero')
        fecha_publicacion = request.form.get('fecha_publicacion')

        new_book = Book(
            titulo=titulo, 
            autor=autor, 
            genero=genero, 
            fecha_publicacion=fecha_publicacion
        )

        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('get_books'))

    return render_template("add_book.html")

# endpoint para borrar
@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('get_books'))
    return jsonify({"error": "Libro no encontrado"}), 404

# endpoint para editar
@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get(book_id)

    if not book:
        return jsonify({"error": "Libro no encontrado"}), 404

    if request.method == 'POST':
        book.titulo = request.form.get('titulo')
        book.autor = request.form.get('autor')
        book.genero = request.form.get('genero')
        book.fecha_publicacion = request.form.get('fecha_publicacion')
        db.session.commit()
        return redirect(url_for('get_books'))

    return render_template('edit_book.html', book=book)

# endpoint para buscar por id
@app.route('/get_book_by_id', methods=['POST'])
def get_book_by_id():
    book_id = request.form.get('id')

    if book_id:
        book = Book.query.get(book_id)
        if book:
            return jsonify({
                "id": book.id,
                "titulo": book.titulo,
                "autor": book.autor,
                "genero": book.genero,
                "fecha_publicacion": book.fecha_publicacion
            })
        return jsonify({"error": "Libro no encontrado"}), 404

    return jsonify({"error": "Libro no encontrado"}), 400

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)