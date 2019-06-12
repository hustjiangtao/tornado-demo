"""init db

Revision ID: 72e4bb853d04
Revises: 
Create Date: 2019-06-12 17:53:41.680708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72e4bb853d04'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('demo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    mysql_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('email', sa.VARCHAR(length=50), nullable=False),
    sa.Column('mobile', sa.VARCHAR(length=20), nullable=True),
    sa.Column('password', sa.CHAR(length=64), nullable=False),
    sa.Column('salt', sa.CHAR(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name'),
    mysql_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('demo')
    # ### end Alembic commands ###