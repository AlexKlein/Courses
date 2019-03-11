import pandas as pd
import sqlalchemy as db

DATABASE_TYPE = 'Oracle'

PG_NAME = 'postgres'
PG_USER = 'postgres'
PG_HOST = 'localhost'
PG_PORT = 5432
PG_PASSWORD = 'system'

ORA_USER = 'DMFRUA'
ORA_PASSWORD = 'DMFRUA$10'
ORA_HOST = 'bisrvzfs3'
ORA_PORT = 1521
ORA_SID = 'ZCMTST'


def check_connect(type):
    if type == 'PostgreSQL':
        db_statement = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'.format(
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT,
            name=PG_NAME
        )
    elif type == 'Oracle':
        db_statement = 'oracle+cx_oracle://{user}:{password}@{host}:{port}/{sid}'.format(
            user=ORA_USER,
            password=ORA_PASSWORD,
            host=ORA_HOST,
            port=ORA_PORT,
            sid=ORA_SID
        )
    else:
        print("I can't find Database driver")

    engine = db.create_engine(db_statement)
    connection = engine.connect()
    transaction = connection.begin()

    return connection, transaction


def get_query(type):
    if type == 'PostgreSQL':
        query = ' '.join(
            [
                row for row in open(
                    'pg_query.sql',
                    'r',
                    encoding='ANSI'
                )
            ]
        )
    elif type == 'Oracle':
        query = ' '.join(
            [
                row for row in open(
                    'ora_query.sql',
                    'r',
                    encoding='ANSI'
                )
            ]
        )
    else:
        print("I can't find query")

    return query


def get_data(conn, query):
    data_set = pd.read_sql(
        query,
        conn,
        index_col=None,
        columns=[
            'full_name',
            'column_name',
            'column_desc'
        ]
    )

    return data_set


def upload_data(data_set, conn):
    conn.execute("truncate table columns_table")

    for index, row in data_set.iterrows():
        conn.execute(
            'insert into {} values (%s, %s, %s)'.format('columns_table') % (
                "'" + row["full_name"] + "'",
                "'" + row["column_name"] + "'",
                "'" + row["column_desc"] + "'"
            )
        )


if __name__ == '__main__':
    connection, transaction = check_connect(DATABASE_TYPE)
    query = get_query(DATABASE_TYPE)

    data_set = get_data(
        connection,
        query
    )

    upload_data(
        data_set,
        connection
    )

    transaction.commit()
    connection.close()
