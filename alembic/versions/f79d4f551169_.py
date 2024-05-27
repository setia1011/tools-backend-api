"""empty message

Revision ID: f79d4f551169
Revises: 
Create Date: 2024-05-25 16:57:59.164968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f79d4f551169'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cedict',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('traditional', sa.VARCHAR(length=500), nullable=True),
    sa.Column('simplified', sa.VARCHAR(length=500), nullable=True),
    sa.Column('pinyin', sa.VARCHAR(length=500), nullable=True),
    sa.Column('english', sa.TEXT(), nullable=True),
    sa.Column('audio_normal', sa.VARCHAR(length=500), nullable=True),
    sa.Column('audio_slow', sa.VARCHAR(length=500), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NULL ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cedict_audio_normal'), 'cedict', ['audio_normal'], unique=False)
    op.create_index(op.f('ix_cedict_audio_slow'), 'cedict', ['audio_slow'], unique=False)
    op.create_index(op.f('ix_cedict_id'), 'cedict', ['id'], unique=False)
    op.create_index(op.f('ix_cedict_pinyin'), 'cedict', ['pinyin'], unique=False)
    op.create_index(op.f('ix_cedict_simplified'), 'cedict', ['simplified'], unique=False)
    op.create_index(op.f('ix_cedict_traditional'), 'cedict', ['traditional'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_cedict_traditional'), table_name='cedict')
    op.drop_index(op.f('ix_cedict_simplified'), table_name='cedict')
    op.drop_index(op.f('ix_cedict_pinyin'), table_name='cedict')
    op.drop_index(op.f('ix_cedict_id'), table_name='cedict')
    op.drop_index(op.f('ix_cedict_audio_slow'), table_name='cedict')
    op.drop_index(op.f('ix_cedict_audio_normal'), table_name='cedict')
    op.drop_table('cedict')
    # ### end Alembic commands ###
