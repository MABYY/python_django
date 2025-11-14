# Python Django Project
Overview
This repository contains a Python-based web application built using the Django framework. It demonstrates a full-stack setup with RESTful API endpoints, leveraging modern development practices for scalability and ease of deployment. This application allows users to:

- **Create an account** and securely log in.
- **Save and manage personal recipes** in a PostgreSQL database.
- **Upload pictures** associated with each recipe (e.g., food photos).
- Interact with a **RESTful API** to perform CRUD operations on users and recipes.
  
It includes robust backend services, database integration, and containerization for seamless development and production environments.

## Features

- Django Framework: High-level Python web framework for rapid development.
- RESTful APIs: Built with Django REST Framework for handling HTTP requests.
- PostgreSQL Database: Persistent data storage with relational database support.
- Docker Containerization: Easy setup and deployment using Docker and Docker Compose.
- Swagger Documentation: Interactive API documentation for exploring and testing endpoints.

## Prerequisites
Before running the project, ensure you have the following installed:

- Docker (version 20.10 or later)
- Docker Compose (version 1.29 or later)
- Git (for cloning the repository)

No additional Python or database installations are required, as everything is managed via Docker.

## Getting Started
- Clone the Repository
- Create .env file in the root folder and customize its corresponding env variables
    - DB_NAME: Database name 
    - DB_USER: Database user 
    - DB_PASSWORD: Database password
    - SECRET_KEY: Django secret key (generate a secure one for production).
- Run the following commands: 
  - cd python_django
  - docker-compose up --build

### This will:
- Build the Django application image.
- Start the PostgreSQL database container.
- Run database migrations automatically.
- Launch the Django development server on port 9000.

### Check Container Status: 
- docker-compose ps

### Stop the Services:
- docker-compose down
- docker-compose down -v

## API Documentation
Swagger is implemented for interactive API documentation. 
You can explore and test the available endpoints directly from your local machine.

- http://localhost:9000/api/schema/swagger-ui/


