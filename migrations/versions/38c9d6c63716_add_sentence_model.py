"""Add Sentence model

Revision ID: 38c9d6c63716
Revises: d1465f8aaaa0
Create Date: 2025-07-14 19:26:32.024390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38c9d6c63716'
down_revision = 'd1465f8aaaa0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sentence',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text_en', sa.String(length=255), nullable=False),
    sa.Column('text_es', sa.String(length=255), nullable=False),
    sa.Column('audio_url', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sentence')
    # ### end Alembic commands ###
