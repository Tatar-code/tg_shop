from database.db import fetchrow,execute,fetch
from database.admins_queries import find_user_id_by_tg_id,find_user_data_by_id

async def find_category_id_by_name(category_name: str):
    category = await fetchrow("""SELECT * FROM categories WHERE category_name = $1""",category_name)
    if category is None:
        return None
    return category['category_id']

async def create_product(name: str, description: str, price: int, in_stock: int, category_id: int, photo_file_id: str):
    await execute("""INSERT INTO products(name,description,price,in_stock,category_id,photo_file_id) VALUES($1,$2,$3,$4,$5,$6)""",name,description,price,in_stock,category_id,photo_file_id)

async def get_all_categories():
    categories = await fetch("""SELECT * FROM categories""")
    return categories

async def get_all_products_by_category_name(category_name: str):
    category_id = await find_category_id_by_name(category_name=category_name)
    all_products = await fetch("""SELECT * FROM products WHERE category_id = $1""",category_id)
    return all_products

async def get_data_product_by_id(product_id: int):
    product = await fetchrow("""SELECT * FROM products WHERE product_id = $1""",product_id)
    if product is None:
        return None
    return product

async def get_id_product_by_name(product_name: str):
    product = await fetchrow('SELECT * FROM products WHERE name = $1',product_name)
    if product is None:
        return None
    return product['product_id']

async def get_category_name_by_product_id(product_id: int):
    product = fetchrow("""SELECT * FROM products WHERE product_id = $1""",product_id)
    category = fetchrow("""SELECT * FROM categories WHERE category_id = $1""",product['category_id'])
    return category['name']

async def create_cart(user_id: int):
    cart = await fetchrow("""SELECT * FROM carts WHERE user_id = $1""",user_id)
    if cart is not None:
        return None
    cart = await execute("""INSERT INTO carts(user_id) VALUES ($1)""",user_id)
    cart = await fetchrow("""SELECT * FROM carts WHERE user_id = $1""",user_id)
    return cart['cart_id']


async def send_product_to_cart(cart_id:int, product_id: int):
    await execute("""INSERT INTO carts_products (cart_id,product_id) VALUES ($1,$2)""",cart_id,product_id)

async def get_cart_by_tg_id(tg_id: int):
    user_id = await find_user_id_by_tg_id(tg_id=tg_id)
    user = await find_user_data_by_id(user_id=user_id)
    cart_id = user['user_cart']
    products_in_cart = await execute("""SELECT * FROM carts_products WHERE cart_id = $1""",cart_id)
    return products_in_cart