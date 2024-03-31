import configparser
import pymysql
import json


with open('petlebi_products.json') as f:
    data = json.load(f)

config = configparser.ConfigParser()
config.read('config.ini')

host = config['mysql']['host']
user = config['mysql']['user']
password = config['mysql']['password']
database = config['mysql']['database']

conn = pymysql.connect(user=user, password=password, host=host, database=database)

try:
    with conn.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")

        cursor.execute("USE petlebi")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS petlebi (
                       product_url VARCHAR(255),
                       product_name VARCHAR(255),
                       product_barcode VARCHAR(50),
                       product_price VARCHAR(50),
                       product_stock VARCHAR(50),
                       product_images TEXT,
                       description TEXT,
                       sku VARCHAR(50),
                       category TEXT,
                       product_id INT PRIMARY KEY,
                       brand VARCHAR(255)
        )
        """)

        for item in data:
            sql = """
            INSERT INTO petlebi (
                product_url, product_name, product_barcode, product_price, 
                product_stock, product_images, description, sku, 
                category, product_id, brand
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """

            product_images = json.dumps(item['images'])
            product_id = int(item['id'])

            datum = (item['url'], item['name'], item['barcode'], item['price'], 
                    item['stock'], product_images, item['description'], item['sku'], 
                    item['category'], product_id, item['brand'])
            
            cursor.execute(sql, datum)

        conn.commit()

finally:
    conn.close()