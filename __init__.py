from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'  # Pour gérer les sessions de manière sécurisée

# Connexion à la base de données SQLite
def get_db_connection():
    conn = sqlite3.connect('bibliotheque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route pour l'authentification des utilisateurs
@app.route('/authentification', methods=['GET', 'POST'])
@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connexion à la base de données
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM utilisateurs WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        # Déboguer l'utilisateur récupéré
        print(f"Utilisateur récupéré: {user}")

        # Si l'utilisateur existe
        if user:
            # Création de la session
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            # Si les identifiants sont incorrects, afficher un message d'erreur
            print("Identifiants incorrects")
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html')


# Route pour le tableau de bord
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('authentification'))
    return render_template('dashboard.html', role=session['role'])

# Route pour afficher les livres
@app.route('/livres')
def livres():
    conn = get_db_connection()
    livres = conn.execute('SELECT * FROM livres').fetchall()  # Récupère tous les livres
    conn.close()
    return render_template('read_data.html', livres=livres)

# Route pour ajouter un livre (administrateur)
@app.route('/ajouter_livre', methods=['GET', 'POST'])
def ajouter_livre():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        conn = get_db_connection()
        conn.execute('INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)', (titre, auteur, 1))
        conn.commit()
        conn.close()
        return redirect(url_for('livres'))
    return render_template('ajouter_livre.html')

# Route pour emprunter un livre
@app.route('/emprunter_livre/<int:id>')
def emprunter_livre(id):
    if 'user_id' not in session:
        return redirect(url_for('authentification'))
    conn = get_db_connection()
    livre = conn.execute('SELECT * FROM livres WHERE id = ?', (id,)).fetchone()
    if livre and livre['disponible'] > 0:
        conn.execute('INSERT INTO emprunts (user_id, livre_id) VALUES (?, ?)', (session['user_id'], id))
        conn.execute('UPDATE livres SET disponible = disponible - 1 WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('livres'))
    conn.close()
    return render_template('livre_non_disponible.html')

# Route pour retourner un livre
@app.route('/retourner_livre/<int:id>')
def retourner_livre(id):
    if 'user_id' not in session:
        return redirect(url_for('authentification'))
    conn = get_db_connection()
    conn.execute('DELETE FROM emprunts WHERE user_id = ? AND livre_id = ?', (session['user_id'], id))
    conn.execute('UPDATE livres SET disponible = disponible + 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('livres'))

# Route pour afficher les utilisateurs (administrateur uniquement)
@app.route('/utilisateurs')
def utilisateurs():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('dashboard'))
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM utilisateurs').fetchall()
    conn.close()
    return render_template('utilisateurs.html', utilisateurs=users)

# Route pour se déconnecter
@app.route('/deconnexion')
def deconnexion():
    session.clear()
    return redirect(url_for('authentification'))

if __name__ == '__main__':
    app.run(debug=True)
