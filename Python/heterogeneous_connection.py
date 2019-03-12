from pandas import concat, DataFrame, Series
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


PG_NAME = 'postgres'
PG_USER = 'postgres'
PG_HOST = 'localhost'
PG_PORT = 5432
PG_PASSWORD = 'system'

ORA_USER = 'HR'
ORA_PASSWORD = 'HR'
ORA_HOST = 'localhost'
ORA_PORT = 1521
ORA_SID = 'XE'


Base = declarative_base()


class CustomersPG(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)


class CustomersORA(Base):
    __tablename__ = 'customers2'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)


if __name__ == '__main__':
    db_statement_pg = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'.format(
                user=PG_USER,
                password=PG_PASSWORD,
                host=PG_HOST,
                port=PG_PORT,
                name=PG_NAME
            )
    db_statement_ora = 'oracle+cx_oracle://{user}:{password}@{host}:{port}/{sid}'.format(
                user=ORA_USER,
                password=ORA_PASSWORD,
                host=ORA_HOST,
                port=ORA_PORT,
                sid=ORA_SID
            )

    engine_pg = create_engine(db_statement_pg)
    engine_ora = create_engine(db_statement_ora)

    Session_pg = sessionmaker(bind=engine_pg)
    session_pg = Session_pg()
    result_pg = Series(session_pg.query(CustomersPG).all())

    Session_ora = sessionmaker(bind=engine_ora)
    session_ora = Session_ora()
    result_ora = Series(session_ora.query(CustomersORA).all())

    frames = [result_pg, result_ora]
    data_set = DataFrame(
        concat(
            frames,
            axis=0,
            join='inner'
        )
    )

    session_pg.close()
    session_ora.close()
