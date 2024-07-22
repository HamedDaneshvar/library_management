# fastapi-postgres-boilerplate
This project template uses FastAPI, Alembic, SQLAlchemy as ORM, Rocketry as a scheduler, Celery as an async task manager with RabbitMQ. It demonstrates a complete async CRUD template. Additionally, I have set up a caching app with an invalidate feature using Redis.

## Project Execution and Documentation
To run the project and access its documentation, follow the steps below:

1. Access the project's README file which contains specifications and execution instructions by opening the following address: [README](app/README.md).
2. Clone the repository: `git clone <repository_url>`
3. Copy the `app/.env-example` file and rename it to `app/.env`.
4. Execute the command to start the project: `docker-compose up -d --build`.
