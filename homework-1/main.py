"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
from psycopg2.extensions import cursor
from csv import reader
from settings import DB_IMPORT_TABLES, DATABASE_CON
import logging
import sys

log = logging.getLogger('data_exporter')


def write_to_db(cur: cursor, table_name: str, columns: list[str], data: list):
    """
    Writes data to database
    :param cur: DB cursor
    :param table_name: Table name
    :param columns: Table columns
    :param data: Data for write
    """

    query = f'INSERT INTO {table_name} ({",".join(columns)}) VALUES ({",".join(["%s"] * len(columns))})'
    for row in data:
        cur.execute(query, row)


def get_data_from_csv(file_name: str, encoding: str = 'utf-8', delimiter: str = ',') -> (list[str], list):
    """
    Load data list from csv file
    :param file_name: CSV file name
    :param encoding: File encoding
    :param delimiter: CSV file data delimiter
    :return: Tuple (column_names, data_list)
    """
    with open(file_name, 'r', encoding=encoding) as file:
        csv_reader = reader(file, delimiter=delimiter)
        return next(csv_reader), [row for row in csv_reader]


def main():
    try:
        with psycopg2.connect(**DATABASE_CON) as connection:
            with connection.cursor() as cur:
                for table_name, file_name in DB_IMPORT_TABLES:
                    columns, data = get_data_from_csv(file_name)
                    write_to_db(cur, table_name, columns, data)
    except Exception as e:
        log.exception(e)
    finally:
        connection.close()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
    main()
