from database.db import fetchrow,execute
from database.user_queries import get_user_by_tg_id,get_user_by_id

async def create_cart(user_id: int):
    cart = await get_cart_by_user_id(user_id=user_id)
    if cart is not None:
        return
    cart = await execute("""INSERT INTO carts(user_id) VALUES ($1)""",user_id)
    cart = await get_cart_by_user_id(user_id=user_id)
    return cart['cart_id']


async def add_product_to_cart(cart_id:int, product_id: int):
    await execute("""INSERT INTO carts_products (cart_id,product_id) VALUES ($1,$2)""",cart_id,product_id)

async def get_all_products_id_in_cart(cart_id: int):
    products_id_in_cart = await execute("""SELECT * FROM carts_products WHERE cart_id = $1""",cart_id)
    return products_id_in_cart

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



