from database.db import fetchrow,execute,fetch

# Категории
async def get_all_categories():
    categories = await fetch("""SELECT * FROM categories""")
    return categories

async def get_category_by_id(category_id: int):
    category = await fetchrow("""SELECT * FROM categories WHERE category_id = $1""",category_id)
    if category is None:
        return 
    return category

async def get_category_id_by_name(category_name: str):
    category = await fetchrow("""SELECT * FROM categories WHERE category_name = $1""",category_name)
    if category is None:
        return None
    return category['category_id']

async def get_category_name_by_product_id(product_id: int):
    product = await get_data_product_by_id(product_id=product_id)
    category = await get_category_by_id(category_id=product['category_id'])
    return category['name']

# Продукты
async def create_product(name: str, description: str, price: int, in_stock: int, category_id: int, photo_file_id: str):
    await execute("""INSERT INTO products(name,description,price,in_stock,category_id,photo_file_id) VALUES($1,$2,$3,$4,$5,$6)""",name,description,price,in_stock,category_id,photo_file_id)

async def get_all_products_by_category_name(category_name: str):
    category_id = await get_category_id_by_name(category_name=category_name)
    all_products = await fetch("""SELECT * FROM products WHERE category_id = $1""",category_id)
    return all_products

async def get_data_product_by_id(product_id: int):
    product = await fetchrow("""SELECT * FROM products WHERE product_id = $1""",product_id)
    if product is None:
        return None
    return product

async def get_data_product_by_name(product_name: int):
    product = await fetchrow('SELECT * FROM products WHERE name = $1',product_name)
    if product is None:
        return None
    return product

async def get_id_product_by_name(product_name: str):
    product = await get_data_product_by_name(product_name=product_name)
    if product is None:
        return None
    return product['product_id']


