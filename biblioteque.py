import sqlite3

connection = sqlite3.connect('bibliotheque.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('admin', 'adminpass', 'admin'))
cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('user1', 'userpass', 'user'))

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
