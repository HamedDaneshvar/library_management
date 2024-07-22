# Technical Task

## Project Overview
This project is a library management system developed using FastAPI, Alembic, PostgreSQL, and other technologies. It provides functionality for managing library operations. The system supports two types of users: employees (library staff) and customers. Employees can handle tasks related to book lending and sales, while customers can request book loans.

Automatic book sales are implemented, and no expert approval is required. However, for book borrowing, a customer needs to submit a request, and upon verification by an employee, the book can be borrowed if the specified conditions mentioned in the technical task are met.

You can view the database schema design for this technical task by opening the file [Library_Management_db_schema.drawio](Library_Management_db_schema.drawio.html).

To run the project, follow these steps:
1. Copy the `.env-example` file and rename it to `.env`.
2. Execute the following command to run the project on Docker:
   ```
   docker-compose up -d --build
   ```
3. Access the project via the link [http://localhost:8091/](http://localhost:8091/).
4. To explore the API documentation, visit [http://localhost:8091/docs](http://localhost:8091/docs).

By default, fake data models are used for demonstration purposes.

To log in as an employee, you can use the following credentials with the [login endpoint](http://localhost:8091/api/v1/users/token):

```
email: admin@gmail.com
password: adminpassword
```

To log in as a customer, you can use the following credentials with the [login endpoint](http://localhost:8091/api/v1/users/token):

```
email: user@gmail.com
password: user
```
