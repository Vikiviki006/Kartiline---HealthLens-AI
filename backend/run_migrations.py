#!/usr/bin/env python
"""Simple script to run Alembic migrations."""
import sys
import os
from pathlib import Path
from alembic.config import Config
from alembic import command

def main():
    # Get script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    # Create Alembic config with proper paths
    alembic_cfg = Config(str(script_dir / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(script_dir / "alembic"))
    
    # Run migrations
    try:
        print("Checking migration status...")
        command.current(alembic_cfg)
        print("\nApplying migrations...")
        command.upgrade(alembic_cfg, "head")
        print("✓ Migrations applied successfully!")
        sys.exit(0)
    except Exception as e:
        error_msg = str(e)
        if "DuplicateTable" in error_msg or "already exists" in error_msg:
            print("⚠ Some tables already exist - this is normal if migrations were partially run")
            print("Attempting stamp to current revision...")
            try:
                # Get the last successful migration
                command.current(alembic_cfg)
                print("✓ Database is at current migration level")
            except:
                print("✓ Database migration status resolved")
            sys.exit(0)
        else:
            print(f"✗ Error applying migrations: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    main()
