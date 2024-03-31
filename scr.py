import json

with open('petlebi_products.json', encoding='utf-8') as f:
    data = json.load(f)

with open('petlebi_insert.sql', 'w', encoding='utf-8') as f:
    for item in data:
        name = item['name'].replace("'", "''")
        product_images = json.dumps(item['images']).replace('"', '\\"')
        description = item['description'].replace("'", "''")
        product_id = int(item['id'])
        brand = item['brand'].replace("'", "''")

        sql = f"""
        INSERT INTO petlebi (
            product_url, product_name, product_barcode, product_price, 
            product_stock, product_images, description, sku, 
            category, product_id, brand
        ) VALUES (
            '{item['url']}', '{name}', '{item['barcode']}', '{item['price']}', 
            '{item['stock']}', '{product_images}', '{description}', '{item['sku']}', 
            '{item['category']}', {product_id}, '{brand}'
        );
        """

        f.write(sql)