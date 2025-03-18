import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO clients (nom, prenom, titre) VALUES (?, ?, ?)",('DUPONT', 'Emilie', 'Orgueil et préjugés'))
cur.execute("INSERT INTO clients (nom, prenom, titre) VALUES (?, ?, ?)",('LEROUX', 'Lucas', 'Les Hauts de Hurle-Vent'))
cur.execute("INSERT INTO clients (nom, prenom, titre) VALUES (?, ?, ?)",('MARTIN', 'Amandine', '1984'))
cur.execute("INSERT INTO clients (nom, prenom, titre) VALUES (?, ?, ?)",('TREMBLAY', 'Antoine', 'L'Étranger'))
cur.execute("INSERT INTO clients (nom, prenom, titre) VALUES (?, ?, ?)",('LAMBERT', 'Sarah', 'L'Odyssée'))

connection.commit()
connection.close()
