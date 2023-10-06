"""Update users table

Revision ID: 19dec93a1188
Revises: 8076b51bffa5
Create Date: 2023-10-06 17:44:29.892784

"""
from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '19dec93a1188'
down_revision = '8076b51bffa5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'created',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('users', 'updated',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(length=72),
               type_=sa.String(length=1024),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hashed_password',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=72),
               existing_nullable=False)
    op.alter_column('users', 'updated',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('users', 'created',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('now()'))
    # ### end Alembic commands ###
