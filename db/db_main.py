# db_main.py

import sqlite3
from db import queries



db = sqlite3.connect('db/store.sqlite3')
cursor = db.cursor()

async def sql_create():
    if db:
        print('База данных подключена!')
    cursor.execute(queries.CREATE_TABLE_STORE)
    cursor.execute(queries.CREATE_TABLE_TABLE)
    cursor.execute(queries.CREATE_TABLE_1)

async def sql_insert_store(name_product, size, collection, category, product_id, info_product, price, photo):

    cursor.execute(queries.INSERT_STORE, (
        name_product, size, collection, category, product_id, info_product, price, photo
    ))
    db.commit()



async def sql_insert_product_details(product_id, category, info_product):

    cursor.execute(queries.INSERT_PRODUCT_DETAILS, (
        product_id, category, info_product
    ))
    db.commit()


async def sql_insert_collection_products(product_id, collection):
    cursor.execute(queries.INSERT_COLLECTION, (
        product_id, collection
    ))

    db.commit()

def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
        SELECT * FROM store s
        INNER JOIN product_details sd ON s.product_id = sd.product_id
        """).fetchall()

    conn.close()
    return products

def fetch_one_product(name_product):
    conn = get_db_connection()
    product = conn.execute("""
        SELECT * FROM store WHERE name_product=?""",
        (name_product,)
        ).fetchone()

    conn.close()
    return product

def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM STORE WHERE product_id = ?', (product_id,))

    conn.commit()
    conn.close()