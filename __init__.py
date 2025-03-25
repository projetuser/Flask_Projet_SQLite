import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'  # Nécessaire pour la gestion de session

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('bibliotheque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Fonction pour vérifier les informations de connexion
def verify_user(username, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM utilisateurs WHERE username = ?', (username,)).fetchone()
    conn.close()
    if user and check_password_hash(user['password'], password):
        return user
    return None

# Page d'accueil avec le formulaire de connexion
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = verify_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html', error="Nom d'utilisateur ou mot de passe incorrect")
    return render_template('index.html')

# Page de connexion réussie
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    if session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('user_dashboard'))

# Page de l'administrateur
@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))
    return render_template('admin_dashboard.html')

# Page de l'utilisateur
@app.route('/user-dashboard')
def user_dashboard():
    if 'user_id' not in session or session['role'] != 'user':
        return redirect(url_for('home'))
    return render_template('user_dashboard.html')

# Déconnexion
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Page d'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = 'user'  # Par défaut, les nouveaux utilisateurs sont des utilisateurs
        conn = get_db_connection()
        conn.execute('INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)', (username, password, role))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('register.html')

# Fonction pour ajouter un livre (page d'administration)
@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))

    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        conn = get_db_connection()
        conn.execute('INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)', (titre, auteur, 1))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_dashboard'))

    return render_template('add_book.html')

# Fonction pour afficher la liste des livres disponibles (pour tous les utilisateurs)
@app.route('/list-books')
def list_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM livres WHERE disponible = 1').fetchall()
    conn.close()
    return render_template('list_books.html', books=books)

# Fonction pour emprunter un livre (pour les utilisateurs)
@app.route('/borrow-book/<int:book_id>')
def borrow_book(book_id):
    if 'user_id' not in session or session['role'] != 'user':
        return redirect(url_for('home'))

    conn = get_db_connection()
    conn.execute('INSERT INTO emprunts (user_id, livre_id) VALUES (?, ?)', (session['user_id'], book_id))
    conn.execute('UPDATE livres SET disponible = 0 WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('user_dashboard'))

# Fonction pour gérer les utilisateurs (administrateur)
@app.route('/manage-users')
def manage_users():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))

    conn = get_db_connection()
    users = conn.execute('SELECT * FROM utilisateurs').fetchall()
    conn.close()
    return render_template('manage_users.html', users=users)

# Fonction pour supprimer un utilisateur (administrateur)
@app.route('/delete-user/<int:user_id>')
def delete_user(user_id):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))

    conn = get_db_connection()
    conn.execute('DELETE FROM utilisateurs WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('manage_users'))

if __name__ == '__main__':
    app.run(debug=True)
