"""update places columns

Revision ID: 9d5e76952f93
Revises: 5f3049ad887d
Create Date: 2026-11-25 16:51:31.183748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d5e76952f93'
down_revision: Union[str, Sequence[str], None] = '5f3049ad887d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Fill empty categories first, so the column can become required
    op.execute(
        "UPDATE places SET category = 'other' "
        "WHERE category IS NULL OR category = ''"
    )

    op.add_column('places', sa.Column('last_synced_at', sa.DateTime(timezone=True), nullable=True))
    op.alter_column('places', 'category',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('places', 'good_for_children',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('places', 'good_for_groups',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.create_index(op.f('ix_places_category'), 'places', ['category'], unique=False)
    op.drop_column('places', 'estimated_duration_minutes')
    op.drop_column('places', 'weather_sensitivity')
    op.drop_column('places', 'indoor_outdoor')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('places', sa.Column('indoor_outdoor', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
    op.add_column('places', sa.Column('weather_sensitivity', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
    op.add_column('places', sa.Column('estimated_duration_minutes', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_places_category'), table_name='places')

    # Booleans become required again, so fill empty values first
    op.execute(
        "UPDATE places SET good_for_children = false "
        "WHERE good_for_children IS NULL"
    )
    op.execute(
        "UPDATE places SET good_for_groups = false "
        "WHERE good_for_groups IS NULL"
    )

    op.alter_column('places', 'good_for_groups',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('places', 'good_for_children',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('places', 'category',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.drop_column('places', 'last_synced_at')