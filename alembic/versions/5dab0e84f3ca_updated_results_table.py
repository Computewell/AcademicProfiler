"""updated results table

Revision ID: 5dab0e84f3ca
Revises: ee25f27a6c93
Create Date: 2023-03-20 05:24:08.203196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5dab0e84f3ca'
down_revision = 'ee25f27a6c93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('results', sa.Column('session', sa.String(), nullable=False))
    op.drop_column('results', 'year')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('results', sa.Column('year', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('results', 'session')
    # ### end Alembic commands ###
