try:
    from database.connection import DATABASE_URL, engine, get_session, init_db
except ModuleNotFoundError:
    from backend.database.connection import DATABASE_URL, engine, get_session, init_db

__all__ = ["DATABASE_URL", "engine", "get_session", "init_db"]