# app/database.py

from sqlmodel import create_engine, SQLModel, Session

# Define the database URL. For now, we use a local SQLite file.
# The database will be created as 'pyflow.db' in the project root.
DATABASE_URL = "sqlite:///pyflow.db"

# The engine is the central access point to the database.
# connect_args is needed only for SQLite to allow it to be used by multiple threads.
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """
    Initializes the database and creates all tables based on SQLModel models.
    This function should be called once when the application starts.
    """
    SQLModel.metadata.create_all(engine)

# Dependency function to get a database session for each request.
# We use `yield` to ensure the session is always closed, even if errors occur.
def get_session():
    with Session(engine) as session:
        yield session