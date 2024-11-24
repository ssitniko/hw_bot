# queries.py

CREATE_TABLE_STORE = '''CREATE TABLE IF NOT EXISTS store(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_product TEXT,
    size TEXT,
    collection TEXT,
    category TEXT,
    product_id TEXT,
    info_product TEXT,
    price TEXT,
    photo
)
'''



CREATE_TABLE_TABLE = '''CREATE TABLE IF NOT EXISTS product_details(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT,
    category TEXT,
    info_product
)
'''

CREATE_TABLE_1 = '''CREATE TABLE IF NOT EXISTS collection_products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT,
    collection
)
'''

INSERT_STORE = '''
    INSERT INTO store(name_product, size, collection, category, product_id, info_product, price, photo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
'''


INSERT_PRODUCT_DETAILS = '''
    INSERT INTO product_details(product_id, category, info_product)
    VALUES (?, ?, ?)
'''

INSERT_COLLECTION = '''
    INSERT INTO collection_products(product_id, collection)
    VALUES (?, ?)
'''