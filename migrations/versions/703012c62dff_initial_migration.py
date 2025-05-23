"""Initial Migration

Revision ID: 703012c62dff
Revises: 
Create Date: 2025-05-15 05:11:35.374161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '703012c62dff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('month', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('month')

    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=200), nullable=False),
    sa.Column('email', sa.VARCHAR(length=200), nullable=False),
    sa.Column('date_added', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###
