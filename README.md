# Cloud Clicker

## Project Overview

Cloud Clicker is a web application designed to track and display click counts. The application supports user authentication, allows users to increment their click count, and displays overall and user-specific click data. The application also includes a dashboard that shows click statistics over time, including total clicks and clicks per minute.

## Sequence Diagram
![Sequence Diagram](/diagrams/sequence_diagram.drawio.png)

## Design Diagram
![Design Diagram](/diagrams/designdiagram.png)

## Table of Contents

- [Cloud Clicker](#cloud-clicker)
  - [Project Overview](#project-overview)
  - [Sequence Diagram](#sequence-diagram)
  - [Design Diagram](#design-diagram)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Deployment](#deployment)
    - [Docker Setup](#docker-setup)
    - [CI/CD with GitHub Actions](#cicd-with-github-actions)
  - [API Endpoints](#api-endpoints)
  - [Frontend Pages](#frontend-pages)
  - [Docker Setup](#docker-setup-1)
  - [CI/CD with GitHub Actions](#cicd-with-github-actions-1)
  - [Logging and Monitoring](#logging-and-monitoring)
  - [Conclusion](#conclusion)

## Project Structure

- **Main**: Contains the main Flask application code and static assets.
  - **application.py**: Main Flask application file.
  - **static**: Directory for static files (CSS, JS).
  - **templates**: Directory for HTML templates.

- **Dockerfile**: Instructions for building the Docker image.
- **Dockerrun.aws.json**: Configuration for deploying the Docker image to AWS Elastic Beanstalk.
- **deploy.yml**: GitHub Actions workflow file for CI/CD.
- **README.md**: Project documentation.

## Features

- **User Authentication**: Provides user registration and login functionality using JWT tokens.
- **Click Tracking**: Users can increment their click count and view total and user-specific clicks.
- **Dashboard**: Displays click statistics over time, including total clicks and clicks per minute.
- **Responsive Design**: User-friendly interface that adapts to different screen sizes.
- **API Endpoints**: RESTful APIs for user registration, login, and click data management.
- **Logging**: Log data at numerous points in the app.
- **Dockerized Deployment**: Deployable via Docker and AWS Elastic Beanstalk.
- **CI/CD Pipeline**: Automated deployment using GitHub Actions.

## Technologies Used

- **Backend**: Python, Flask, SQLite, JWT
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Deployment**: Docker, AWS Elastic Beanstalk
- **CI/CD**: GitHub Actions

## Deployment

### Docker Setup

- **Dockerfile**: Defines the environment and commands to set up and run the application in a Docker container.
- **Dockerrun.aws.json**: Configuration file for deploying the Docker container to AWS Elastic Beanstalk, specifying ports, image details, and volumes.

### CI/CD with GitHub Actions

- **deploy.yml**: GitHub Actions workflow for automated deployment to AWS Elastic Beanstalk. The workflow includes steps for setting up Python, installing dependencies, configuring AWS credentials, and deploying the application.

## API Endpoints

- **POST /api/register**: Register a new user.
- **POST /api/login**: Login and receive a JWT token.
- **POST /api/clicks**: Increment the click count (requires authentication).
- **GET /api/clicks**: Get total and user-specific click counts.
- **GET /api/clicks/log**: Get click data over time and clicks per minute.

## Frontend Pages

- **index.html**: Landing page with options to sign in or sign up, and links to view clicks and the dashboard.
- **clicks.html**: Displays total clicks and user-specific clicks. Allows authenticated users to increment their click count.
- **charts.html**: Dashboard displaying click statistics over time, including total clicks and clicks per minute.

## Docker Setup

- **Dockerfile**: Contains the instructions for building the Docker image, including setting up the Python environment, installing dependencies, and running the application.
- **Dockerrun.aws.json**: Specifies the configuration for deploying the Docker image to AWS Elastic Beanstalk, including the Docker image name, port mappings, and volume mounts.

## CI/CD with GitHub Actions

- **deploy.yml**: Defines the CI/CD pipeline for deploying the application to AWS Elastic Beanstalk. It includes steps for checking out the code, setting up the Python environment, configuring AWS credentials, and deploying the application.

## Logging and Monitoring

- **Logging**: The application logs request and response details for debugging and monitoring purposes. Logs are stored in the `/var/log/cloud-clicker` directory.
- **Monitoring with AWS CloudWatch**: Logs can be monitored using AWS CloudWatch for real-time insights and alerting.

## Conclusion

Cloud Clicker is a comprehensive web application for tracking and displaying click counts, featuring user authentication, a responsive UI, and real-time data visualization. It is built using modern web technologies and is deployable via Docker and AWS Elastic Beanstalk, with CI/CD automation using GitHub Actions.
