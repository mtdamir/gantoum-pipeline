Gantoum Simple Order Management System

Project Overview
This project is a simple ETL system designed for managing Gantoum products, built using the stack of Airflow, FastAPI, and PostgreSQL. The primary goal of the project is to create an efficient and streamlined platform for handling user orders and automating product data management.

The app section consists of a set of RESTful APIs that allow users to register, log into their accounts, and place orders for products using token-based authentication. Data storage is handled by a PostgreSQL database, which includes the users, products, and orders tables.

The dags section is implemented using Airflow and is responsible for extracting product data from a website. It includes DAGs that run periodically to collect new product data, process it, and store it in the products table of the database. This automated process ensures that the product catalog in the system remains up-to-date.

Special attention has been given to security in the design of this project. This includes the use of token-based authentication (JWT) to secure the APIs, input validation to prevent common attacks, and secure database connection management to maintain data integrity and security. The project is containerized using Docker, making it easier to set up and deploy across different environments.


```
+----------------+       +-------------------------------------------+
|     User       |       |              FastAPI Application          |
|                |       |                                           |
|  [HTTP Requests]----->|  +-------------------+                    |
|                |       |  |     main.py      |                    |
|                |       |  +-------------------+                    |
|                |       |  | Routers           |                    |
|                |       |  | - users_router.py |                    |
|                |       |  | - purchases_router.py |                |
|                |       |  +-------------------+                    |
|                |       |  | Services          |                    |
|                |       |  | - user_service.py |                    |
|                |       |  | - purchases_service.py |               |
|                |       |  +-------------------+                    |
|                |       |  | Schemas & DTOs    |                    |
|                |       |  | - schemas/        |                    |
|                |       |  | - dtos/           |                    |
|                |       |  +-------------------+                    |
|                |       |  | Guards            |                    |
|                |       |  | - user_guards.py  |                    |
|                |       |  +-------------------+                    |
|                |       |  | Config            |                    |
|                |       |  | - settings.py     |                    |
|                |       |  +-------------------+                    |
+----------------+       |                                           |
                        +-------------------------------------------+
                                    |
                                    | [DB Queries]
                                    v
                        +----------------------------+       +-----------------+
                        |            db/            |       |    PostgreSQL   |
                        | - postgres_connection.py  |<----->| - users         |
                        | - create_user_table.py    |       | - products      |
                        | - create_order_table.py   |       | - orders        |
                        +----------------------------+       +-----------------+
                                    ^
                                    | [Insert Data]
                                    |
                        +----------------------------+
                        |          Airflow           |
                        | - load_products_dag.py    |
                        +----------------------------+
```
