from database.db import execute,fetchrow,fetch
from database.user_queries import get_user_by_tg_id

async def create_petition(tg_id: int, petition_text: str):
    user = await get_user_by_tg_id(tg_id=tg_id)
    await execute("""INSERT INTO petitions (user_id, petition_text) VALUES ($1,$2)""",user['user_id'],petition_text)
    petition = await fetchrow("""SELECT * FROM petitions WHERE user_id = $1 ORDER BY created_at DESC LIMIT 1""",user['user_id'])
    await execute("""INSERT INTO users_petitions (user_id, petition_id) VALUES ($1,$2)""",user['user_id'], petition['petition_id'])


async def get_all_petitions_by_tg_id(tg_id: int):
    user = await get_user_by_tg_id(tg_id=tg_id)
    all_petitions_by_user = await fetch("""SELECT * FROM users_petitions WHERE user_id = $1 ORDER BY petition_id DESC""",user['user_id'])
    if all_petitions_by_user is None:
        return None
    return all_petitions_by_user

async def get_data_by_petition(petition_id: int):
    petition = await fetchrow("""SELECT * FROM petitions WHERE petition_id = $1""",petition_id)
    if petition is None:
        return None
    return petition
