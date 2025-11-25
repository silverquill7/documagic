"""create documents table

Revision ID: 0001_create_documents
Revises: 
Create Date: 2025-11-21 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_documents'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('source', sa.String(length=128), nullable=True),
        sa.Column('sender', sa.String(length=255), nullable=True),
        sa.Column('received_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('storage_path', sa.String(length=1024), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('parsed_json', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
    )

def downgrade():
    op.drop_table('documents')
