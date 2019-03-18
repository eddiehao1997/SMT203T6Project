"""empty message

Revision ID: f7c0a050d48a
Revises: 
Create Date: 2019-03-16 18:36:02.215451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7c0a050d48a'
down_revision = None
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
    op.create_table('sensor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.String(), nullable=False),
    sa.Column('sensor_type', sa.String(), nullable=False),
    sa.Column('deployment_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('sensor_id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.String(length=10), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('modified_timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('chat_id')
    )
    op.create_table('motion_sensor_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.String(), nullable=False),
    sa.Column('timestamp', sa.String(), nullable=False),
    sa.Column('sensor_figure', sa.Integer(), nullable=False),
    sa.Column('status_conclusion', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensor.sensor_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('machine_id', sa.String(), nullable=False),
    sa.Column('start_timestamp', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['machine_id'], ['machine.machine_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_input',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.String(), nullable=False),
    sa.Column('service_type', sa.String(), nullable=False),
    sa.Column('input_timestamp', sa.DateTime(), nullable=False),
    sa.Column('receive_timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['user.chat_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vibration_sensor_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.String(), nullable=False),
    sa.Column('timestamp', sa.String(), nullable=False),
    sa.Column('sensor_figure', sa.Integer(), nullable=False),
    sa.Column('status_conclusion', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensor.sensor_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prompt',
    sa.Column('chat_id', sa.String(), nullable=False),
    sa.Column('usage_id', sa.Integer(), nullable=False),
    sa.Column('machine_id', sa.String(), nullable=False),
    sa.Column('start_timestamp', sa.DateTime(), nullable=False),
    sa.Column('time_to_prompt', sa.DateTime(), nullable=True),
    sa.Column('ending_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['user.chat_id'], ),
    sa.ForeignKeyConstraint(['usage_id'], ['usage.id'], ),
    sa.PrimaryKeyConstraint('chat_id', 'usage_id'),
    sa.UniqueConstraint('usage_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prompt')
    op.drop_table('vibration_sensor_data')
    op.drop_table('user_input')
    op.drop_table('usage')
    op.drop_table('motion_sensor_data')
    op.drop_table('user')
    op.drop_table('sensor')
    op.drop_table('machine')
    # ### end Alembic commands ###
