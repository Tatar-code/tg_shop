from database.db import fetchrow,execute
from database.user_queries import get_user_by_tg_id,get_user_by_id
from database.product_queries import get_data_product_by_id

async def create_cart(user_id: int):
    cart = await get_cart_by_user_id(user_id=user_id)
    if cart is not None:
        return None
    cart = await execute("""INSERT INTO carts(user_id) VALUES ($1)""",user_id)
    cart = await get_cart_by_user_id(user_id=user_id)
    return cart['cart_id']


async def add_product_to_cart(cart_id:int, product_id: int):
    product = await get_summary_for_product_in_cart(cart_id=cart_id,product_id=product_id)
    if product is None:
        await execute("""INSERT INTO carts_products (cart_id,product_id) VALUES ($1,$2)""",cart_id,product_id)
        return None
    await set_summary_for_product_in_cart(cart_id=cart_id,product_id=product,summary=product + 1)

async def get_all_products_in_cart(cart_id: int):
    products_in_cart = await execute("""SELECT * FROM carts_products WHERE cart_id = $1""",cart_id)
    return products_in_cart

async def get_cart_by_user_id(user_id: int):
    cart = await fetchrow("""SELECT * FROM carts WHERE user_id = $1""",user_id)
    if cart is None:
        return None
    return cart

async def get_cart_by_tg_id(tg_id: int):
    user = await get_user_by_tg_id(tg_id=tg_id)
    cart = await fetchrow("""SELECT * FROM carts WHERE user_id = $1""",user['user_id'])
    if cart is None:
        return None
    return cart

async def get_summary_for_product_in_cart(cart_id: int, product_id: int):
    product = await fetchrow("""SELECT * FROM carts_products WHERE cart_id = $1 AND product_id = $2""",cart_id,product_id)
    if product is None:
        return None
    return product['summary']

async def set_summary_for_product_in_cart(cart_id: int, product_id: int, summary: int):
    await execute("""UPDATE carts_products SET summary = $1 WHERE cart_id = $2 AND product_id = $3""",summary,cart_id,product_id)


