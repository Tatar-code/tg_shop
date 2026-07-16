from database.db import fetch,fetchrow,execute
from database.owners import set_user_role
from database.admins import find_user_id_by_tg_id
    


async def create_user(tg_id: int, username: str):
    user = await fetchrow("""SELECT * FROM users WHERE tg_id = $1""",tg_id)
    if user is None:
        await execute("""INSERT INTO users (tg_id,username) VALUES ($1,$2)""",tg_id,username)
        user = await find_user_id_by_tg_id(tg_id=tg_id)
        await set_user_role(user_id=user,role_id=1)
    else:
        return False
    return True