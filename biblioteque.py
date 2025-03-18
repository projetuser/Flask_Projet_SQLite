import sqlite3

# Connexion à la base de données
connection = sqlite3.connect('bibliotheque.db')

# Création du schéma de la base de données
with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Ajouter des utilisateurs avec des mots de passe en texte clair
cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('admin', 'adminpass', 'admin'))
cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('user1', 'userpass', 'user'))

# Ajouter des livres
cur.execute("INSERT INTO livres (titre, auteur, nombre_exemplaires) VALUES (?, ?, ?)", ('Orgueil et Préjugés', 'Jane Austen', 1))
cur.execute("INSERT INTO livres (titre, auteur, nombre_exemplaires) VALUES (?, ?, ?)", ('Les Hauts de Hurle-Vent', 'Emily Brontë', 1))
cur.execute("INSERT INTO livres (titre, auteur, nombre_exemplaires) VALUES (?, ?, ?)", ('1984', 'George Orwell', 1))
cur.execute("INSERT INTO livres (titre, auteur, nombre_exemplaires) VALUES (?, ?, ?)", ("L'Étranger", 'Albert Camus', 1))
cur.execute("INSERT INTO livres (titre, auteur, nombre_exemplaires) VALUES (?, ?, ?)", ("L'Odyssée", 'Homère', 1))
cur.execute("INSERT INTO livres (titre, auteur, nombre_exemplaires) VALUES (?, ?, ?)", ("Le Petit Prince", 'Antoine de Saint-Exupéry', 1))
cur.execute("INSERT INTO livres (titre, auteur, nombre_exemplaires) VALUES (?, ?, ?)", ("Harry Potter à l'école des sorciers", 'J.K. Rowling', 1))
cur.execute("INSERT INTO livres (titre, auteur, nombre_exemplaires) VALUES (?, ?, ?)", ("Les Misérables", 'Victor Hugo', 1))

# Commit des changements
connection.commit()
connection.close()
