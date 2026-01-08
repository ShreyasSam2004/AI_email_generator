"""
Migration script to create new tables for VentureBeat, TechCrunch, and ScienceDaily.
Run this once to add the new tables to your database.
"""
from app.database.connection import engine
from app.database.models import Base, VentureBeatArticle, TechCrunchArticle, ScienceDailyArticle


def create_new_tables():

    print("Creating new tables...")

    # Create only the new tables
    VentureBeatArticle.__table__.create(engine, checkfirst=True)
    print("[OK] Created venturebeat_articles table")

    TechCrunchArticle.__table__.create(engine, checkfirst=True)
    print("[OK] Created techcrunch_articles table")

    ScienceDailyArticle.__table__.create(engine, checkfirst=True)
    print("[OK] Created sciencedaily_articles table")

    print("\nAll new tables created successfully!")


if __name__ == "__main__":
    create_new_tables()
