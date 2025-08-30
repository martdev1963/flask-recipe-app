Recipe Generator Application Documentation

This documentation provides a comprehensive guide to the Recipe Generator, a web application that leverages a Python backend and a JavaScript frontend to create, store, and manage recipes.

Application Overview

The application is built on a simple client-server architecture.

    The backend, a Flask web server, is responsible for handling all core logic, including API requests, communication with the Gemini API to generate recipes, and database operations with Firebase Firestore.

    The frontend, a single HTML file, provides the user interface. It uses JavaScript to interact with the backend API to generate, display, and delete recipes.

Prerequisites

To run this application, you will need to install the following software and configure a Google Cloud project.

    Python 3.x: Ensure you have a recent version of Python installed.

    Pip: Python's package installer, which is typically included with Python.

    Google Cloud Project: A project with Firebase enabled, and the Cloud Firestore API activated. You must have a service account JSON file from this project.

Project Structure

The application should be organized in a specific directory structure for Flask to function correctly.

.
├── app.py
└── templates
└── index.html

    app.py: This is the main Python file containing the Flask web server and backend logic.

    templates/: This is a required directory where Flask automatically looks for HTML files.

    index.html: The single-file frontend for the application.

Backend (app.py) Documentation

The app.py file is the heart of the application, managing all server-side operations.

Python Dependencies

First, you must install all the required Python libraries. Open your terminal and run the following command:
Bash

pip install Flask Flask-Cors requests firebase-admin

Key Code Sections

    Configuration: The firebase_config dictionary on lines 17-27 is crucial for authentication. It contains placeholder values that must be replaced with the credentials from your service account JSON file. The private_key is particularly important, as it contains escaped newlines that the code automatically handles.

    Gemini API Integration: The generate_recipe function on line 87 makes a POST request to the Gemini API. It uses the requests library to send the user's prompt and a JSON schema, ensuring the generated recipe is in a structured format.

    API Endpoints: The app exposes the following RESTful API endpoints:

        GET /: Serves the index.html file to the user's browser.

        POST /recipes: Accepts a JSON payload with a prompt and user_id. It calls the Gemini API to generate a new recipe, saves it to Firestore, and returns the newly created recipe as a JSON object.

        GET /recipes: Accepts a user_id as a query parameter. It retrieves all recipes for that user from Firestore and returns them as a JSON array.

        DELETE /recipes/<recipe_id>: Accepts a recipe_id in the URL and a user_id as a query parameter. It deletes the corresponding recipe document from Firestore.

    Firestore Integration: The app connects to your Firebase project using the firebase-admin SDK. The recipe data is stored in a collection path that is dynamically built using the app_id and user_id: /artifacts/{app_id}/users/{user_id}/recipes. This structure ensures the data is private to each user and adheres to Firebase's security best practices.

Frontend (index.html) Documentation

The index.html file provides the entire user interface and client-side logic in a single file for convenience.

Structure and Styling

The HTML file is structured to be fully responsive using Tailwind CSS.

    A main container holds the application's header, form, and recipe display area.

    The #recipe-form element captures user input for generating new recipes.

    The #recipes-container is a grid where the JavaScript dynamically injects recipe cards.

    The styling is handled entirely by Tailwind's utility classes and a small, custom style block for the card shadow and font.

JavaScript Logic

The JavaScript section handles all client-side interactions.

    fetchRecipes(): This function is called when the page loads. It sends a GET request to the backend to retrieve any previously saved recipes for the user_001 placeholder ID and renders them on the page.

    renderRecipe(): This utility function takes a recipe JSON object and creates a new HTML card element for it. This keeps the recipe display area up to date.

    Form Submission: When the user submits the form, the event listener prevents the default page reload, updates the UI to show a "Generating..." message, and sends the user's prompt to the backend's POST /recipes endpoint.

    deleteRecipe(): This function is attached to the delete button on each recipe card. It sends a DELETE request to the backend with the recipe's ID, which removes the recipe from Firestore and the user interface.

    Error Handling: Both the fetchRecipes() and form submission handlers include try...catch blocks to capture and display errors from the backend in the #status-message area.

How to Run the Application

With all the components and dependencies in place, you can now run the application.

    Open your terminal and navigate to the directory containing your app.py and templates folder.

    Run the Flask server with the following command:

Bash

python app.py

    The console will show that the server is running on http://127.0.0.1:5000. Open this URL in your web browser to access the Recipe Generator application.
