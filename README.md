# 💕 Dating App - AI-Powered Matchmaking

A complete dating web application with machine learning compatibility scoring, real-time chat, and friend requests.

## ✨ Features

- **ML-Powered Matching** – Compatibility scores based on user profiles (age, height, interests, lifestyle)
- **User Authentication** – JWT-based login/registration
- **Profile Management** – Upload photos, write bio, set preferences
- **Smart Recommendations** – See only opposite gender matches ranked by compatibility
- **Friend Requests** – Send, accept, or reject friend requests
- **Private Chat** – Real-time messaging with friends
- **Responsive Design** – Works on desktop and mobile

## 🛠️ Tech Stack

### Backend
- Flask (Python)
- SQLAlchemy ORM
- JWT Authentication
- Scikit-learn (ML matching)
- SQLite (database)

### Frontend
- React 18
- React Router DOM
- CSS3 (custom styling)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Clone repository
git clone https://github.com/helina-me/dating-app.git
cd dating-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app import app; from models import db; app.app_context().push(); db.create_all()"

# Start backend server
python app.py
