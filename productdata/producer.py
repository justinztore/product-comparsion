import sys

from productdata.tasks import crawler
from loguru import logger
from productdata import db
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import re

def update(dataset):

    logger.info(f"Producer update dataset : {dataset}")

    if dataset == "watsons_category" :
        print(f"starting run {dataset}")
        queue = 'watsons'
        task = crawler.s(dataset=dataset, parameters={'dataset':dataset, 'data_source':queue})
        task.apply_async(queue="watsons")

    if dataset == "watsons_product":

        meta = MetaData()

        schedule_task = Table(
            'schedule_task', meta, 
            Column('id', Integer, primary_key = True), 
            Column('type', String), 
            Column('platform', String), 
            Column('name', String), 
            Column('url', String), 
        )

        s = schedule_task.select().where(schedule_task.c.id <= 41)
        conn = db.router.mysql_productdata_conn
        result = conn.execute(s)

        queue = 'watsons'

        for row in result:
            print (row)

            if row.url != '':
                category_code = re.findall('[^/]+(?=/$|$)', row.url)[0]
                print(category_code)
                if category_code != '':
                    task = crawler.s(dataset=dataset, parameters={'dataset':dataset, 'data_source':queue, 'category_code':category_code})
                    task.apply_async(queue="watsons")
        
        pass

    if dataset == "hktvmall_category":
        pass
    
    if dataset == "hktvmall_product":
        pass

if __name__ == "__main__":
    (
        dataset,
    ) = sys.argv[1:]
    
    update(dataset)