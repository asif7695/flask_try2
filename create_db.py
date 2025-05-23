from hello import app, db

# Use the app context to make sure everything's loaded right
with app.app_context():
    db.create_all()
    print("✅ Database created successfully!")
