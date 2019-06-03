"""Rename Users and Roles tables

Revision ID: 97bc6186c9fd
Revises: 0a7918f12a6d
Create Date: 2019-06-01 23:08:31.241546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97bc6186c9fd'
down_revision = '0a7918f12a6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles_users')
    op.create_table('roles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=80), nullable=True),
                    sa.Column('description', sa.String(length=255),
                              nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(length=255), nullable=True),
                    sa.Column('password', sa.String(length=255),
                              nullable=True),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    op.create_table('roles_users',
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('role_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
                    )
    op.drop_table('role')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('email', sa.VARCHAR(length=255), nullable=True),
                    sa.Column('password', sa.VARCHAR(length=255),
                              nullable=True),
                    sa.Column('active', sa.BOOLEAN(), nullable=True),
                    sa.Column('confirmed_at', sa.DATETIME(), nullable=True),
                    sa.CheckConstraint('active IN (0, 1)'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    op.create_table('role',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('name', sa.VARCHAR(length=80), nullable=True),
                    sa.Column('description', sa.VARCHAR(length=255),
                              nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('roles_users',
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('role_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
                    )
    op.drop_table('role')
    op.drop_table('user')
    op.drop_table('roles_users')
    # ### end Alembic commands ###