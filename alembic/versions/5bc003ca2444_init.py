from alembic import op
import sqlalchemy as sa

revision = "5bc003ca2444"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
    )

    op.create_table(
        "products",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("price", sa.Float, nullable=False),
    )

def downgrade() -> None:
    op.drop_table("products")
    op.drop_table("users")
