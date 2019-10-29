"""empty message

Revision ID: 358c18d89660
Revises: 
Create Date: 2019-10-17 07:35:31.542909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '358c18d89660'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('control',
    sa.Column('control_id', sa.Integer(), nullable=False),
    sa.Column('control_name', sa.String(length=60), nullable=False),
    sa.Column('control_description', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('control_id'),
    sa.UniqueConstraint('control_id'),
    sa.UniqueConstraint('control_name'),
    schema='mc_demo'
    )
    op.create_table('recipe',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('recipe_name', sa.String(length=60), nullable=False),
    sa.Column('recipe_description', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('recipe_id'),
    sa.UniqueConstraint('recipe_id'),
    sa.UniqueConstraint('recipe_name'),
    schema='mc_demo'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe', schema='mc_demo')
    op.drop_table('control', schema='mc_demo')
    # ### end Alembic commands ###
