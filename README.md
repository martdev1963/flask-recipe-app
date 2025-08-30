# flask-recipe-app

MAB Media – Recipe Generator: Technical Documentation

1. Overview

This document provides a detailed technical overview of the "MAB Media – Recipe Generator" Flask application. The application is a simple, single-page web service that allows users to generate and view "fake" recipes based on a user-submitted dish name. All generated recipes are stored in a local SQLite database and displayed on the main page. 2. Key Features

    Recipe Generation: Creates a templated recipe based on the user's input.

    Image Integration: Fetches a placeholder image from loremflickr.com based on the dish name.

    Persistent Storage: Uses an SQLite database to store generated recipes for a historical log.

    Dynamic UI: Displays the form for recipe generation and a list of previously created recipes with their images.

    Single-File Application: The entire application, including the server logic, database handlers, and HTML templates, is contained within a single Python file.

3. Technology Stack

   Python: The core programming language.

   Flask: A lightweight web framework used to handle web requests and routing.

   SQLite: A file-based database engine used for local data persistence.

   Jinja2: The templating engine used by Flask to render dynamic HTML.

   HTML/CSS: Used for the application's user interface and styling.

4. File Structure & Components

The entire application is self-contained in a single app.py file (or a file with a similar name). It is logically divided into several key sections:
4.1. Configuration

This section defines global constants for the application, such as the title (APP_TITLE) and the name of the database file (DATABASE).
4.2. Database Helpers

This section manages the SQLite database connection.

    get_db(): Initializes and returns a database connection. It uses Flask's g object to store the connection, ensuring that only one connection is created per request.

    close_db(exception): A teardown function registered with Flask. It automatically closes the database connection at the end of each request, releasing resources.

    init_db(): Creates the recipes table if it does not already exist. This function is called on the first page load to ensure the database schema is ready.

4.3. Core Logic

This section contains the application's main functional components.

    image_for_query(query: str) -> tuple[str, str]: A utility function that generates a URL for a placeholder image from the loremflickr.com service. It replaces spaces in the query with + to make it URL-safe.

    generate_recipe(dish: str) -> str: A simple function that generates a string of "fake" recipe ingredients and instructions based on the provided dish name.

4.4. HTML Template

The TEMPLATE string is a multi-line string containing all the HTML and CSS for the application's user interface. It combines both the base structure (head, body, styling) and the dynamic content (the form and the recipe history loop) into a single, cohesive template. This allows all template variables ({{ title }}) and control structures ({% for r in recipes %}) to be processed in a single pass by the Jinja2 engine.
4.5. Routes

This is the core of the Flask application, defining how web requests are handled.

    @app.route("/", methods=["GET", "POST"]): This decorator registers the index() function to handle requests to the root URL (/). It is configured to accept both GET and POST methods.

    GET Request: When the page is loaded, the application fetches all recipes from the database in reverse chronological order (ORDER BY id DESC) and passes them to the template for rendering.

    POST Request: When the user submits the form, the application extracts the dish name, generates a recipe and an image URL, inserts a new record into the recipes table, and then redirects back to the main page. This redirect ensures that a page refresh won't resubmit the form.

4.6. Run App

This block of code is a standard Python entry point. The if **name** == "**main**": check ensures that the development server only runs when the script is executed directly. It binds the server to all network interfaces (host="0.0.0.0") and runs in debug mode, which automatically restarts the server when code changes. 5. Database Schema

The SQLite database contains a single table named recipes.

Column

Data Type

Constraints

Description

id

INTEGER

PRIMARY KEY, AUTOINCREMENT

A unique ID for each recipe entry.

query

TEXT

NOT NULL

The user's original search query (the dish name).

recipe

TEXT

NOT NULL

The full generated recipe text.

image_url

TEXT

NOT NULL

The URL for the placeholder image.

created_at

TEXT

NOT NULL

The timestamp when the recipe was created. 6. How to Run the Application

    Prerequisites: Ensure you have Python and Flask installed. If not, install Flask using pip install Flask.

    Save the file: Save the code as app.py.

    Run from the command line: Navigate to the directory where you saved app.py in your terminal and execute:

    python app.py

    Access the app: Open your web browser and navigate to http://127.0.0.1:5000.

The application will automatically create the recipes.db file and the recipes table upon the first run. 7. Potential Improvements

    Real AI Integration: Replace the generate_recipe() function with a call to a real large language model (LLM) API to generate more creative and varied recipes.

    User Authentication: Implement user login and registration to allow users to save their own private recipe history.

    More Robust UI: Use a CSS framework like Tailwind CSS or Bootstrap for a more polished, responsive design instead of inline styles.

    Error Handling: Add more robust error handling for form submissions and database operations.

    Pagination: Implement pagination for the recipe history list to improve performance if the number of stored recipes grows large.
