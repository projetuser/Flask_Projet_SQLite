import sqlite3

# Connexion à la base de données SQLite
connection = sqlite3.connect('bibliotheque.py')  # Utilise un fichier Python pour la base de données

# Exécution du script de création de la base de données (si ce n'est pas déjà fait)
with open('schema.sql') as f:
    connection.executescript(f.read())

# Création d'un curseur pour exécuter les requêtes
cur = connection.cursor()

# Ajout des utilisateurs (admin et user)
cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('admin', 'adminpass', 'admin'))
cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('user1', 'userpass', 'user'))

# Ajout des livres à la bibliothèque
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ('Orgueil et Préjugés', 'Jane Austen', 1))
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ('Les Hauts de Hurle-Vent', 'Emily Brontë', 1))
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ('1984', 'George Orwell', 1))
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ("L'Étranger", 'Albert Camus', 1))
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ("L'Odyssée", 'Homère', 1))
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ("Le Petit Prince", 'Antoine de Saint-Exupéry', 1))
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ("Harry Potter à l'école des sorciers", 'J.K. Rowling', 1))
cur.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ("Les Misérables", 'Victor Hugo', 1))

# Validation des changements dans la base de données
connection.commit()

# Fermeture de la connexion à la base de données
connection.close()
