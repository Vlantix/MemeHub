from app import app
from models import database, User

def test_user_model():
    with app.app_context():
        # Clear existing data and recreate tables
        print("🔄 Resetting database...")
        database.drop_all()
        database.create_all()
        print("✅ Database tables created")
        
        # Create a new user
        print("\n📝 Creating new user...")
        user = User(
            display_name='John Doe',
            username='john_doe'
        )
        user.set_password('mysecretpassword123')
        
        # Add to database
        database.session.add(user)
        database.session.commit()
        print(f"✅ User created with ID: {user.id}")
        
        # Display user info
        print(f"\n👤 User details:")
        print(user.to_dict())
        
        # Test password verification
        print("\n🔐 Testing password verification:")
        print(f"  Correct password 'mysecretpassword123': {user.check_password('mysecretpassword123')}")
        print(f"  Wrong password 'wrongpass': {user.check_password('wrongpass')}")
        
        # Test retrieving user from database
        print("\n🔍 Testing database retrieval:")
        retrieved_user = User.query.filter_by(username='john_doe').first()
        if retrieved_user:
            print(f"✅ User found: {retrieved_user.display_name}")
            print(f"   Username: {retrieved_user.username}")
            print(f"   Active: {retrieved_user.is_active}")
        else:
            print("❌ User not found")
        
        # Test creating a second user
        print("\n📝 Creating second user...")
        user2 = User(
            display_name='Jane Smith',
            username='jane_smith'
        )
        user2.set_password('janepassword456')
        database.session.add(user2)
        database.session.commit()
        print(f"✅ User created: {user2.display_name}")
        
        # Test querying all users
        print("\n📊 All users in database:")
        all_users = User.query.all()
        print(f"  Total users: {len(all_users)}")
        for u in all_users:
            print(f"  - {u.username} ({u.display_name})")

if __name__ == '__main__':
    test_user_model()