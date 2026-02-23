"""create member table

Revision ID: 001
Revises:
Create Date: 2026-02-23
"""

from alembic import op
import sqlalchemy as sa
from fastapi_ddd.domain.custom_types.entity_id_type import EntityIdType

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "member",
        sa.Column("mem_id", EntityIdType(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("passwd", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("mem_id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_member_mem_id"), "member", ["mem_id"])


def downgrade() -> None:
    op.drop_index(op.f("ix_member_mem_id"), table_name="member")
    op.drop_table("member")
