"""
Migration script to create all database tables.
Safe to run multiple times - uses checkfirst=True to avoid errors.
"""
from app.database.connection import engine
from app.database.models import Base


def create_new_tables():
    print("Creating database tables...")

    # Create all tables defined in models
    # checkfirst=True means it won't error if tables already exist
    Base.metadata.create_all(engine, checkfirst=True)

    print("[OK] All tables created successfully!")
    print("\nTables:")
    print("  - youtube_videos")
    print("  - openai_articles")
    print("  - anthropic_articles")
    print("  - venturebeat_articles")
    print("  - techcrunch_articles")
    print("  - sciencedaily_articles")
    print("  - digests")


if __name__ == "__main__":
    create_new_tables()
