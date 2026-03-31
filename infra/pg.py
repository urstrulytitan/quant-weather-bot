import os, asyncpg

_pg_dsn = os.getenv("PG_DSN", "postgresql://quant:quant@localhost:5432/quant")

async def pg_log(table: str, row: dict):
    cols = ",".join(row.keys())
    placeholders = ",".join(f"${i+1}" for i in range(len(row)))
    values = list(row.values())
    sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders});"
    conn = await asyncpg.connect(_pg_dsn)
    try:
        await conn.execute(sql, *values)
    finally:
        await conn.close()