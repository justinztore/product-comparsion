import pymysql.cursors
import pandas as pd

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='test',
                             database='ProductData',
                             cursorclass=pymysql.cursors.DictCursor)


sql = "SELECT * FROM ProductData.products where updated_at >= '2022-08-24' and name like '%乳霜%'"
df = pd.read_sql(sql, connection, index_col='id')
print(df)


# with connection:
#     # with connection.cursor() as cursor:
#     #     # Create a new record
#     #     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
#     #     cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

#     # # connection is not autocommit by default. So you must commit to save
#     # # your changes.
#     # connection.commit()

#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "SELECT * FROM ProductData.products where updated_at >= '2022-08-24' and name like '%乳霜%'"
#         cursor.execute(sql)
#         result = cursor.fetchone()
#         print(result)