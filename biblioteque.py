import sqlite3

connection = sqlite3.connect('bibliotheque.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Ajout d'utilisateurs (Admin et Utilisateurs normaux)
cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('admin', 'admin123', 'admin'))
cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('user1', 'password1', 'user'))
cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('user2', 'password2', 'user'))

# Ajout de livres disponibles
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ('Orgueil et préjugés', 'Jane Austen', 1))
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ('Les Hauts de Hurle-Vent', 'Emily Brontë', 1))
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ('1984', 'George Orwell', 1))
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ('L'Étranger', 'Albert Camus', 1))
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ('L'Odyssée', 'Homère', 1))

# Ajout d'emprunts fictifs
cur.execute("INSERT INTO emprunts (user_id, livre_id) VALUES (?, ?)", (2, 1))
cur.execute("INSERT INTO emprunts (user_id, livre_id) VALUES (?, ?)", (3, 3))

connection.commit()
connection.close()
