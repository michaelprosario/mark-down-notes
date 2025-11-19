"""initial_schema

Revision ID: 4e7e79a1f193
Revises: 
Create Date: 2025-11-19 04:45:17.834390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4e7e79a1f193'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - create all tables with indexes, constraints, and triggers."""
    
    # Determine if we're using PostgreSQL or SQLite
    bind = op.get_bind()
    is_postgres = bind.dialect.name == 'postgresql'
    
    # UUID type - use native UUID for PostgreSQL, String for SQLite
    uuid_type = postgresql.UUID(as_uuid=True) if is_postgres else sa.String(36)
    uuid_default = sa.text('gen_random_uuid()') if is_postgres else sa.text('(lower(hex(randomblob(4))) || \'-\' || lower(hex(randomblob(2))) || \'-4\' || substr(lower(hex(randomblob(2))),2) || \'-\' || substr(\'89ab\',abs(random()) % 4 + 1, 1) || substr(lower(hex(randomblob(2))),2) || \'-\' || lower(hex(randomblob(6))))')
    
    # Create notebooks table
    op.create_table(
        'notebooks',
        sa.Column('id', uuid_type, primary_key=True, server_default=uuid_default),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('color', sa.String(7), nullable=False, server_default='#0078D4'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('idx_notebooks_created_at', 'notebooks', ['created_at'])
    op.create_index('idx_notebooks_deleted_at', 'notebooks', ['deleted_at'])

    # Create sections table
    op.create_table(
        'sections',
        sa.Column('id', uuid_type, primary_key=True, server_default=uuid_default),
        sa.Column('notebook_id', uuid_type, nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('display_order', sa.Integer, nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['notebook_id'], ['notebooks.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_sections_notebook_id', 'sections', ['notebook_id'])
    op.create_index('idx_sections_notebook_order', 'sections', ['notebook_id', 'display_order'])
    op.create_index('idx_sections_deleted_at', 'sections', ['deleted_at'])

    # Create pages table
    op.create_table(
        'pages',
        sa.Column('id', uuid_type, primary_key=True, server_default=uuid_default),
        sa.Column('section_id', uuid_type, nullable=False),
        sa.Column('parent_page_id', uuid_type, nullable=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text, nullable=False, server_default=''),
        sa.Column('content_plain', sa.Text, nullable=False, server_default=''),
        sa.Column('search_vector', sa.Text if not is_postgres else postgresql.TSVECTOR, nullable=True),
        sa.Column('display_order', sa.Integer, nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_page_id'], ['pages.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_pages_section_id', 'pages', ['section_id'])
    op.create_index('idx_pages_parent_page_id', 'pages', ['parent_page_id'])
    op.create_index('idx_pages_section_order', 'pages', ['section_id', 'display_order'])
    if is_postgres:
        op.create_index('idx_pages_search_vector', 'pages', ['search_vector'], postgresql_using='gin')
    op.create_index('idx_pages_updated_at', 'pages', ['updated_at'])
    op.create_index('idx_pages_deleted_at', 'pages', ['deleted_at'])

    # Create tags table
    op.create_table(
        'tags',
        sa.Column('id', uuid_type, primary_key=True, server_default=uuid_default),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('color', sa.String(7), nullable=False, server_default='#6C757D'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    # Create page_tags join table
    op.create_table(
        'page_tags',
        sa.Column('page_id', uuid_type, nullable=False),
        sa.Column('tag_id', uuid_type, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['page_id'], ['pages.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('page_id', 'tag_id'),
    )
    op.create_index('idx_page_tags_tag_id', 'page_tags', ['tag_id'])
    op.create_index('idx_page_tags_page_id', 'page_tags', ['page_id'])

    # PostgreSQL-specific features (triggers, full-text search)
    if is_postgres:
        # Create trigger function for updating updated_at
        op.execute("""
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = NOW();
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)

        # Create triggers for updated_at auto-update
        op.execute("""
            CREATE TRIGGER update_notebooks_updated_at 
            BEFORE UPDATE ON notebooks
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """)
        
        op.execute("""
            CREATE TRIGGER update_sections_updated_at 
            BEFORE UPDATE ON sections
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """)
        
        op.execute("""
            CREATE TRIGGER update_pages_updated_at 
            BEFORE UPDATE ON pages
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """)
        
        op.execute("""
            CREATE TRIGGER update_tags_updated_at 
            BEFORE UPDATE ON tags
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """)

        # Create trigger for auto-updating search_vector
        op.execute("""
            CREATE TRIGGER pages_search_vector_update
            BEFORE INSERT OR UPDATE OF title, content_plain ON pages
            FOR EACH ROW EXECUTE FUNCTION
            tsvector_update_trigger(search_vector, 'pg_catalog.english', title, content_plain);
        """)


def downgrade() -> None:
    """Downgrade schema - drop all tables, triggers, and functions."""
    
    # Determine if we're using PostgreSQL
    bind = op.get_bind()
    is_postgres = bind.dialect.name == 'postgresql'
    
    # Drop triggers first (PostgreSQL only)
    if is_postgres:
        op.execute('DROP TRIGGER IF EXISTS pages_search_vector_update ON pages;')
        op.execute('DROP TRIGGER IF EXISTS update_tags_updated_at ON tags;')
        op.execute('DROP TRIGGER IF EXISTS update_pages_updated_at ON pages;')
        op.execute('DROP TRIGGER IF EXISTS update_sections_updated_at ON sections;')
        op.execute('DROP TRIGGER IF EXISTS update_notebooks_updated_at ON notebooks;')
        
        # Drop trigger function
        op.execute('DROP FUNCTION IF EXISTS update_updated_at_column();')
    
    # Drop tables in reverse order (respecting foreign key dependencies)
    op.drop_table('page_tags')
    op.drop_table('tags')
    op.drop_table('pages')
    op.drop_table('sections')
    op.drop_table('notebooks')

