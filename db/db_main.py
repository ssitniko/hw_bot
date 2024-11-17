import sqlite3


from db import queries



db = sqlite3.connect('db/store.sqlite3')
cursor = db.cursor()

async def sql_create():
    if db:
        print('База данных подключена!')
    cursor.execute(queries.CREATE_TABLE_TABLE)
    cursor.execute(queries.CREATE_TABLE_1)

async def sql_insert_product_details(product_id, category, info_product):
    cursor.execute(queries.INSERT_PRODUCT_DETAILS, (
        product_id, category, info_product
    ))

async def sql_insert_collection_products(product_id, collection):
    cursor.execute(queries.INSERT_COLLECTION, (
        product_id, collection
    ))

    db.commit()