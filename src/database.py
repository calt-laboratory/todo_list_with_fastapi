import databases
import sqlalchemy

DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)

# Metadata contains definitions of tables and associated objects such as index, view, triggers, etc.
# Hence, an object of MetaData class from SQLAlchemy is a collection of Table objects and their associated schema
# constructs.
metadata = sqlalchemy.MetaData()

# Database table schema
todos = sqlalchemy.Table(
    "todos",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("item", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

metadata.create_all(engine)
