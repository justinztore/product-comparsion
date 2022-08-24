import importlib
import typing

from productdata import db
from productdata.worker import app, CallbackTask

@app.task(base=CallbackTask)
def crawler(dataset, parameters):
    # using getattr and importlib
    # according to sifferent data set to use different crawler to get data
    # 

    df = getattr(
        importlib.import_module(f"productdata.crawler.{dataset}"),
        "crawler", 
    ) (parameters=parameters)

    print(df)

    table = 'schedule_task'
    if parameters['dataset'] == 'watsons_product' or parameters['dataset'] == 'hktvmall_product':
        table = 'products'

    db.upload_data(df, table, db.router.mysql_productdata_conn)

    print("call crawler success")