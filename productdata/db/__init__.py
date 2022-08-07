from productdata.db.router import (
    Router,
)
from productdata.db.db import *

router = Router()

def get_db_router():
    return router