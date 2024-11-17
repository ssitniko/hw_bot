
CREATE_TABLE_TABLE = '''CREATE TABLE IF NOT EXISTS product_details(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT,
    category TEXT,
    info_product TEXT
)
'''

CREATE_TABLE_1 = '''CREATE TABLE IF NOT EXISTS collection_products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT,
    collection
)
'''

INSERT_PRODUCT_DETAILS = '''
    INSERT INTO product_details(product_id, category, info_product)
    VALUES (?, ?, ?)
'''

INSERT_COLLECTION = '''
    INSERT INTO collection_products(product_id, collection)
    VALUES (?, ?)
'''