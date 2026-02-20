# 🧠 Smart Task Manager (Python + Flask)


# 📌 Smart Task Manager

A **Flask-based Smart Task Manager** that helps users manage tasks efficiently with analytics, productivity tracking, and a clean dashboard UI.

---

## 🚀 Features Implemented (v1.0)

### 🔐 Authentication

* User Registration
* Login / Logout
* Secure password hashing
* Session handling

### 📝 Task Management

* Add tasks
* Edit tasks
* Delete tasks
* Mark tasks as completed
* Priority levels (Low / Medium / High)
* Due dates

### 🔎 Productivity Tools

* Task filters (All / Pending / Completed)
* Task search (title & description)
* Daily streak system ⏱️
* Productivity score (%)
* AI-based task suggestions 🧠 (rule-based)

### 📊 Analytics Dashboard

* Total tasks
* Completed vs Pending tasks
* Weekly productivity overview
* Priority distribution
* Streak counter

### 🎨 UI / UX

* Bootstrap-based responsive UI
* Task cards
* Badges & status indicators
* Clean dashboard layout
* Optional dark mode support (future-ready)

  ## 🚀 Live Demo
https://your-render-link.onrender.com

---

## 🗂️ Project Structure

```plaintext
smart-task-manager/
│
├── backend/
│   ├── app.py
│   ├── routes.py
│   ├── models.py
│   ├── extensions.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── analytics.html
│
├── static/
│   ├── css/
│   ├── js/
│
├── instance/
│   └── app.db
│
├── run.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite (SQLAlchemy ORM)
* **Frontend:** HTML, Bootstrap, Jinja2
* **Charts:** Chart.js
* **Authentication:** Flask-Login
* **Security:** Werkzeug Password Hashing

---

## 🧪 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/smart-task-manager.git
cd smart-task-manager
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the application

```bash
python run.py
```

### 5️⃣ Open in browser

```
http://127.0.0.1:5000
```

---

## 📦 Requirements (`requirements.txt`)

```plaintext
Flask
Flask-Login
Flask-SQLAlchemy
Werkzeug
python-dotenv
```

---

## 🧠 AI Task Suggestions (Rule-Based)

The system intelligently suggests actions based on:

* Pending high-priority tasks
* Overdue tasks
* Completion status
* User consistency

---

## 🏗️ Current Status

* ✅ Core features stable
* 🚧 Advanced analytics (future)
* 🚀 Ready for FREE deployment

---

## 🌍 Deployment

This project can be deployed **FREE** using:

* Render
* Railway
* PythonAnywhere

(Deployment guide coming soon)

---

## 👨‍💻 Author

**Pratik Santosh Walunj**
🎓 Computer Science Graduate
💻 Flask | Python | WordPress | Full Stack
📍 India

---

## 📄 License

This project is licensed under the **MIT License** – free to use and modify.

---

