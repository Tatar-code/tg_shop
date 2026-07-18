from database.db import fetch,fetchrow,execute
    


async def create_user(tg_id: int, username: str):
    from database.role_queries import set_user_role
    from database.cart_queries import create_cart
    user = await get_user_by_tg_id(tg_id=tg_id)
    if user is None:
        await execute("""INSERT INTO users (tg_id,username) VALUES ($1,$2)""",tg_id,username)
        user = await get_user_by_tg_id(tg_id=tg_id)
        cart = await create_cart(user_id=user['user_id'])
        await set_user_role(user_id=user['user_id'],role_id=1)
        await execute("""UPDATE users SET user_cart = $1 WHERE user_id = $2""",cart,user['user_id'])
    else:
        return False
    return True

async def get_user_by_tg_id(tg_id: int):
    user = await fetchrow("""SELECT * FROM users WHERE tg_id = $1""",tg_id)
    if user is None:
        return None
    return user


async def get_user_by_id(user_id: int):
    user = await fetchrow("""SELECT * FROM users WHERE user_id = $1""",user_id)
    if user is None:
        return None
    return user