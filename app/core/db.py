from sqlalchemy import create_engine, Column, String, Float, Integer, Table, MetaData
from databases import Database

DATABASE_URL = "sqlite:///uptime_monitor.db"

database = Database(DATABASE_URL)
metadata = MetaData()

logs_table = Table(
    "logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("url", String),
    Column("status", String),
    Column("latency", Float),
    Column("timestamp", Float)
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

# async function to save a log
async def save_log(log):
    query = logs_table.insert().values(**log)
    await database.execute(query)

# async function to fetch last N logs
async def fetch_logs(limit=20):
    query = logs_table.select().order_by(logs_table.c.id.desc()).limit(limit)
    return await database.fetch_all(query)
