"""
Script to drop all tables from the database.
WARNING: This will delete ALL data! Use with caution.
"""
from app.database.connection import engine
from app.database.models import Base

def drop_all_tables():
    print("WARNING: This will drop all tables and delete ALL data!")
    print("\nTables that will be dropped:")
    print("  - youtube_videos")
    print("  - openai_articles")
    print("  - anthropic_articles")
    print("  - venturebeat_articles")
    print("  - techcrunch_articles")
    print("  - sciencedaily_articles")
    print("  - digests")

    confirm = input("\nAre you sure? Type 'yes' to continue: ")

    if confirm.lower() != 'yes':
        print("Aborted.")
        return

    print("\nDropping all tables...")
    Base.metadata.drop_all(engine)
    print("[OK] All tables dropped successfully!")

    print("\nRecreating all tables...")
    Base.metadata.create_all(engine)
    print("[OK] All tables recreated successfully!")

    print("\nDatabase is now clean and ready for fresh data!")

if __name__ == "__main__":
    drop_all_tables()
