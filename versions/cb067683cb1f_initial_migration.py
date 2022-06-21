"""Initial migration.

Revision ID: cb067683cb1f
Revises: 1cd5822d09ba
Create Date: 2021-12-01 18:00:20.101321

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cb067683cb1f'
down_revision = '1cd5822d09ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_index('Author', table_name='books')
    op.drop_index('name', table_name='books')
    op.drop_table('books')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('Author', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('Publisher', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('book_prize', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='books_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('name', 'books', ['name'], unique=False)
    op.create_index('Author', 'books', ['Author'], unique=False)
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
    # ### end Alembic commands ###
