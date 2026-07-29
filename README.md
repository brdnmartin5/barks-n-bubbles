# Barks N Bubbles

## Overview

Barks N Bubbles is a pet grooming appointment system developed as a senior Information Systems capstone project. The application allows users to manage customers, pets, groomers, services, and appointments through a very simple web interface.

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- Bootstrap

## Features

- Customer management (create, read, update, delete)
- Pet management (create, read, update, delete)
- Groomer management (create, read, update, delete)
- Service management (create, read, update, delete)
- Appointment scheduling
- Reports page displaying summary information from the database

## Project Structure

### app.py

This is where most of the project is. It runs the Flask application and contains all of the routes for the website.

We decided to keep everything in one file because it made it easier to work on as a group and easier to follow while we were learning Flask. Since our project isn't very large, splitting everything into multiple files didn't really seem necessary.

Each section has the same basic CRUD operations:

- View
- Add
- Edit
- Delete

The routes also connect to the SQLite database to get, update, or delete information.

### templates

The templates folder contains all of the HTML pages that users actually see.

**base.html**

This is the main layout for the website. Every page extends this file so we only had to build things like the navigation bar and Bootstrap setup once.

**home.html**

This is the dashboard. It's the first page users see and lets them navigate to each section of the system.

**customers.html**

Displays all customers that are currently in the database.

**add_customer.html**

Allows the user to add a new customer.

**edit_customer.html**

Allows the user to update customer information.

The same idea is used for Pets, Groomers, Services, and Appointments.

### Reports

The reports page gives a quick summary of what's in the database. We used simple SQL queries like 'COUNT()' to show total for customers, pets, groomers, services, and appointments. We also used 'GROUP BY' to show how many appointments are scheduled, completed, or cancelled.

### Database

The project uses SQLite. We chose SQLite because it was simple to set it up, works well with Flask, and was more than enough for a project this size.

The database stores:

- Customers
- Pets
- Groomers
- Services
- Appointments
- Administrators

## Why we built it this way

We wanted to keep the project simple and focus on the business requirements instead of making it overly complicated. Flask made it easy to connect Python, HTML, and the database together. Bootstrap helped us build a clean interface without spending a lot of time on CSS. Some of the code is repetitive because every section follows the same CRUD pattern. We actually kept it that way because it made the project easier to understand, debug, and maintain while we were building it.


## Authors
- Brandon Martin
- Heesoo Kim
