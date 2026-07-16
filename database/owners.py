from database.db import execute
from database.admins import get_level

async def set_user_role(user_id: int, role_id: int):
    await execute("""INSERT INTO users_roles(user_id, role_id) VALUES ($1,$2)""",user_id,role_id)

async def set_admin(user_id: int):
    user_level = await get_level(user_id=user_id)
    if user_level == 2:
        return None
    await set_user_role(user_id=user_id, role_id=2)

async def del_admin(user_id: int):
    await execute("""DELETE FROM users_roles WHERE user_id = $1 and role_id = $2""",user_id,2)

async def create_product(name: str, description: str, price: int, in_stock: int):
    await execute("""INSERT INTO products(name,description,price,in_stock) VALUES($1,$2,$3,$4)""",name,description,price,in_stock)