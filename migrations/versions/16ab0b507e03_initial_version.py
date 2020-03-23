"""initial version

Revision ID: 16ab0b507e03
Revises:
Create Date: 2019-01-09 10:44:18.137854

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '16ab0b507e03'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'transactions',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('account_number', sa.String(50)),
        sa.Column('amount', sa.Integer())
    )


def downgrade():
    op.drop_table('transactions')
