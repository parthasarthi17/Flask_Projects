"""Initial migration.

Revision ID: 1cd5822d09ba
Revises: 
Create Date: 2021-12-01 17:59:25.090966

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1cd5822d09ba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('book', table_name='authors')
    op.drop_index('name', table_name='authors')
    op.drop_table('authors')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('public_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('password', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('admin', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('authors',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('book', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('country', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('booker_prize', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('name', 'authors', ['name'], unique=False)
    op.create_index('book', 'authors', ['book'], unique=False)
    # ### end Alembic commands ###
