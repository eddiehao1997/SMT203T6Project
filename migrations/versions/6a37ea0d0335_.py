"""empty message

Revision ID: 6a37ea0d0335
Revises: 43d257ed4612
Create Date: 2019-03-19 10:22:00.595036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a37ea0d0335'
down_revision = '43d257ed4612'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('machine_id', sa.String(), nullable=False),
    sa.Column('start_timestamp', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['machine_id'], ['machine.machine_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usage')
    # ### end Alembic commands ###
