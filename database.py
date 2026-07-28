import sqlite3


def create_database():
    connection = sqlite3.connect("barksnbubbles.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS administrator (
            adminID INTEGER PRIMARY KEY AUTOINCREMENT,
            adminFName TEXT NOT NULL,
            adminLName TEXT NOT NULL,
            adminEmail TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            customerID INTEGER PRIMARY KEY AUTOINCREMENT,
            customerFName TEXT NOT NULL,
            customerLName TEXT NOT NULL,
            customerEmail TEXT,
            customerPhone TEXT,
            customerAddress TEXT,
            customerAlt TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pet (
            petID INTEGER PRIMARY KEY AUTOINCREMENT,
            petName TEXT NOT NULL,
            breed TEXT,
            size TEXT,
            customerID INTEGER NOT NULL,
            FOREIGN KEY (customerID) REFERENCES customer(customerID)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groomer (
            groomerID INTEGER PRIMARY KEY AUTOINCREMENT,
            groomerFName TEXT NOT NULL,
            groomerLName TEXT NOT NULL,
            groomerCell TEXT,
            groomerSpecialty TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS service (
            serviceID INTEGER PRIMARY KEY AUTOINCREMENT,
            serviceName TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            duration INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointment (
            apptID INTEGER PRIMARY KEY AUTOINCREMENT,
            apptDate TEXT NOT NULL,
            apptTime TEXT NOT NULL,
            serviceID INTEGER NOT NULL,
            status TEXT NOT NULL,
            petID INTEGER NOT NULL,
            groomerID INTEGER NOT NULL,
            adminID INTEGER NOT NULL,
            FOREIGN KEY (serviceID) REFERENCES service(serviceID),
            FOREIGN KEY (petID) REFERENCES pet(petID),
            FOREIGN KEY (groomerID) REFERENCES groomer(groomerID),
            FOREIGN KEY (adminID) REFERENCES administrator(adminID)
        )
    """)

    connection.commit()
    connection.close()

    print("Database and tables created successfully.")


if __name__ == "__main__":
    create_database()