#!/usr/bin/env python
"""Check database schema."""
import sys
from app.database.session import engine
from sqlalchemy import inspect, text

def check_schema():
    """Check if ai_summary column exists."""
    try:
        inspector = inspect(engine)
        
        # Get reports table columns
        if 'reports' in inspector.get_table_names():
            columns = inspector.get_columns('reports')
            col_names = [col['name'] for col in columns]
            
            print("Reports table columns:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
            
            if 'ai_summary' in col_names:
                print("\n✓ ai_summary column EXISTS!")
                return True
            else:
                print("\n✗ ai_summary column MISSING")
                print("\nAdding ai_summary column...")
                with engine.begin() as conn:
                    conn.execute(text("ALTER TABLE reports ADD COLUMN ai_summary TEXT;"))
                    conn.commit()
                print("✓ ai_summary column added successfully!")
                return True
        else:
            print("✗ reports table not found")
            return False
    except Exception as e:
        print(f"✗ Error checking schema: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_schema()
    sys.exit(0 if success else 1)
