"""Initial migration.

Revision ID: a29e6e23880c
Revises: 
Create Date: 2024-06-23 20:17:58.632997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a29e6e23880c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artigo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=False),
    sa.Column('codigoArtigo', sa.String(length=21), nullable=False),
    sa.Column('preco', sa.Float(), nullable=True),
    sa.Column('imagem', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('codigoArtigo'),
    sa.UniqueConstraint('descricao')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('artigo')
    # ### end Alembic commands ###