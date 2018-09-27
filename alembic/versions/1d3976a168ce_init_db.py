"""init db

Revision ID: 1d3976a168ce
Revises: 
Create Date: 2018-09-27 17:25:58.954592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d3976a168ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bookmark',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP()'), nullable=True),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP() on update CURRENT_TIMESTAMP()'), nullable=True),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('url', sa.VARCHAR(length=256), nullable=False),
    sa.Column('type', sa.VARCHAR(length=32), nullable=False),
    sa.Column('creator', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_bookmark_creator'), 'bookmark', ['creator'], unique=False)
    op.create_index(op.f('ix_bookmark_name'), 'bookmark', ['name'], unique=False)
    op.create_index(op.f('ix_bookmark_url'), 'bookmark', ['url'], unique=False)
    op.create_table('demo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP()'), nullable=True),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP() on update CURRENT_TIMESTAMP()'), nullable=True),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    mysql_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP()'), nullable=True),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP() on update CURRENT_TIMESTAMP()'), nullable=True),
    sa.Column('title', sa.VARCHAR(length=100), nullable=False),
    sa.Column('author', sa.VARCHAR(length=50), nullable=False),
    sa.Column('tag', sa.VARCHAR(length=32), nullable=True),
    sa.Column('intro', sa.VARCHAR(length=300), nullable=True),
    sa.Column('content', sa.TEXT(), nullable=True),
    sa.Column('format', sa.VARCHAR(length=10), nullable=True),
    sa.Column('source', sa.VARCHAR(length=10), nullable=True),
    sa.Column('source_id', sa.VARCHAR(length=64), nullable=True),
    sa.Column('original_url', sa.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('upload',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP()'), nullable=True),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP() on update CURRENT_TIMESTAMP()'), nullable=True),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('new_name', sa.VARCHAR(length=100), nullable=True),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('content_type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('url', sa.VARCHAR(length=120), nullable=False),
    sa.Column('upload_dir', sa.CHAR(length=4), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url'),
    mysql_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP()'), nullable=True),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP() on update CURRENT_TIMESTAMP()'), nullable=True),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('email', sa.VARCHAR(length=50), nullable=False),
    sa.Column('mobile', sa.VARCHAR(length=20), nullable=True),
    sa.Column('password', sa.CHAR(length=64), nullable=False),
    sa.Column('salt', sa.CHAR(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name'),
    mysql_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('upload')
    op.drop_table('post')
    op.drop_table('demo')
    op.drop_index(op.f('ix_bookmark_url'), table_name='bookmark')
    op.drop_index(op.f('ix_bookmark_name'), table_name='bookmark')
    op.drop_index(op.f('ix_bookmark_creator'), table_name='bookmark')
    op.drop_table('bookmark')
    # ### end Alembic commands ###