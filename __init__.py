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

if __name__ == '__main__':
    app.run(debug=True)
