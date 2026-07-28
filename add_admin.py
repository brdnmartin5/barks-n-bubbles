import sqlite3

connection = sqlite3.connect("barksnbubbles.db")

connection.execute("""
INSERT INTO administrator
(adminFName, adminLName, adminEmail)
VALUES (?, ?, ?)
""",
("System", "Administrator", "admin@barksnbubbles.com"))

connection.commit()
connection.close()

print("Administrator added successfully!")