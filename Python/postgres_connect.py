from psycopg2 import sql, connect, DatabaseError
import pandas as pd


DATABASE_NAME = 'postgres'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = 'system'


def check_connect():
    try:
        conn = connect(
            dbname=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD
        )
        conn.autocommit = True
    except DatabaseError as e:
        print("You've got Database Error {}".format(e.pgerror))
        raise

    return conn


def get_data(conn):
    pg_cursor = conn.cursor()
    pg_cursor.execute(query)
    data_set = pd.DataFrame(
        pg_cursor.fetchall(),
        index=None,
        columns=[
            'full_name',
            'column_name',
            'column_desc'
        ]
    )
    return data_set, pg_cursor


def upload_data(data_set, pg_cursor):
    pg_cursor.execute("truncate columns_table")

    for index, row in data_set.iterrows():
        pg_cursor.execute(
            sql.SQL(
                'insert into {} values (%s, %s, %s)'
            ).format(
                sql.Identifier(
                    'columns_table'
                )
            ),
            [
                row["full_name"],
                row["column_name"],
                row["column_desc"]
            ]
        )


if __name__ == '__main__':
    query = ' '.join(
        [
            row for row in open(
                'pg_query.sql',
                'r',
                encoding='ANSI'
            )
        ]
    )
    connection = check_connect()
    data_set, cur = get_data(
        connection
    )
    upload_data(
        data_set,
        cur
    )
    connection.commit()
