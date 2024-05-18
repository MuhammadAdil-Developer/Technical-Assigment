# Django Project with User Authentication, Project, and Task Management

This project is a Django application that provides user authentication (signup and login), and allows users to manage projects and tasks. It includes APIs for creating, retrieving, updating, and deleting projects and tasks.and add users to projects

## Table of Contents

- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [APIs](#apis)
  - [User Authentication](#user-authentication)
  - [Project Management](#project-management)
  - [Task Management](#task-management)

Features
User Authentication: Sign-up and login endpoints for user authentication.
Project Management: CRUD operations for managing user projects.
Task Management: CRUD operations for managing tasks within projects.
User add to Project:Project Creater can add multiple Users in the projects.
Permission Handling: Ensures that only authorized users can perform certain actions.
Token-Based Authentication: Secure token generation and validation for user sessions.

## Setup Instructions


1. Create a virtual environment and activate it:


2. python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install the dependencies:

3. pip install -r requirements.txt
Apply migrations:

4. python manage.py makemigrations
python manage.py migrate
Create a superuser:

5. python manage.py createsuperuser
Run the development server:

6. python manage.py runserver
Access the admin interface at http://127.0.0.1:8000/admin and log in with your superuser credentials.