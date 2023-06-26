# SCISSOR: Shorten. Simplify. Share.



## Description
Scissor is a URL shortener application which takes a long URL as input and provides a shortened version of the URL. The application is built using Flask, a Python web framework, and uses SQLAlchemy for the ORM (Object-Relational Mapping) layer and SQLite as the database. The application also uses Flask-Migrate for handling database schema migrations, which makes it easier to adapt the database schema as the application evolves over time.



## Main Components
Here are the main components of the Scissor App:

**Flask**: A micro web framework written in Python that is easy to use and provides the flexibility to use extensions like Flask-SQLAlchemy and Flask-Login.

**Flask-SQLAlchemy**: A Flask extension that simplifies the use of SQLAlchemy, which is an Object Relational Mapper (ORM) that allows interaction with the database in an object-oriented way.

**Flask-Login**: A Flask extension that provides user session management. It handles the common tasks of logging in, logging out, and remembering users’ sessions over extended periods.

**Flask-Limiter**: Used to limit the rate of requests that clients can make to the app. The limiting is achieved through setting various decorators on the routes.

**Flask-Caching**: This is a Flask extension that adds caching support to your Flask application. It has support for various caching backends and it is compatible with Flask-Limiter.

**Flask-Migrate**: Handles SQLAlchemy database migrations for Flask applications using Alembic.



## How Scissor Works
After a user signs up or logs in, they can enter any long URL into the provided form. The Scissor App will first check that the URL is valid, and then create a short URL (or a custom URL) that redirects to the original URL. All the short URLs and custom URLs are associated with the user who created them.
Each shortened (or custom-shortened) URL is unique. When the URL is visited, the application increments a click count, tracking how many times the link has been used. Also, users can generate a QR code for their short URL or custom URL.



## App Structure
### Here is the structure of the Scissor app:

**__init__.py**: This is where the Flask app is created and configured. The SQLAlchemy database, Flask login manager, and Flask limiter are also initialized here.

**auth.py**: This module contains routes for user authentication (signup, login, logout).

**config.py**: This module contains configuration settings for the app. Sensitive information is fetched from environment variables for security.

**models.py**: This module contains the SQLAlchemy ORM models (User, Url, CustomUrl).

**views.py**: This module contains the main routes of the application. This includes routes for displaying the home page, handling URL shortening, URL redirection, and QR code generation.

The app relies on environment variables for some sensitive information. Make sure you have the following variables set in your environment:

**SECRET_KEY**: A secret key for your application, used for session signing.

**DATABASE_URI**: The database URI that should be used for the connection.

**SERVER_NAME**: The name and port number of the server.

**REDIS_URL**: The URL to connect to the Redis server.

### Here are the endpoints used in the Scissor app:

**/ or /home**: The home page of the application. Displays all shortened URLs for the currently logged-in user.

**/login**: Log in to the application. Limited to 10 attempts per minute.

**/signup**: Sign up for a new account. Limited to 10 attempts per minute.

**/logout**: Log out of the application.

**/shortenurl**: Generate a shortened URL. Requires login.

**/customurl**: Generate a custom shortened URL. Requires login.

**/<url_key>**: Redirect to the original URL corresponding to the provided url_key.

**/generate_qr/<url_key>**: Generate a QR code for the provided url_key. Requires login.

***Database Migrations***:
The application uses Flask-Migrate, which is a Flask extension that handles SQLAlchemy database migrations. This is especially useful as it provides a command-line interface for performing migrations, including creating migration scripts automatically.
The migration scripts are stored in a migrations folder in the root of the project. They provide a version history of the database schema, which can be navigated using the Flask-Migrate commands.

***User Authentication***:
The application includes user authentication. Users can sign up for a new account, log in to an existing account, and log out. The application uses hashed passwords for security. This is handled by the werkzeug.security module.

***Rate Limiting***:
The application uses rate limiting to protect against abuse. This is handled by Flask-Limiter. The login, signup, URL shortening, and URL redirection endpoints are all limited to 10 requests per minute.

***Caching***:
The application uses Flask-Caching with a Redis backend for caching. The cache is primarily used to store the results of URL shortening requests, which allows the application to quickly return results for repeat requests without needing to access the database. If the connection to the Redis server is lost, the application will fall back to using a simple memory-based cache.

***Exception Handling***:
The application includes basic exception handling. In the case of a bad request or an internal server error, the application will return an appropriate HTTP status code and a descriptive error message.

***Analytics***:
In addition to shortening URLs, the application also provides some basic analytics for each shortened URL. It tracks the number of times each URL is clicked. This information is displayed next to each URL on the home page.



## Why Scissor?

Streamline Sharing: Say goodbye to clunky URLs that get lost in the crowd. Scissor simplifies your links, making them shareable with a click. Whether it's social media, emails, or your website, Scissor ensures a seamless experience for you and your audience.

Track Performance: Get valuable insights into your link's performance. Scissor's built-in analytics lets you see who's clicking and where they're coming from. Harness the power of data to optimize your strategies and drive results.

Effortless and Intuitive: Scissor is designed with simplicity in mind. Just paste your long URL, hit "Shorten," and watch the magic happen. No technical jargon or complicated setup required.

Versatile Applications: From social media buffs to email marketers and website owners, Scissor fits right into your workflow. It's the ultimate tool for individuals, businesses, and organizations seeking to amplify their online presence.

User-Friendly Experience: Scissor's sleek interface puts you in control. Shorten and customize your URLs with ease, saving time and boosting productivity. We believe in keeping things simple, so you can focus on what matters most.

Unlock the power of concise sharing with Scissor. Make your links impactful, trackable, and effortlessly shareable. Join Scissor today and redefine the way you communicate online. Shorten with Scissor and experience the difference.



## Installation

### Clone the repository to your local environment. In the project's root directory, run the following command to install the necessary dependencies:

*pip install -r requirements.txt*

### Set up the necessary environment variables:

*export SECRET_KEY=<your-secret-key>*

*export DATABASE_URI=<your-database-uri>*

*export SERVER_NAME=<your-server-name>*

*export REDIS_URL=<your-redis-url>*

## Usage

### To run the server, use the following command in the root directory:

*flask run*

### To initialize the migrations for the first time, run:

*flask db init*

This will create the migrations folder and the necessary configuration files inside it.

### To generate a migration script after modifying the database models, use:

*flask db migrate -m "message"*

Where "message" is a brief description of the changes made.

### Finally, to apply the migrations to the database, use:

*flask db upgrade*



## Built with:
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)



<br/>
Live link: <a href="https://scissor-app.onrender.com">SCISSOR</a>
