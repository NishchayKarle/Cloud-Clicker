# Cloud Clicker

+ Find the app [here](http://cloudclickerenv.eba-4fpezeke.us-east-1.elasticbeanstalk.com)
+ http://cloudclickerenv.eba-4fpezeke.us-east-1.elasticbeanstalk.com


## Project Overview

+ Cloud Clicker is a web application designed to track and display click counts.
+ The application supports user authentication, allows users to increment their click count, and displays overall and user-specific click data in real time.
+ The application also includes a dashboard that shows click statistics over time, including total clicks and clicks per minute.
+ The application also has a comprehensive logging system to keep track of all aspects of the application.
+ On code push deployment to AWS Elastic Beanstalk

## Table of Contents

- [Cloud Clicker](#cloud-clicker)
  - [Project Overview](#project-overview)
  - [Table of Contents](#table-of-contents)
  - [Sequence Diagram](#sequence-diagram)
  - [Design Diagram](#design-diagram)
  - [Project Structure](#project-structure)
  - [Features](#features)
  - [Real-Time Click Updates](#real-time-click-updates)
    - [Implementation Details](#implementation-details)
      - [Backend](#backend)
      - [Frontend](#frontend)
      - [Steps](#steps)
  - [Database and Consistency](#database-and-consistency)
    - [Database](#database)
    - [Database Schema](#database-schema)
    - [Consistency](#consistency)
    - [Initialization](#initialization)
  - [API Endpoints](#api-endpoints)
    - [POST /api/register](#post-apiregister)
    - [POST /api/login](#post-apilogin)
    - [POST /api/clicks](#post-apiclicks)
    - [GET /api/clicks](#get-apiclicks)
    - [GET /api/clicks/log](#get-apiclickslog)
  - [Frontend Pages](#frontend-pages)
  - [Logging and Monitoring](#logging-and-monitoring)
  - [Dashboard](#dashboard)
    - [Features](#features-1)
    - [Implementation](#implementation)
      - [Backend](#backend-1)
      - [Frontend](#frontend-1)
  - [Deployment](#deployment)
    - [Docker Setup](#docker-setup)
    - [CI/CD with GitHub Actions](#cicd-with-github-actions)
  - [AWS Setup](#aws-setup)
    - [Steps Involved](#steps-involved)
    - [Consistency Between Deployments](#consistency-between-deployments)
  - [Technologies Used](#technologies-used)
  - [Thoughts on possible Improvements](#thoughts-on-possible-improvements)
    - [API Scaling](#api-scaling)
    - [Scaling the Number of Servers](#scaling-the-number-of-servers)
  - [Conclusion](#conclusion)

## Sequence Diagram
![Sequence Diagram](/diagrams/sequence_diag.drawio.jpeg)

## Design Diagram
![Design Diagram](/diagrams/system_design.drawio.jpeg)


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

## Real-Time Click Updates

![Live Updates Gif](/screenshots/LiveUpdates.gif)

Cloud Clicker provides real-time updates for click counts to ensure all users see the most current data without needing to refresh their browser. This is achieved through a combination of regular polling and client-side updates using JavaScript.

### Implementation Details

#### Backend

The backend exposes an API endpoint `/api/clicks` that returns the current total and user-specific click counts. This endpoint is used by the frontend to fetch the latest click data at regular intervals.

#### Frontend

The frontend periodically fetches the latest click data from the backend and updates the user interface accordingly. This is done using JavaScript's `setInterval` function to make periodic API calls and update the DOM with the new data.

#### Steps

1. **Initial Load**:
   - When a user navigates to the clicks page, the frontend makes an initial API call to fetch the current click counts.
   - The initial data is used to populate the click counts displayed on the page.

2. **Periodic Polling**:
   - The frontend sets up a timer using `setInterval` to periodically make GET requests to the `/api/clicks` endpoint.
   - This ensures that the click counts are updated regularly without requiring a page refresh.

3. **DOM Updates**:
   - The data returned from the API call is used to update the click count elements in the DOM.
   - The total click count and user-specific click count (if the user is authenticated) are updated in real-time.

4. **Handling User Clicks**:
   - When a user clicks the "Click Me!" button, a POST request is made to the `/api/clicks` endpoint to increment the click counts.
   - The response from this request includes the updated total and user-specific click counts, which are then used to update the DOM immediately.


## Database and Consistency

### Database

Cloud Clicker uses SQLite for its database management system.

### Database Schema

The database schema consists of the following tables:

1. **users**:
   - **id** (INTEGER, Primary Key): Unique identifier for each user.
   - **username** (TEXT, Unique): Username of the user.
   - **password** (TEXT): Hashed password of the user.

2. **clicks**:
   - **id** (INTEGER, Primary Key): Unique identifier for the click record.
   - **count** (INTEGER): Total click count across all users.

3. **user_clicks**:
   - **user_id** (INTEGER, Foreign Key): Identifier linking to the user.
   - **clicks** (INTEGER): Click count specific to the user.

4. **click_log**:
   - **id** (INTEGER, Primary Key): Unique identifier for each click log entry.
   - **user_id** (INTEGER, Foreign Key): Identifier linking to the user.
   - **timestamp** (TEXT): Timestamp of the click event.

### Consistency

To maintain consistency within the database, the following strategies are implemented:

1. **Atomic Transactions**:
   - Each database operation that modifies data (e.g., incrementing click counts) is wrapped in a transaction. This ensures that the operations are atomic, meaning they are all-or-nothing. If an error occurs during a transaction, the entire transaction is rolled back to maintain database integrity.

2. **Foreign Key Constraints**:
   - The database schema uses foreign key constraints to enforce relationships between tables. For example, the `user_clicks` and `click_log` tables have foreign keys linking to the `users` table. This ensures referential integrity by preventing orphaned records.

3. **Data Validation**:
   - Data validation is performed at the application level before any data is written to the database. This includes checking for unique usernames during registration and ensuring valid data types for each field.

4. **Concurrent Access Handling**:
   - SQLite handles concurrent access using file locks. While SQLite supports multiple readers and a single writer, it's important to design the application to minimize write contention. In Cloud Clicker, operations that modify click counts are designed to be quick and efficient to reduce the likelihood of write contention.

5. **Error Handling**:
   - Comprehensive error handling is implemented to catch and log database-related errors. This helps in identifying and resolving issues promptly, ensuring the reliability of the application.

### Initialization

- **Database Initialization**:
  - The database is initialized using the `init_db` function in the `application.py` file. This function creates the necessary tables if they do not already exist and inserts initial data where applicable (e.g., setting the initial click count to 0).

- The database will be mounted at `/var/lib/cloud-clicker/` and stored at `/app/db` on the docker container


## API Endpoints

### POST /api/register

- **Description**: Registers a new user.
- **Request Body Parameters**:
  - `username` (string): The desired username for the new user.
  - `password` (string): The password for the new user.
- **Responses**:
  - **201 Created**: Indicates that the user was registered successfully.
  - **409 Conflict**: Indicates that the username already exists.

### POST /api/login

- **Description**: Logs in a user and returns a JWT token.
- **Request Body Parameters**:
  - `username` (string): The username of the user.
  - `password` (string): The password of the user.
- **Responses**:
  - **200 OK**: Indicates that the login was successful and returns a JWT token.
  - **401 Unauthorized**: Indicates that the username or password is incorrect.

### POST /api/clicks

- **Description**: Increments the total click count and the user's click count. This endpoint requires authentication.
- **Headers**:
  - `Authorization` (string): Bearer token obtained from the login endpoint.
- **Responses**:
  - **200 OK**: Indicates that the click count was incremented successfully and returns the updated total and user-specific click counts.
  - **401 Unauthorized**: Indicates that authentication is required to access this endpoint.

### GET /api/clicks

- **Description**: Retrieves the total click count and, if authenticated, the user's click count.
- **Headers** (optional):
  - `Authorization` (string): Bearer token obtained from the login endpoint.
- **Responses**:
  - **200 OK**: 
    - If authenticated, returns both the total click count and the user's click count.
    - If not authenticated, returns only the total click count.

### GET /api/clicks/log

- **Description**: Retrieves click data over time and clicks per minute.
- **Responses**:
  - **200 OK**: Returns logs of click data, including timestamps of each click, and clicks per minute.
  - **500 Internal Server Error**: Indicates an error occurred while fetching the data.


## Frontend Pages

- **index.html**: Landing page with options to sign in or sign up, and links to view clicks and the dashboard.
- **clicks.html**: Displays total clicks and user-specific clicks. Allows authenticated users to increment their click count.
- **charts.html**: Dashboard displaying click statistics over time, including total clicks and clicks per minute.


## Logging and Monitoring

- **Logging Configuration**:
    - A rotating file handler to handle log rotation and prevent the log file from growing indefinitely.
    - Logs are stored in the logs directory with a max size of 10MB.

- **Logging Key Events**:
    - Log messages for user registration, login attempts (both successful and failed), click counts retrieval, and click count increments.

    - The application logs request and response details for debugging and monitoring purposes. Logs are stored in the `/var/log/cloud-clicker` directory. 
    - The `@app.before_request` decorator is used to register a function to be executed before each request in your Flask application. This is part of Flask's request lifecycle, where we can hook into different stages of request processing to execute custom code.
    - **Function Execution**:
        - **Headers Logging**: `app.logger.info('Headers: %s', request.headers)`
        - Logs the headers of the incoming request.
        - **Body Logging**: `app.logger.info('Body: %s', request.get_data())`
        - Logs the body of the incoming request.

-
    ```python
    @app.before_request
    def log_request_info():
        """Log the request information before processing a request."""
        app.logger.info("Headers: %s", request.headers)
        app.logger.info("Body: %s", request.get_data())
    ```

- **Monitoring with AWS CloudWatch**: Logs can be monitored using AWS CloudWatch for real-time insights and alerting. CloudWatch allows you to view, search, and monitor the logs generated by your application. You can set up metrics and alarms based on specific log patterns to get alerted when certain conditions are met.



## Dashboard

![Dashboard](/screenshots/dashboard.jpeg)

The Cloud Clicker dashboard provides real-time visualizations of click statistics, including total clicks over time and clicks per minute. This helps users track and analyze click trends and activity levels.

### Features

- **Total Clicks Over Time**: Line chart displaying cumulative clicks over a period.
- **Clicks Per Minute**: Bar chart showing the number of clicks recorded each minute.

### Implementation

#### Backend

The `/api/clicks/log` endpoint provides click event logs with timestamps, used to calculate and visualize click data.

#### Frontend

- **Chart.js**: Used to render the charts.
- **Periodic Updates**: The dashboard fetches data at regular intervals to keep the charts updated in real-time.


## Deployment

### Docker Setup

- **Dockerfile**: Contains the instructions for building the Docker image, including setting up the Python environment, installing dependencies, and running the application.
- **Dockerrun.aws.json**: Specifies the configuration for deploying the Docker image to AWS Elastic Beanstalk, including the Docker image name, port mappings, and volume mounts.

### CI/CD with GitHub Actions

- **deploy.yml**: Defines the CI/CD pipeline for deploying the application to AWS Elastic Beanstalk. It checks out the code, sets up the Python environment, configures AWS credentials (using github secrets), and deploys the application.

## AWS Setup
Cloud Clicker is deployed using AWS Elastic Beanstalk, which simplifies the process of deploying, managing, and scaling the application. The setup involves creating an environment, deploying the application in a docker managed environment, and ensuring that the database and logs are consistently maintained across deployments.

### Steps Involved

1. **Create Elastic Beanstalk Application**:
   - Github actions creates the Elastic Beanstalk Application and the Environment.
   - Select the appropriate platform (Docker) and configure the environment settings.

2. **Deploy the Application**:
   - Use the `Dockerrun.aws.json` file to specify the Docker container configuration.
   - Deploy the Docker container to the Elastic Beanstalk environment.

3. **Database Setup**:
   - SQLite is used as the database. The database file is stored within the application's filesystem.
   - Ensure the database file is properly backed up before each deployment.

4. **Logging Setup**:
   - Application logs are stored in the `/var/log/cloud-clicker` directory.
   - Use AWS CloudWatch to monitor and manage these logs for real-time insights and alerting.

### Consistency Between Deployments

Maintaining database and log consistency across deployments is crucial to ensure data integrity and application stability.

1. **Database Consistency**:
   - The SQLite database file is mounted on persistent storage, ensuring data consistency across deployments.
   - `/app/db` on the container is mounted at `/var/lib/cloud-clicker`
2. **Log Consistency**:
   - The log directory `/app/log` is mounted on the ec2 instance at `/var/log/cloud-clicker` ensuring log consistency across deployments.


## Technologies Used

- **Backend**: Python, Flask, SQLite, JWT
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Deployment**: Docker, AWS Elastic Beanstalk
- **CI/CD**: GitHub Actions

## Thoughts on possible Improvements
Looking at ways to enhance the Cloud Clicker application, there are several strategies we can implement to ensure it scales efficiently and remains responsive under increased traffic.

### API Scaling

To handle higher volumes of traffic and ensure our API remains performant, consider the following improvements:

1. **Load Balancing**:
   - Implementing load balancing will distribute incoming traffic across multiple instances of our application. Utilizing AWS Elastic Load Balancer (ELB) can help manage this distribution automatically, improving both fault tolerance and reliability.

2. **Horizontal Scaling**:
   - By scaling horizontally, we can add more server instances to handle increased load. AWS Auto Scaling can automatically adjust the number of instances based on traffic patterns, ensuring optimal performance during peak times and cost savings during low-traffic periods.

3. **Rate Limiting**:
   - Introducing rate limiting will protect our API from being overwhelmed by too many requests. Tools like Amazon API Gateway allow us to define usage plans and throttling limits, effectively managing API usage.

4. **Caching**:
   - Implementing caching mechanisms can significantly reduce the load on our database and improve response times. Using in-memory data stores like Redis or Memcached allows us to cache frequently accessed data, minimizing the need for repeated database queries.

5. **Asynchronous Processing**:
   - Offloading time-consuming tasks to background workers can help keep our API responsive. AWS SQS (Simple Queue Service) and AWS Lambda are great tools for processing tasks asynchronously.

6. **Database Optimization**:
   - Optimizing our database queries and indexing will enhance performance. We should consider using more robust database solutions like Amazon RDS (Relational Database Service) or Amazon DynamoDB to achieve better scalability and reliability.

### Scaling the Number of Servers

To efficiently scale the number of servers based on traffic, the following strategies should be considered:

1. **Auto Scaling Groups**:
   - Using AWS Auto Scaling Groups will allow us to automatically add or remove instances based on predefined metrics such as CPU utilization, memory usage, or request count. This ensures we have the right amount of resources to handle current traffic.

2. **Monitoring and Alerts**:
   - Setting up monitoring and alerts with AWS CloudWatch will help us keep track of application performance and resource usage. Custom CloudWatch alarms can notify us when thresholds are breached, enabling proactive scaling decisions.

3. **Infrastructure as Code (IaC)**:
   - Managing and automating the deployment and scaling of our infrastructure with Infrastructure as Code (IaC) tools like AWS CloudFormation or Terraform ensures consistency and repeatability in our scaling operations.

4. **Blue/Green Deployments**:
   - Implementing blue/green deployments minimizes downtime during scaling operations and updates. By running two identical environments and switching traffic between them, we can ensure seamless scaling and updates without affecting our users.

5. **Containerization and Orchestration**:
   - Containerizing our application with Docker and using orchestration tools like Kubernetes or AWS ECS (Elastic Container Service) provides robust scaling and self-healing capabilities.

6. **Serverless Architecture**:
   - Moving to a serverless architecture using AWS Lambda for handling individual API requests allows for automatic scaling and reduces the need for server management. AWS Lambda scales automatically with traffic, providing a highly scalable solution.


## Conclusion

Cloud Clicker is a comprehensive web application for tracking and displaying click counts, featuring user authentication, a responsive UI, and real-time data visualization. It is built using modern web technologies and is deployable via Docker and AWS Elastic Beanstalk, with CI/CD automation using GitHub Actions.
