import cx_Oracle as ora
import pandas as pd


DATABASE_USER = 'HR'
DATABASE_PASSWORD = 'HR'
DATABASE_TNS = '(DESCRIPTION= \
                    (ADDRESS= \
                        (PROTOCOL = TCP) \
                        (HOST = localhost) \
                        (PORT = 1521) \
                    ) \
                    (CONNECT_DATA= \
                        (SERVER=DEDICATED) \
                        (SERVICE_NAME=XE) \
                    ) \
                )'


def check_connect():
    try:
        conn = ora.connect(
            DATABASE_USER,
            DATABASE_PASSWORD,
            DATABASE_TNS.replace(
                ' ',
                ''
            )
        )
    except ora.DatabaseError as e:
        print("You've got Database Error {}".format(e))
        raise

    return conn


def get_data(conn):
    ora_cursor = conn.cursor()
    ora_cursor.execute(query)
    data_set = pd.DataFrame(
        ora_cursor.fetchall(),
        index=None,
        columns=[
            'full_name',
            'column_name',
            'column_desc'
        ]
    )
    return data_set, ora_cursor


def upload_data(data_set, ora_cursor):
    ora_cursor.execute("truncate table columns_table")

    for index, row in data_set.iterrows():
        ora_cursor.execute(
            "insert into columns_table (full_name, \
                                        column_name, \
                                        column_desc) values (:1, \
                                                             :2, \
                                                             :3)",
            row)

    ora_cursor.execute('commit')
    ora_cursor.close()


if __name__ == '__main__':
    query = ' '.join(
        [
            row for row in open(
                'ora_query.sql',
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
    connection.close()
