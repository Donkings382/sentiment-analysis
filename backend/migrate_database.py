"""
Database migration script - Drop old tables and create new structure
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from models.database import Base, engine
from sqlalchemy import text

def migrate():
    print("\n" + "="*60)
    print("DATABASE MIGRATION")
    print("="*60)
    
    # Drop old tables
    print("\nDropping old tables...")
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS results CASCADE"))
        conn.commit()
    print("Old tables dropped")
    
    # Create new tables
    print("\nCreating new tables (searches + tweets)...")
    Base.metadata.create_all(bind=engine)
    print("New tables created")
    
    print("\n" + "="*60)
    print("MIGRATION COMPLETE!")
    print("="*60)
    print("\nNew structure:")
    print("  - searches table (stores each scrape event)")
    print("  - tweets table (stores individual tweets)")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        print(f"\nMigration failed: {e}\n")
        import traceback
        traceback.print_exc()
