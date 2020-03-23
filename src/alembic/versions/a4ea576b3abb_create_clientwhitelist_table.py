"""create clientwhitelist table

Revision ID: a4ea576b3abb
Revises: 
Create Date: 2020-03-17 12:02:41.378038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4ea576b3abb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'client_whitelist',
        sa.Column('id_regex', sa.Integer, primary_key=True),
        sa.Column('client', sa.String(50), nullable=False),
        sa.Column('regex', sa.Unicode(200), nullable=False),
    )


def downgrade():
    op.drop_table('client_whitelist')
