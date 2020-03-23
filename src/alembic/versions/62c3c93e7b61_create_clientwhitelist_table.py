"""create globalwhitelist table

Revision ID: 62c3c93e7b61
Revises: a4ea576b3abb
Create Date: 2020-03-17 12:05:37.338415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62c3c93e7b61'
down_revision = 'a4ea576b3abb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'global_whitelist',
        sa.Column('id_regex', sa.Integer, primary_key=True),
        sa.Column('regex', sa.Unicode(200), nullable=False),
    )


def downgrade():
    op.drop_table('global_whitelist')
