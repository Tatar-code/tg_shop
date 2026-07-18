from database.db import fetchrow,execute
from database.user_queries import get_user_by_tg_id

async def set_user_role(user_id: int, role_id: int):
    await execute("""INSERT INTO users_roles(user_id, role_id) VALUES ($1,$2)""",user_id,role_id)

async def del_user_role(user_id: int, role_id: int):
     await execute("""DELETE FROM users_roles WHERE user_id = $1 and role_id = $2""",user_id,role_id)

async def get_level(user_id: int):
    level = await fetchrow("""SELECT role_id FROM users_roles WHERE user_id=$1 ORDER BY role_id DESC LIMIT 1""", user_id)
    if level is None:
        await set_user_role(user_id=user_id, role_id=1)
        return 1
    return level['role_id']


async def is_admin(tg_id: int):
    user = await get_user_by_tg_id(tg_id=tg_id)
    if user is None:
        return False
    else:
        role_id = await get_level(user_id=user['user_id'])
        if role_id >= 2:
            return True
        return False
        
async def is_owner(tg_id: int):
    user = await get_user_by_tg_id(tg_id=tg_id)
    if user is None:
        return False
    else:
        role_id = await get_level(user_id=user['user_id'])
        if role_id == 3:
            return True
        return False

async def set_admin(user_id: int):
    await set_user_role(user_id=user_id, role_id=2)

async def del_admin(user_id: int):
    await del_user_role(user_id=user_id, role_id=2)