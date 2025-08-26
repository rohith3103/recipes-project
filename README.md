# recipes-project

This is a full-stack recipe application built for the NxtWave AI/ML role assessment. It features a Python (Flask) backend and a React.js frontend.

## Features

- Parse and store recipe data from a JSON file in a database.
- RESTful API with endpoints for pagination, sorting, and advanced searching.
- A user-friendly frontend to display, filter, and view details of recipes.

## Tech Stack

- **Backend:** Python, Flask, SQLite
- **Frontend:** React.js, HTML, CSS, JavaScript

## How to Run the Application

### 1. Backend Setup

1.  Navigate to the `backend` directory:
    `cd backend`
2.  Install dependencies:
    `pip install -r requirements.txt`
3.  Populate the database:
    `python recipes_database.py`
4.  Start the server:
    `flask run`

### 2. Frontend Setup

1.  Open a new terminal and navigate to the `frontend` directory:
    `cd frontend`
2.  Install dependencies:
    `npm install`
3.  Start the React app:
    `npm start`

> The application will be available at `http://localhost:3000`.
