from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'votre_clé_secrète'  # Utilisez une clé secrète pour sécuriser les sessions

# Fonction de connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('bibliotheque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route pour la page d'accueil
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM utilisateurs WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']

            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            return render_template('index.html', error="Nom d'utilisateur ou mot de passe incorrect")

    return render_template('index.html')

# Route pour le tableau de bord de l'administrateur
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))  # Rediriger vers la page d'accueil si non admin
    return render_template('admin_dashboard.html', username=session['username'])

# Route pour le tableau de bord de l'utilisateur
@app.route('/user_dashboard')
def user_dashboard():
    if 'username' not in session or session['role'] != 'user':
        return redirect(url_for('index'))  # Rediriger vers la page d'accueil si non user
    return render_template('user_dashboard.html', username=session['username'])

# Route pour l'inscription d'un utilisateur
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'user'  # Par défaut, les nouveaux utilisateurs sont des utilisateurs

        conn = get_db_connection()
        conn.execute('INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)', (username, password, role))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))  # Rediriger vers la page d'accueil après inscription

    return render_template('register.html')

# Route pour se déconnecter
@app.route('/logout')
def logout():
    session.clear()  # Vider la session
    return redirect(url_for('index'))  # Rediriger vers la page d'accueil

if __name__ == '__main__':
    app.run(debug=True)
