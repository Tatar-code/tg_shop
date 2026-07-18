from database.db import fetch,fetchrow,execute
from database.owners_queries import set_user_role
from database.admins_queries import find_user_id_by_tg_id
from database.product_queries import send_product_to_cart,create_cart
    


async def create_user(tg_id: int, username: str):
    user = await fetchrow("""SELECT * FROM users WHERE tg_id = $1""",tg_id)
    if user is None:
        await execute("""INSERT INTO users (tg_id,username) VALUES ($1,$2)""",tg_id,username)
        user = await find_user_id_by_tg_id(tg_id=tg_id)
        await set_user_role(user_id=user,role_id=1)
        cart = await create_cart(user_id=user)
        await execute("""UPDATE users SET user_cart = $1 WHERE user_id = $2""",cart,user)
    else:
        return False
    return True

async def create_petition(tg_id: int, petition_text: str):
    user_id = await find_user_id_by_tg_id(tg_id=tg_id)
    await execute("""INSERT INTO petitions (user_id, petition_text) VALUES ($1,$2)""",user_id,petition_text)
    petition = await fetchrow("""SELECT petition_id FROM petitions WHERE user_id = $1 ORDER BY created_at DESC LIMIT 1""",user_id)
    await execute("""INSERT INTO users_petitions (user_id, petition_id) VALUES ($1,$2)""",user_id, petition['petition_id'])


async def all_petitions_by_user(tg_id: int):
    all_petitions = []
    user_id = await find_user_id_by_tg_id(tg_id=tg_id)
    all_petitions_by_user = await fetch("""SELECT petition_id FROM users_petitions WHERE user_id = $1 ORDER BY petition_id DESC""",user_id)
    if all_petitions_by_user is None:
        return None
    for petition in all_petitions_by_user:
        all_petitions.append(petition['petition_id'])
    return all_petitions

async def get_data_by_petition(petition_id: int):
    petition = await fetchrow("""SELECT * FROM petitions WHERE petition_id = $1""",petition_id)
    if petition is None:
        return None
    return petition
