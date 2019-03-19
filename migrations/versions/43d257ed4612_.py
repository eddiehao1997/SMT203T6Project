"""empty message

Revision ID: 43d257ed4612
Revises: 2680916f751e
Create Date: 2019-03-19 10:21:25.928160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43d257ed4612'
down_revision = '2680916f751e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('machine',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('machine_id', sa.String(), nullable=False),
    sa.Column('machine_type', sa.String(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('machine_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('machine')
    # ### end Alembic commands ###