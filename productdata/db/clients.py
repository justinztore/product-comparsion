from productdata.config import (
    MYSQL_DATA_USER,
    MYSQL_DATA_PASSWORD,
    MYSQL_DATA_HOST,
    MYSQL_DATA_PORT,
    MYSQL_DATA_DATABASE,
)

from sqlalchemy import (
    create_engine,
    engine,
)


def get_mysql_productdata_conn() -> engine.base.Connection:
    
    address = (
        f"mysql+pymysql://{MYSQL_DATA_USER}:{MYSQL_DATA_PASSWORD}"
        f"@{MYSQL_DATA_HOST}:{MYSQL_DATA_PORT}/{MYSQL_DATA_DATABASE}"
    )
    print(address)
    engine = create_engine(address)
    connect = engine.connect()
    return connect