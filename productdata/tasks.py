import importlib
import typing

from productdata.worker import app

@app.task()
def crawler(dataset, parameters):
    # using getattr and importlib
    # according to sifferent data set to use different crawler to get data
    # 

    df = getattr(
        importlib.import_module(f"productdata.crawler.{dataset}"),
        "crawler", 
    ) (parameters=parameters)

    print(df)

    print("call crawler success")