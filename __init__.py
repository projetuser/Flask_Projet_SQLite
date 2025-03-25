from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

# Utiliser une clé secrète pour sécuriser les sessions
app.secret_key = 'votre_clé_secrète'  # Remplacez cette clé par une clé secrète complexe et aléatoire

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

        # Connexion à la base de données et vérification des identifiants
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM utilisateurs WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            # Stocker les informations de l'utilisateur dans la session
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']

            # Redirection en fonction du rôle
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            # Si l'utilisateur ou mot de passe est incorrect, afficher une erreur
            return render_template('index.html', error="Nom d'utilisateur ou mot de passe incorrect")

    return render_template('index.html')

# Route pour le tableau de bord de l'administrateur
@app.route('/admin_dashboard')
def admin_dashboard():
    # Vérifier si l'utilisateur est connecté et est un admin
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))  # Si ce n'est pas un admin, rediriger vers la page d'accueil
    return render_template('admin_dashboard.html', username=session['username'])

# Route pour le tableau de bord de l'utilisateur
@app.route('/user_dashboard')
def user_dashboard():
    # Vérifier si l'utilisateur est connecté et est un utilisateur
    if 'username' not in session or session['role'] != 'user':
        return redirect(url_for('index'))  # Si ce n'est pas un utilisateur, rediriger vers la page d'accueil
    return render_template('user_dashboard.html', username=session['username'])

# Route pour l'inscription d'un utilisateur
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'user'  # Par défaut, les nouveaux utilisateurs sont des utilisateurs

        # Connexion à la base de données pour ajouter l'utilisateur
        conn = get_db_connection()
        conn.execute('INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)', (username, password, role))
        conn.commit()
        conn.close()

        # Rediriger vers la page de connexion après inscription
        return redirect(url_for('index'))  # Rediriger vers la page d'accueil après inscription

    return render_template('register.html')

# Route pour se déconnecter
@app.route('/logout')
def logout():
    session.clear()  # Vider la session
    return redirect(url_for('index'))  # Rediriger vers la page d'accueil après déconnexion

if __name__ == '__main__':
    app.run(debug=True)
