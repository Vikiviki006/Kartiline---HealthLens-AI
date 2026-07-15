import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.user_model import User
from app.core.security import hash_password
import uuid

def seed_dummy_user():
    db: Session = SessionLocal()
    try:
        user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
        existing_user = db.query(User).filter_by(id=user_id).first()
        hashed_pwd = hash_password("password123")
        
        if not existing_user:
            dummy_user = User(
                id=user_id,
                email="dev@example.com",
                hashed_password=hashed_pwd,
                full_name="Dev User"
            )
            db.add(dummy_user)
            db.commit()
            print("Dummy user seeded successfully with password: password123")
        else:
            # Update password if it's the unhashed dummy string
            if existing_user.hashed_password == "dummy_password_hash":
                existing_user.hashed_password = hashed_pwd
                db.commit()
                print("Dummy user password updated to proper bcrypt hash (password123).")
            else:
                print("Dummy user already exists with proper password.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding dummy user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_dummy_user()
