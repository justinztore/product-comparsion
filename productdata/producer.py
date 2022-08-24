import sys

from productdata.tasks import crawler
from loguru import logger
from productdata import db
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import re
from random import randint

def update(dataset):

    logger.info(f"Producer update dataset : {dataset}")

    if dataset == "watsons_category" :
        print(f"starting run {dataset}")
        queue = 'watsons'
        task = crawler.s(dataset=dataset, parameters={'dataset':dataset, 'data_source':queue})
        task.apply_async(queue=queue)

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

        #s = schedule_task.select().where(schedule_task.c.platform == 'watsons')
        s = schedule_task.select().where(schedule_task.c.id >= 126).where(schedule_task.c.id <= 147)
        conn = db.router.mysql_productdata_conn
        result = conn.execute(s)

        

        for row in result:
            print (row)

            if row.url != '':
                queue_number = randint(1,3)
                queue = f'watsons_{queue_number}'

                category_code = re.findall('[^/]+(?=/$|$)', row.url)[0]
                print(category_code)
                if category_code != '':
                    task = crawler.s(dataset=dataset, parameters={'dataset':dataset, 'data_source':queue, 'category_code':category_code, 'task_id':row.id})
                    task.apply_async(queue=queue)
        
        pass

    if dataset == "hktvmall_category":
        print(f"starting run {dataset}")
        queue = 'hktvmall'
        task = crawler.s(dataset=dataset, parameters={'dataset':dataset, 'data_source':queue})
        task.apply_async(queue=queue)

        pass
    
    if dataset == "hktvmall_product":
        print(f"starting run {dataset}")
        meta = MetaData()

        schedule_task = Table(
            'schedule_task', meta, 
            Column('id', Integer, primary_key = True), 
            Column('type', String), 
            Column('platform', String), 
            Column('name', String), 
            Column('url', String), 
        )

        #s = schedule_task.select().where(schedule_task.c.platform == 'hktvmall')
        s = schedule_task.select().where(schedule_task.c.id == 3)
        conn = db.router.mysql_productdata_conn
        result = conn.execute(s)

        for row in result:
            print (row)

            if row.url != '':
                queue_number = randint(1,3)
                queue = f'hktvmall_{queue_number}'

                category_code = re.findall('[^/]+(?=/$|$)', row.url)[0]
                print(category_code)
                if category_code != '':
                    task = crawler.s(dataset=dataset, parameters={'dataset':dataset, 'data_source':queue, 'category_code':category_code, 'task_id':row.id})
                    task.apply_async(queue=queue)

        # category_code = '3AAA16050000000'
        

        pass

if __name__ == "__main__":
    (
        dataset,
    ) = sys.argv[1:]
    
    update(dataset)