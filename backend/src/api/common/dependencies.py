from src.database.sqlite.handler import SQLiteHandler


async def get_database_dependency() -> SQLiteHandler:
    db_handler = SQLiteHandler()
    return db_handler
