from database.db import fetchrow,execute,fetchval,fetch

async def get_level(user_id: int):
    from database.owners import set_user_role
    level = await fetchrow("""SELECT role_id FROM users_roles WHERE user_id=$1 ORDER BY role_id DESC LIMIT 1""", user_id)
    if level is None:
        await set_user_role(user_id=user_id, role_id=1)
        return 1
    return level['role_id']

async def find_user_id_by_tg_id(tg_id: int):
    user = await fetchrow("""SELECT user_id FROM users WHERE tg_id = $1""",tg_id)
    if user is None:
        return None
    return user['user_id']

async def is_admin(tg_id: int):
    user_id = await find_user_id_by_tg_id(tg_id=tg_id)
    if user_id is None:
        return False
    else:
        role_id = await get_level(user_id=user_id)
        if role_id >= 2:
            return True
        return False
        
async def is_owner(tg_id: int):
    user_id = await find_user_id_by_tg_id(tg_id=tg_id)
    if user_id is None:
        return False
    else:
        role_id = await get_level(user_id=user_id)
        if role_id == 3:
            return True
        return False
