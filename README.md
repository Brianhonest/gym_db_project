# Health and Fitness Club Management System

A full-stack database-driven application for managing gym operations, including member registrations, trainer scheduling, and administrative functions.

**Course:** COMP 3005 - Database Management Systems  
**Semester:** Fall 2025  
**Author:** Brian Christoper

---

## 📋 Project Overview

This system manages three user roles with distinct operations:
- **Members:** Register, track health metrics, set fitness goals, book classes and PT sessions
- **Trainers:** Set availability schedules, view upcoming sessions and classes
- **Admins:** Create group classes, manage room bookings

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python web framework)
- **ORM:** SQLAlchemy (for database operations)
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **API Testing:** Postman

---

## 📂 Project Structure
```
gym_db/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database connection configuration
│   └── routers/             # API endpoint routers
│       ├── members.py       # Member operations
│       ├── trainers.py      # Trainer operations
│       └── admin.py         # Admin operations
├── models/
│   ├── user.py              # User, Member, Trainer, Admin models
│   ├── room.py              # Room model
│   ├── group_class.py       # GroupClass model
│   ├── class_registration.py
│   ├── fitness_goal.py
│   ├── health_metric.py
│   ├── personal_training_session.py
│   └── trainer_availability.py
├── frontend/
│   ├── index.html           # Web interface
│   ├── styles.css           # Styling
│   └── app.js               # Frontend JavaScript
├── sql/
│   ├── create_view.sql      # Database views
│   ├── create_trigger.sql   # Database triggers
│   └── create_index.sql     # Database indexes
├── docs/
│               # ER Diagram and documentation and relational schema
├── populate_data.py         # Sample data generator
├── .env                     # Environment variables (not in repo)
├── create_tables.py         # Script to create database tables
└── requirements.txt         # Python dependencies
```

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone [your-repo-url]
cd gym_db
```

### 2. Create Virtual Environment
```bash
python -m venv gym_env
source gym_env/bin/activate  # On Windows: gym_env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

Create a PostgreSQL database:
```sql
CREATE DATABASE gym_db;
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/gym_db
```

Replace `YOUR_USERNAME` and `YOUR_PASSWORD` with your PostgreSQL credentials.

### 6. Create Database Tables
```bash
python create_tables.py
```

### 7. Populate Sample Data
```bash
python populate_data.py
```

### 8. Run Database Scripts (Views, Triggers, Indexes)
```bash
psql -d gym_db -f sql/create_view.sql
psql -d gym_db -f sql/create_trigger.sql
psql -d gym_db -f sql/create_index.sql
```

### 9. Start the Backend Server
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 10. Open the Frontend

Open `frontend/index.html` in your web browser, or serve it with:
```bash
cd frontend
python -m http.server 8080
```

Then navigate to `http://localhost:8080`

---

## 📊 Database Schema

The system uses 11 entities:
- **User** (parent entity for Member, Trainer, Admin via ISA hierarchy)
- **Member, Trainer, Admin** (specialized user types)
- **Room** (gym facilities)
- **GroupClass** (scheduled fitness classes)
- **ClassRegistration** (junction table for Member-GroupClass M:N relationship)
- **FitnessGoal** (member fitness objectives)
- **HealthMetric** (historical health data)
- **PersonalTrainingSession** (1-on-1 training appointments)
- **TrainerAvailability** (trainer working hours)

**Normalization:** All tables are in Third Normal Form (3NF) to prevent data anomalies.

---

## 🎯 Implemented Operations

### Member Operations (6)
1. ✅ User Registration - Create new member account
2. ✅ Profile Management - Update personal information
3. ✅ Log Health Metrics - Record weight, heart rate, etc.
4. ✅ View Dashboard - See health stats, goals, and activity
5. ✅ Register for Group Class - Enroll in fitness classes
6. ✅ Schedule PT Session - Book personal training

### Trainer Operations (2)
7. ✅ Set Availability - Define working hours
8. ✅ View Schedule - See upcoming sessions and classes

### Admin Operations (2)
9. ✅ Create Group Class - Add new fitness classes
10. ✅ Update Room Booking - Reassign rooms for sessions/classes

---

## 🔍 Key Features

- **ISA Hierarchy:** User entity with specialized Member/Trainer/Admin types
- **Complex Validation:** Overlap detection for trainer availability and room bookings
- **Trigger:** Automatic class capacity checking to prevent overbooking
- **View:** Optimized query for member dashboard (latest health metrics)
- **Indexes:** Performance optimization on frequently queried columns
- **ORM Implementation:** Full SQLAlchemy usage for database operations (10% bonus)

---

## 🧪 Testing

API endpoints can be tested using:
- **Swagger UI:** `http://localhost:8000/docs` (auto-generated by FastAPI)
- **Postman:** Import the collection from `postman_collection.json` (if included)
- **Frontend:** Use the web interface at `frontend/index.html`

### Sample Test Data

After running `populate_data.py`, you'll have:
- 5 users (3 members, 1 trainer, 1 admin)
- 3 rooms
- 2 group classes
- Sample health metrics, goals, and sessions

**Test Credentials:**
- Member IDs: 1, 2, 3
- Trainer ID: 4
- Admin ID: 5

---

## 📹 Demo Video

(https://youtu.be/16-v5wvh-Lw)

The video demonstrates:
- ER diagram explanation
- Database schema and normalization
- All 10 operations working
- Code walkthrough

---

## 📝 Report

See `docs/` folder for:
- ER Diagram (ERD.pdf)
- Relational Schema
- Normalization analysis

---

## 🐛 Known Issues / Future Improvements

- Manual user ID entry (would implement authentication system)
- No password hashing (using placeholder for demo)
- Could add data visualizations to dashboard
- Could implement email notifications for class registrations

