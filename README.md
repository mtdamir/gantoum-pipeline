ساختار پروژه :
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
