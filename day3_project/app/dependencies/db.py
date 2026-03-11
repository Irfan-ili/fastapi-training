from app.database.fake_db import FakeDatabase

def get_db():
    """
    TOPIC: DB Session Pattern + Request-Scoped Session

    yield splits this into 3 phases:
      1. BEFORE yield  → open session   (setup)
      2. yield db      → view runs here
      3. AFTER yield   → close session  (cleanup, always runs)

    Production SQLAlchemy version looks identical:
        def get_db():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()
    """
    db = FakeDatabase()
    db.begin()
    try:
        yield db
    finally:
        db.close()
