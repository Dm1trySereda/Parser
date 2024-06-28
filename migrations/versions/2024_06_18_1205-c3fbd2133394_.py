"""empty message

Revision ID: c3fbd2133394
Revises: 
Create Date: 2024-06-18 12:05:40.125938

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c3fbd2133394"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("book_num", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("author", sa.String(length=255), nullable=False),
        sa.Column("price_new", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("price_old", sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column("discount", sa.String(length=20), nullable=True),
        sa.Column("rating", sa.DECIMAL(precision=4, scale=2), nullable=True),
        sa.Column("image", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("book_num"),
    )
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "history",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("book_num", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("price", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=255), nullable=True),
        sa.Column("hashed_password", sa.String(length=1024), nullable=True),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_table(
        "auth_provider_users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("provider", sa.String(length=255), nullable=False),
        sa.Column("remote_user_id", sa.String(length=255), nullable=True),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("remote_user_id"),
    )
    op.create_index(
        op.f("ix_auth_provider_users_email"),
        "auth_provider_users",
        ["email"],
        unique=True,
    )
    op.execute(
        "INSERT INTO roles (name, title, description) VALUES ('admin', 'Administrator', 'User with all permissions')"
    )
    op.execute(
        "INSERT INTO roles (name, title, description) VALUES ('subadmin', 'Sub-Administrator', 'User with sub-permissions')"
    )
    op.execute(
        "INSERT INTO roles (name, title, description) VALUES ('client', 'Client', 'Regular user without admin permissions')"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_auth_provider_users_email"), table_name="auth_provider_users"
    )
    op.drop_table("auth_provider_users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_table("history")
    op.drop_table("roles")
    op.drop_table("books")
    # ### end Alembic commands ###
