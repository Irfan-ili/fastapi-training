from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on:    Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ── users (must be created BEFORE items — foreign key) ────
    op.create_table(
        "users",
        sa.Column("id",              sa.Integer(),    nullable=False),
        sa.Column("username",        sa.String(50),   nullable=False),
        sa.Column("email",           sa.String(100),  nullable=False),
        sa.Column("hashed_password", sa.String(255),  nullable=False),
        sa.Column("role",            sa.String(20),   server_default="user"),
        sa.Column("is_active",       sa.Boolean(),    server_default="true"),
        sa.Column("created_at",      sa.DateTime(),   server_default=sa.func.now()),
        sa.Column("updated_at",      sa.DateTime(),   nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_id",       "users", ["id"])
    op.create_index("ix_users_username", "users", ["username"])
    op.create_index("ix_users_email",    "users", ["email"])

    # ── items ─────────────────────────────────────────────────
    op.create_table(
        "items",
        sa.Column("id",         sa.Integer(),  nullable=False),
        sa.Column("name",       sa.String(100), nullable=False),
        sa.Column("price",      sa.Float(),     nullable=False),
        sa.Column("owner_id",   sa.Integer(),   nullable=False),
        sa.Column("created_at", sa.DateTime(),  server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(),  nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_items_id", "items", ["id"])


def downgrade() -> None:
    op.drop_table("items")
    op.drop_table("users")
