from app import app
from models import db, User

with app.app_context():
    users = User.query.all()
    for u in users:
        # Use user ID to generate consistent, gender-neutral image
        # Picsum provides random but stable images
        u.photo_url = f"https://picsum.photos/id/{u.id % 1000}/200/200"
    db.session.commit()
    print(f"Updated {len(users)} users with Picsum photos")