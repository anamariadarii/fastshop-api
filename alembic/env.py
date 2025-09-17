from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine
from alembic import context

# === Importă modelele pentru a avea metadata ===
from app.db import Base
import app.models  # <-- ai grijă să imporți modelele aici

# Această variabilă este folosită de Alembic pentru autogenerate
target_metadata = Base.metadata

# Obține configurația Alembic
config = context.config

# Încarcă logging din alembic.ini, dacă există
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Citim URL-ul DB din ENV (folosim psycopg pentru Alembic)
DB_SYNC_URL = (
    os.getenv("ALEMBIC_DATABASE_URL")
    or os.getenv("DATABASE_SYNC_URL")
    or "postgresql+psycopg://postgres:admin@db:5432/fastshop"
)
config.set_main_option("sqlalchemy.url", DB_SYNC_URL)


def run_migrations_offline():
    """Rulăm migrațiile în mod 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Rulăm migrațiile în mod 'online' (cu engine real)."""
    connectable = create_engine(DB_SYNC_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
