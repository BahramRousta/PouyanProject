# PouyanProject

PouyanProject is a social networking project based on the Django Rest Framework. It provides a RESTful API for various social networking features.

## Installation

To get started with the PouyanProject, follow the steps below:
1. Clone the repository:
    ```shell
    git clone https://github.com/BahramRousta/PouyanProject.git
    ```

2. Navigate to the project directory:

    ```shell
    cd PouyanProject
    ```

3. Build and start the Docker containers:

    ```shell
    docker-compose up
    ```

4. Run tests (optional):

    ```shell
    docker exec social_network sh -c 'pytest'
    ```
   
    This command will execute the test suite and provide feedback on the functionality and integrity of the project.


5. Access the service:

    The server will start running at [http://localhost:8000/swagger/](http://localhost:8000/swagger/), where you can explore the API using the Swagger UI interface.


## Features

The PouyanProject Django REST service offers the following features:

**API Endpoints**: 
The service provides a comprehensive set of API endpoints for various social networking functionalities such as user management, posts, comments, likes.

**Authentication and Authorization**: Secure authentication mechanisms are implemented to protect user data and restrict access to authorized users only. Choose from JWT authentication.

**Input Validation and Serialization**: The service ensures proper input validation and serialization of data to prevent security vulnerabilities and improve reliability.

**Error Handling**: Custom error responses are implemented, and common exceptions are handled gracefully to provide informative feedback to API consumers and improve service robustness.

**Pagination**: API endpoints that return a large number of results are paginated, improving performance and usability, especially with large datasets.

**Caching**: Caching mechanisms are utilized to cache frequently accessed data, enhancing response times. Choose from Redis as an external solutions.

**Logging and Monitoring**: Comprehensive logging is implemented to track and debug issues effectively.

**Unit Testing and Test Coverage**: The project includes a suite of unit tests to ensure the correctness of the service. Use tools is pytest.