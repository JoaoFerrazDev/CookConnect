"""empty message

Revision ID: 9f912751650d
Revises: 
Create Date: 2024-06-13 21:24:30.304713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f912751650d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('encomenda',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('utilizadorId', sa.Integer(), nullable=True),
    sa.Column('aberta', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('encomenda_linha',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('encomendaId', sa.Integer(), nullable=True),
    sa.Column('artigoId', sa.Integer(), nullable=True),
    sa.Column('quantidade', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['encomendaId'], ['encomenda.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('encomenda_linha')
    op.drop_table('encomenda')
    # ### end Alembic commands ###
