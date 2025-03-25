import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'random_secret_key'  # Clé secrète pour les sessions

# Fonction de connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('bibliotheque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Fonction de vérification de l'utilisateur
def verify_user(username, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM utilisateurs WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):  # Vérification du mot de passe
        return user
    return None

# Route d'accueil pour la connexion
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Vérifier l'utilisateur dans la base de données
        user = verify_user(username, password)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))  # Redirection vers le tableau de bord
        else:
            return render_template('index.html', error="Nom d'utilisateur ou mot de passe incorrect")
    
    return render_template('index.html')

# Route du tableau de bord (admin ou utilisateur)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))  # Si l'utilisateur n'est pas connecté, rediriger vers la page d'accueil
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM utilisateurs WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    
    if user['role'] == 'admin':
        return render_template('admin_dashboard.html', user=user)
    else:
        return render_template('user_dashboard.html', user=user)

# Route pour l'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'user'  # Par défaut, le rôle est 'user'

        # Hachage du mot de passe avant de l'enregistrer
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)",
                         (username, hashed_password, role))
            conn.commit()
            return redirect(url_for('home'))  # Rediriger vers la page d'accueil après l'inscription
        except sqlite3.IntegrityError:
            return render_template('register.html', error="Ce nom d'utilisateur existe déjà.")
        finally:
            conn.close()

    return render_template('register.html')

# Route pour la déconnexion
@app.route('/logout')
def logout():
    session.clear()  # Vider la session
    return redirect(url_for('home'))

# Route pour ajouter un livre (admin uniquement)
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))  # Si l'utilisateur n'est pas admin, rediriger vers la page d'accueil
    
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        
        conn = get_db_connection()
        conn.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)",
                     (titre, auteur, 1))  # Livre disponible par défaut
        conn.commit()
        conn.close()
        
        return redirect(url_for('dashboard'))
    
    return render_template('add_book.html')

# Route pour gérer les livres (admin uniquement)
@app.route('/list_books')
def list_books():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))  # Si l'utilisateur n'est pas admin, rediriger vers la page d'accueil
    
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM livres").fetchall()
    conn.close()
    
    return render_template('list_books.html', books=books)

# Route pour gérer les utilisateurs (admin uniquement)
@app.route('/manage_users')
def manage_users():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))  # Si l'utilisateur n'est pas admin, rediriger vers la page d'accueil
    
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM utilisateurs").fetchall()
    conn.close()
    
    return render_template('manage_users.html', users=users)

# Route pour emprunter un livre (utilisateur uniquement)
@app.route('/borrow_book/<int:book_id>')
def borrow_book(book_id):
    if 'user_id' not in session or session['role'] != 'user':
        return redirect(url_for('home'))  # Si l'utilisateur n'est pas connecté ou n'est pas un utilisateur
    
    conn = get_db_connection()
    conn.execute("INSERT INTO emprunts (user_id, livre_id) VALUES (?, ?)",
                 (session['user_id'], book_id))  # Enregistrer l'emprunt
    conn.commit()
    conn.close()
    
    return redirect(url_for('dashboard'))

# Page d'erreur 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Lancement de l'application
if __name__ == '__main__':
    app.run(debug=True)
