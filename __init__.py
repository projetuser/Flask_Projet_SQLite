import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('bibliotheque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Créer la base de données et exécuter le schéma
def create_db():
    connection = sqlite3.connect('bibliotheque.db')
    with open('schema1.sql') as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()

# Initialiser la base de données avec des utilisateurs et des livres par défaut
def init_db():
    connection = sqlite3.connect('bibliotheque.db')
    cur = connection.cursor()

    # Ajouter des utilisateurs
    cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('admin', generate_password_hash('adminpass'), 'admin'))
    cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('user1', generate_password_hash('userpass'), 'user'))
    cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('user2', generate_password_hash('userpass2'), 'user'))

    # Ajouter des livres
    cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ('Orgueil et Préjugés', 'Jane Austen', 1))
    cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ('Les Hauts de Hurle-Vent', 'Emily Brontë', 1))
    cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ('1984', 'George Orwell', 1))
    cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ("L'Étranger", 'Albert Camus', 1))
    cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ("L'Odyssée", 'Homère', 1))
    cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ("Le Petit Prince", 'Antoine de Saint-Exupéry', 1))
    cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ("Harry Potter à l'école des sorciers", 'J.K. Rowling', 1))
    cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ("Les Misérables", 'Victor Hugo', 1))

    connection.commit()
    connection.close()
    print("Base de données initialisée avec succès!")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/livres', methods=['GET'])
def list_books():
    conn = get_db_connection()
    livres = conn.execute('SELECT * FROM livres WHERE disponible = 1').fetchall()
    conn.close()
    return render_template('list_books.html', livres=livres)

@app.route('/ajouter-livre', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        conn = get_db_connection()
        conn.execute('INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)', (titre, auteur, 1))
        conn.commit()
        conn.close()
        return redirect(url_for('list_books'))
    return render_template('add_book.html')

@app.route('/emprunter-livre', methods=['GET', 'POST'])
def borrow_book():
    if request.method == 'POST':
        livre_id = request.form['livre_id']
        user_id = 1  # A remplacer avec la gestion de l'utilisateur connecté
        conn = get_db_connection()
        conn.execute('INSERT INTO emprunts (user_id, livre_id) VALUES (?, ?)', (user_id, livre_id))
        conn.execute('UPDATE livres SET disponible = 0 WHERE id = ?', (livre_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('list_books'))
    conn = get_db_connection()
    livres = conn.execute('SELECT * FROM livres WHERE disponible = 1').fetchall()
    conn.close()
    return render_template('borrow_book.html', livres=livres)

@app.route('/gestion-utilisateurs', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        conn = get_db_connection()
        conn.execute('INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)', (username, password, role))
        conn.commit()
        conn.close()
    return render_template('manage_users.html')

if __name__ == '__main__':
    create_db()
    init_db()
    app.run(debug=True)
