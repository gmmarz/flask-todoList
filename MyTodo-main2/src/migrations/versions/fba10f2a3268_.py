"""empty message

Revision ID: fba10f2a3268
Revises: 
Create Date: 2024-03-09 18:05:32.748303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fba10f2a3268'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tarefas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=255), nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=False),
    sa.Column('data_inicio', sa.Date(), nullable=False),
    sa.Column('data_conclusao', sa.Date(), nullable=True),
    sa.Column('concluida', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tarefas')
    # ### end Alembic commands ###
