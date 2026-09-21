from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.config.settings import get_settings

settings = get_settings()
is_sqlite = settings.database_url.startswith("sqlite")
is_memory = settings.database_url == "sqlite://"

connect_args = {"check_same_thread": False} if is_sqlite else {}
poolclass = StaticPool if is_memory else None

engine = create_engine(
    settings.database_url,
    pool_pre_ping=not is_memory,
    connect_args=connect_args,
    poolclass=poolclass,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
