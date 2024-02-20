from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)

# Metadata contains definitions of tables and associated objects such as index, view, triggers, etc.
# Hence, an object of MetaData class from SQLAlchemy is a collection of Table objects and their associated schema
# constructs.
metadata = MetaData()

# Database table schema
Base = declarative_base()

todo_table_schema = Table(
    "todos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("item", String),
    Column("completed", Boolean),
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
