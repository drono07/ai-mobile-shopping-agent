"""
Create authentication and conversation tables
"""
from database import engine, Base, User, Conversation, ConversationMessage

def create_auth_tables():
    """Create authentication and conversation tables"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Successfully created authentication and conversation tables")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise

if __name__ == "__main__":
    create_auth_tables()
