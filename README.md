# Task Manager Web Application

## Overview

A full-stack task management application built with Django (backend) and React (frontend), allowing users to create, organize, and track their tasks efficiently.

## ✨ Features

- User authentication and authorization
- Task creation, update, and deletion
- Real-time updates using Django REST framework

## 🛠️ Tech Stack

### Backend

- Python 3.8+
- Django
- Django REST Framework
- Simple JWT (JWT Authentication)
- Django Extensions
- DRF Spectacular (for API documentation)
- Corsheaders (for CORS handling)
- SQLite3 (default database)

### Frontend

- Node.js 14+
- React
- React Router
- State Management (Redux or Context API)
- Axios (for API calls)
- Tailwind CSS (for styling)
- React Icons (for icons)
- Webpack (for bundling and building)

## 🔧 Installation

1. Install Python 3.8+ and pip (Python package manager)
2. Install Django and required packages using pip:

    ```bash
    pip install django djangorestframework django-extensions drf-spectacular corsheaders
    ```

3. Install Node.js 14+ and npm (or yarn)
4. Install React and required packages using npm (or yarn):

     ```bash
     npm install react react-router-dom react-icons axios tailwindcss webpack
     
     ```

5. Install PostgreSQL (or another database of your choice) and configure it according to your needs
6. Clone the repository and navigate to the project directory
7. Run `npm install` (or `yarn install`) to install dependencies
8. Run `python manage.py migrate` to create the database schema
9. Run `python manage.py runserver` to start the backend development server
10. Run `npm start` (or `yarn start`) to start the frontend development server

Note: These installation steps are general and may vary depending on your specific environment and requirements.

## 🏗️ Project Structure

```
Task-Master
├── backend
│   ├── db.sqlite3
│   ├── manage.py
│   ├── schema.yaml
│   ├── task_master
│   ├── tasks
│   └── User
├── frontend
│   ├── node_modules
│   ├── package.json
│   ├── package-lock.json
│   ├── public
│   ├── src
│   └── tailwind.config.js
└── README.md
```

## 📚 API Documentation

The following APIs are used in the backend:

### Authentication APIs

- `POST /api/auth/login/`: Login user
- `POST /api/auth/register/`: Register new user
- `POST /api/auth/logout/`: Logout user
- `POST /api/auth/token/refresh/`: Refresh token

### User APIs

- `GET /api/auth/profile/`: Retrieve user profile
- `PUT /api/auth/profile/`: Update user profile

### Task APIs

- `GET /api/tasks/`: List all tasks
- `POST /api/tasks/`: Create new task
- `GET /api/tasks/{id}/`: Retrieve task
- `PUT /api/tasks/{id}/`: Update task
- `DELETE /api/tasks/{id}/`: Delete task

### Project APIs

- `GET /api/projects/`: List all projects
- `POST /api/projects/`: Create new project
- `GET /api/projects/{id}/`: Retrieve project
- `PUT /api/projects/{id}/`: Update project
- `DELETE /api/projects/{id}/`: Delete project

### Comment APIs

- `GET /api/comments/`: List all comments
- `POST /api/comments/`: Create new comment
- `GET /api/comments/{id}/`: Retrieve comment
- `PUT /api/comments/{id}/`: Update comment
- `DELETE /api/comments/{id}/`: Delete comment

### API Documentation

- `GET /schema/`: API schema
- `GET /swagger/`: API Swagger documentation

## 🧪 Running Tests

### Backend Tests

```bash
python manage.py test
```

## 👤 Authors

- Omar Alghareeb
- Ibrahim Mohamed
- Nawal Khaled
