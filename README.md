# SCISSOR: Shorten. Simplify. Share.



The Scissor App is a Flask-based URL shortener web application that shortens long URLs to more convenient and secure "short URLs" and "custom URLs", with user management functionality and rate limiting.



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
Here is the structure of the Scissor app:

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

*Rate Limiting*
Scissor app uses rate limiting to protect the app against DoS attacks and to prevent abuse. The @limit decorator is used to limit certain routes, allowing only a certain number of requests per minute.

*Caching*
Scissor app uses caching to improve performance. It uses Flask-Caching extension with Redis as the backend. It is used together with Flask-Limiter to limit the number of requests. The connection settings for Redis are configured in __init__.py.



## Why Scissor?

Streamline Sharing: Say goodbye to clunky URLs that get lost in the crowd. Scissor simplifies your links, making them shareable with a click. Whether it's social media, emails, or your website, Scissor ensures a seamless experience for you and your audience.

Track Performance: Get valuable insights into your link's performance. Scissor's built-in analytics lets you see who's clicking and where they're coming from. Harness the power of data to optimize your strategies and drive results.

Effortless and Intuitive: Scissor is designed with simplicity in mind. Just paste your long URL, hit "Shorten," and watch the magic happen. No technical jargon or complicated setup required.

Versatile Applications: From social media buffs to email marketers and website owners, Scissor fits right into your workflow. It's the ultimate tool for individuals, businesses, and organizations seeking to amplify their online presence.

User-Friendly Experience: Scissor's sleek interface puts you in control. Shorten and customize your URLs with ease, saving time and boosting productivity. We believe in keeping things simple, so you can focus on what matters most.

Unlock the power of concise sharing with Scissor. Make your links impactful, trackable, and effortlessly shareable. Join Scissor today and redefine the way you communicate online. Shorten with Scissor and experience the difference.

## Built with:
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)



<br/>
Live link: <a href="https://scissor-app.onrender.com">SCISSOR</a>
