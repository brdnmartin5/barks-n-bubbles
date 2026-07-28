import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def get_db_connection():
    connection = sqlite3.connect("barksnbubbles.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/customers")
def customers():
    connection = get_db_connection()

    customers = connection.execute(
        "SELECT * FROM customer ORDER BY customerLName, customerFName"
    ).fetchall()

    connection.close()

    return render_template("customers.html", customers=customers)


@app.route("/customers/add", methods=["GET", "POST"])
def add_customer():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]
        alternate_contact = request.form["alternate_contact"]

        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO customer (
                customerFName,
                customerLName,
                customerEmail,
                customerPhone,
                customerAddress,
                customerAlt
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                first_name,
                last_name,
                email,
                phone,
                address,
                alternate_contact
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("customers"))

    return render_template("add_customer.html")
@app.route("/customers/edit/<int:customer_id>", methods=["GET", "POST"])
def edit_customer(customer_id):
    connection = get_db_connection()

    customer = connection.execute(
        "SELECT * FROM customer WHERE customerID = ?",
        (customer_id,)
    ).fetchone()

    if customer is None:
        connection.close()
        return "Customer not found.", 404

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]
        alternate_contact = request.form["alternate_contact"]

        connection.execute(
            """
            UPDATE customer
            SET customerFName = ?,
                customerLName = ?,
                customerEmail = ?,
                customerPhone = ?,
                customerAddress = ?,
                customerAlt = ?
            WHERE customerID = ?
            """,
            (
                first_name,
                last_name,
                email,
                phone,
                address,
                alternate_contact,
                customer_id
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("customers"))

    connection.close()

    return render_template("edit_customer.html", customer=customer)


@app.route("/customers/delete/<int:customer_id>", methods=["POST"])
def delete_customer(customer_id):
    connection = get_db_connection()

    connection.execute(
        "DELETE FROM customer WHERE customerID = ?",
        (customer_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("customers"))
@app.route("/pets")
def pets():
    connection = get_db_connection()

    pets = connection.execute(
        """
        SELECT
            pet.petID,
            pet.petName,
            pet.breed,
            pet.size,
            customer.customerFName,
            customer.customerLName
        FROM pet
        JOIN customer
            ON pet.customerID = customer.customerID
        ORDER BY pet.petName
        """
    ).fetchall()

    connection.close()

    return render_template("pets.html", pets=pets)
@app.route("/pets/add", methods=["GET", "POST"])
def add_pet():
    connection = get_db_connection()

    customers = connection.execute(
        """
        SELECT customerID, customerFName, customerLName
        FROM customer
        ORDER BY customerLName, customerFName
        """
    ).fetchall()

    if request.method == "POST":
        pet_name = request.form["pet_name"]
        breed = request.form["breed"]
        size = request.form["size"]
        customer_id = request.form["customer_id"]

        connection.execute(
            """
            INSERT INTO pet (
                petName,
                breed,
                size,
                customerID
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                pet_name,
                breed,
                size,
                customer_id
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("pets"))

    connection.close()

    return render_template("add_pet.html", customers=customers)
@app.route("/pets/edit/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    connection = get_db_connection()

    pet = connection.execute(
        "SELECT * FROM pet WHERE petID = ?",
        (pet_id,)
    ).fetchone()

    customers = connection.execute(
        """
        SELECT customerID, customerFName, customerLName
        FROM customer
        ORDER BY customerLName, customerFName
        """
    ).fetchall()

    if request.method == "POST":
        pet_name = request.form["pet_name"]
        breed = request.form["breed"]
        size = request.form["size"]
        customer_id = request.form["customer_id"]

        connection.execute(
            """
            UPDATE pet
            SET petName = ?,
                breed = ?,
                size = ?,
                customerID = ?
            WHERE petID = ?
            """,
            (
                pet_name,
                breed,
                size,
                customer_id,
                pet_id
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("pets"))

    connection.close()

    return render_template(
        "edit_pet.html",
        pet=pet,
        customers=customers
    )
@app.route("/pets/delete/<int:pet_id>", methods=["POST"])
def delete_pet(pet_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM pet WHERE petID = ?",
        (pet_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("pets"))
@app.route("/groomers")
def groomers():
    connection = get_db_connection()

    groomers = connection.execute(
        """
        SELECT *
        FROM groomer
        ORDER BY groomerLName, groomerFName
        """
    ).fetchall()

    connection.close()

    return render_template(
        "groomers.html",
        groomers=groomers
    )
@app.route("/groomers/add", methods=["GET", "POST"])
def add_groomer():

    connection = get_db_connection()

    if request.method == "POST":

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        cell = request.form["cell"]
        specialty = request.form["specialty"]

        connection.execute(
            """
            INSERT INTO groomer
            (
                groomerFName,
                groomerLName,
                groomerCell,
                groomerSpecialty
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                first_name,
                last_name,
                cell,
                specialty
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("groomers"))

    connection.close()

    return render_template("add_groomer.html")
@app.route("/groomers/edit/<int:groomer_id>", methods=["GET", "POST"])
def edit_groomer(groomer_id):
    connection = get_db_connection()

    groomer = connection.execute(
        "SELECT * FROM groomer WHERE groomerID = ?",
        (groomer_id,)
    ).fetchone()

    if groomer is None:
        connection.close()
        return "Groomer not found.", 404

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        cell = request.form["cell"]
        specialty = request.form["specialty"]

        connection.execute(
            """
            UPDATE groomer
            SET groomerFName = ?,
                groomerLName = ?,
                groomerCell = ?,
                groomerSpecialty = ?
            WHERE groomerID = ?
            """,
            (
                first_name,
                last_name,
                cell,
                specialty,
                groomer_id
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("groomers"))

    connection.close()

    return render_template("edit_groomer.html", groomer=groomer)


@app.route("/groomers/delete/<int:groomer_id>", methods=["POST"])
def delete_groomer(groomer_id):
    connection = get_db_connection()

    connection.execute(
        "DELETE FROM groomer WHERE groomerID = ?",
        (groomer_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("groomers"))
@app.route("/services")
def services():
    connection = get_db_connection()

    services = connection.execute(
        """
        SELECT *
        FROM service
        ORDER BY serviceName
        """
    ).fetchall()

    connection.close()

    return render_template(
        "services.html",
        services=services
    )
@app.route("/services/add", methods=["GET", "POST"])
def add_service():
    connection = get_db_connection()

    if request.method == "POST":
        service_name = request.form["service_name"]
        description = request.form["description"]
        price = request.form["price"]
        duration = request.form["duration"]

        connection.execute(
            """
            INSERT INTO service
            (
                serviceName,
                description,
                price,
                duration
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                service_name,
                description,
                price,
                duration
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("services"))

    connection.close()

    return render_template("add_service.html")
@app.route("/services/edit/<int:service_id>", methods=["GET", "POST"])
def edit_service(service_id):
    connection = get_db_connection()

    service = connection.execute(
        "SELECT * FROM service WHERE serviceID = ?",
        (service_id,)
    ).fetchone()

    if service is None:
        connection.close()
        return "Service not found.", 404

    if request.method == "POST":
        service_name = request.form["service_name"]
        description = request.form["description"]
        price = request.form["price"]
        duration = request.form["duration"]

        connection.execute(
            """
            UPDATE service
            SET serviceName = ?,
                description = ?,
                price = ?,
                duration = ?
            WHERE serviceID = ?
            """,
            (
                service_name,
                description,
                price,
                duration,
                service_id
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("services"))

    connection.close()

    return render_template(
        "edit_service.html",
        service=service
    )
@app.route("/services/delete/<int:service_id>", methods=["POST"])
def delete_service(service_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM service WHERE serviceID = ?",
        (service_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("services"))
@app.route("/appointments")
def appointments():
    connection = get_db_connection()

    appointments = connection.execute(
        """
        SELECT
            appointment.apptID,
            appointment.apptDate,
            appointment.apptTime,
            appointment.status,
            pet.petName,
            customer.customerFName,
            customer.customerLName,
            groomer.groomerFName,
            groomer.groomerLName,
            service.serviceName
        FROM appointment
        JOIN pet
            ON appointment.petID = pet.petID
        JOIN customer
            ON pet.customerID = customer.customerID
        JOIN groomer
            ON appointment.groomerID = groomer.groomerID
        JOIN service
            ON appointment.serviceID = service.serviceID
        ORDER BY appointment.apptDate, appointment.apptTime
        """
    ).fetchall()

    connection.close()

    return render_template(
        "appointments.html",
        appointments=appointments
    )
@app.route("/appointments/add", methods=["GET", "POST"])
def add_appointment():
    connection = get_db_connection()

    pets = connection.execute("""
        SELECT petID, petName
        FROM pet
        ORDER BY petName
    """).fetchall()

    groomers = connection.execute("""
        SELECT groomerID, groomerFName, groomerLName
        FROM groomer
        ORDER BY groomerLName
    """).fetchall()

    services = connection.execute("""
        SELECT serviceID, serviceName
        FROM service
        ORDER BY serviceName
    """).fetchall()

    if request.method == "POST":

        appt_date = request.form["appt_date"]
        appt_time = request.form["appt_time"]
        service_id = request.form["service_id"]
        status = request.form["status"]
        pet_id = request.form["pet_id"]
        groomer_id = request.form["groomer_id"]

        admin_id = 1

        connection.execute(
            """
            INSERT INTO appointment
            (
                apptDate,
                apptTime,
                serviceID,
                status,
                petID,
                groomerID,
                adminID
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                appt_date,
                appt_time,
                service_id,
                status,
                pet_id,
                groomer_id,
                admin_id
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("appointments"))

    connection.close()

    return render_template(
        "add_appointment.html",
        pets=pets,
        groomers=groomers,
        services=services
    )
@app.route("/appointments/edit/<int:appt_id>", methods=["GET", "POST"])
def edit_appointment(appt_id):
    connection = get_db_connection()

    appointment = connection.execute(
        "SELECT * FROM appointment WHERE apptID = ?",
        (appt_id,)
    ).fetchone()

    pets = connection.execute(
    "SELECT petID, petName FROM pet ORDER BY petName"
    ).fetchall() 
    groomers = connection.execute(
        "SELECT groomerID, groomerFName, groomerLName FROM groomer ORDER BY groomerLName"
    ).fetchall()

    services = connection.execute(
        "SELECT serviceID, serviceName FROM service ORDER BY serviceName"
    ).fetchall()

    if request.method == "POST":

        connection.execute(
            """
            UPDATE appointment
            SET apptDate = ?,
                apptTime = ?,
                serviceID = ?,
                status = ?,
                petID = ?,
                groomerID = ?
            WHERE apptID = ?
            """,
            (
                request.form["appt_date"],
                request.form["appt_time"],
                request.form["service_id"],
                request.form["status"],
                request.form["pet_id"],
                request.form["groomer_id"],
                appt_id
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("appointments"))

    connection.close()

    return render_template(
        "edit_appointment.html",
        appointment=appointment,
        pets=pets,
        groomers=groomers,
        services=services
    )
@app.route("/appointments/delete/<int:appt_id>", methods=["POST"])
def delete_appointment(appt_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM appointment WHERE apptID = ?",
        (appt_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("appointments"))


# ADD THE REPORTS ROUTE HERE
@app.route("/reports")
def reports():
    connection = get_db_connection()

    total_customers = connection.execute(
        "SELECT COUNT(*) AS total FROM customer"
    ).fetchone()["total"]

    total_pets = connection.execute(
        "SELECT COUNT(*) AS total FROM pet"
    ).fetchone()["total"]

    total_groomers = connection.execute(
        "SELECT COUNT(*) AS total FROM groomer"
    ).fetchone()["total"]

    total_services = connection.execute(
        "SELECT COUNT(*) AS total FROM service"
    ).fetchone()["total"]

    total_appointments = connection.execute(
        "SELECT COUNT(*) AS total FROM appointment"
    ).fetchone()["total"]

    appointments_by_status = connection.execute(
        """
        SELECT status, COUNT(*) AS total
        FROM appointment
        GROUP BY status
        """
    ).fetchall()

    connection.close()

    return render_template(
        "reports.html",
        total_customers=total_customers,
        total_pets=total_pets,
        total_groomers=total_groomers,
        total_services=total_services,
        total_appointments=total_appointments,
        appointments_by_status=appointments_by_status
    )


if __name__ == "__main__":
    app.run(debug=True)
