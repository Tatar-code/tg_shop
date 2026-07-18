import asyncio
import asyncpg

pool = None

async def set_pool(dsn):
    global pool
    pool = await asyncpg.create_pool(
        dsn=dsn,
        min_size=3,
        max_size=10,
        max_inactive_connection_lifetime=300)
    
async def get_pool():
    if pool is None:
        print('Пул закрыт')
    else:
        return pool
    
async def close_pool():
    if pool is None:
        print('Пул закрыт')
    else:
        await pool.close()
    
async def fetch(sql,*args):
    async with pool.acquire() as conn:
        return await conn.fetch(sql, *args)
    
async def fetchrow(sql,*args):
    async with pool.acquire() as conn:
        return await conn.fetchrow(sql,*args)

async def fetchval(sql,*args):
    async with pool.acquire() as conn:
        return await conn.fetchval(sql,*args)

async def execute(sql,*args):
    async with pool.acquire() as conn:
        return await conn.execute(sql,*args)

async def create_database():
    await set_pool(dsn='postgresql://postgres:123123@localhost:5432/tgshop')

    await execute("""
                CREATE TABLE IF NOT EXISTS users (
                user_id serial primary key,
                tg_id bigint not null unique,
                username varchar(128),
                user_cart integer,
                adress text,
                contact varchar(32) unique
                )
                  """)
    
    await execute("""
                CREATE TABLE IF NOT EXISTS roles (
                role_id serial primary key,
                role_name varchar(64) unique not null,
                role_level integer unique not null
                )
                  """)
    
    await execute("""
                CREATE TABLE IF NOT EXISTS users_roles (
                user_id integer references users(user_id) ON DELETE CASCADE,
                role_id integer references roles(role_id) ON DELETE CASCADE,
                PRIMARY KEY (user_id, role_id)
                )
                  """)
    
    await execute("""
                CREATE TABLE IF NOT EXISTS categories (
                category_id serial primary key,
                category_name varchar(128) not null unique)
                  """)
    
    await execute("""
                CREATE TABLE IF NOT EXISTS products (
                product_id serial primary key,
                name text not null,
                description text,
                price integer not null,
                in_stock smallint not null,
                category_id smallint references categories(category_id) ON DELETE CASCADE,
                photo_file_id varchar(256),
                reviews smallint default 0)
                """)
    
    await execute("""
                CREATE TABLE IF NOT EXISTS carts (
                cart_id serial primary key,
                user_id integer references users(user_id) ON DELETE CASCADE,
                cart_summary integer not null default 0)
                """)
    
    await execute("""CREATE TABLE IF NOT EXISTS carts_products (
                cart_id integer references carts(cart_id) ON DELETE CASCADE,
                product_id integer references products(product_id) ON DELETE CASCADE,
                PRIMARY KEY (cart_id, product_id))
                """)
    
    await execute("""
                CREATE TABLE IF NOT EXISTS petitions (
                petition_id serial primary key,
                user_id integer references users(user_id) ON DELETE CASCADE,
                petition_text text not null,
                created_at timestamp default current_timestamp,
                is_actual boolean default true)
                  """)
    
    await execute("""
                CREATE TABLE IF NOT EXISTS users_petitions (
                user_id integer references users(user_id) ON DELETE CASCADE,
                petition_id integer references petitions(petition_id) ON DELETE CASCADE,
                PRIMARY KEY(user_id, petition_id)
                )""")
    
    await close_pool()

if __name__ == '__main__':
    asyncio.run(create_database())