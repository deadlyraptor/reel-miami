"""Initialize the database

Revision ID: eeba71363d2d
Revises:
Create Date: 2019-04-29 21:02:08.743674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eeba71363d2d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('venues',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('address1', sa.String(), nullable=False),
                    sa.Column('address2', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('postal_code', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('venue_photo', sa.String(length=20),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('films',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('running_time', sa.String(), nullable=False),
                    sa.Column('director', sa.String(), nullable=False),
                    sa.Column('year', sa.String(), nullable=False),
                    sa.Column('venue_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('showtimes',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('date', sa.String(), nullable=False),
                    sa.Column('time', sa.String(), nullable=False),
                    sa.Column('ticketing_link', sa.String(), nullable=False),
                    sa.Column('film_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['film_id'], ['films.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('showtimes')
    op.drop_table('films')
    op.drop_table('venues')
    # ### end Alembic commands ###
