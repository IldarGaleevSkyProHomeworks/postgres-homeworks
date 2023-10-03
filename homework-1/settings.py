import os

DATABASE_CON = {
    'host': 'localhost',
    'port': 5432,
    'database': 'north',
    'user': 'postgres',
    'password': os.getenv('POSTGRES_PWD'),
}

DB_IMPORT_TABLES = [
    ('employees', 'homework-1/north_data/employees_data.csv'),
    ('customers', 'homework-1/north_data/customers_data.csv'),
    ('orders', 'homework-1/north_data/orders_data.csv'),
]
