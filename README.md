# BILLMASTER 🧾

**BILLMASTER** is a Django-based billing and inventory management system that allows authenticated users to manage products, generate invoices, and email PDF bills.

---

## 🔧 Features
- User Sign-Up & Login (session-based)
- Add, View, Delete Products
- Create Bills, Generate PDF
- Send PDF bills via Email
- Maintains per-user inventory

---

## 🛠️ One-Page Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/Anit-Paul/BILLMASTER.git
cd BILLMASTER
If you get fatal: destination path 'BILLMASTER' already exists, delete the folder or choose another directory.

Step 2: Create & Activate Virtual Environment
bash
Copy
Edit
# Windows
python -m venv env
env\Scripts\activate

# Linux / macOS
python3 -m venv env
source env/bin/activate
Step 3: Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
If the file doesn't exist, run:

bash
Copy
Edit
pip freeze > requirements.txt
Step 4: Run Migrations
bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
Step 5: Start the Development Server
bash
Copy
Edit
python manage.py runserver
Now visit: http://127.0.0.1:8000/

📁 Folder Overview
csharp
Copy
Edit
BILLMASTER/
├── bill/               # Billing app (product CRUD, bill logic)
│   ├── views.py
│   ├── models.py
│   └── pdf.py
├── login/              # Auth app
│   ├── views.py
│   ├── models.py
├── home/               # Dashboard
│   └── views.py
├── templates/          # HTML pages
│   ├── bill/
│   ├── login/
│   └── home/
├── static/             # CSS/JS
├── manage.py
└── requirements.txt
👨‍💻 Developer Info
Name: Anit Paul

University: Sister Nivedita University (3rd Year B.Tech)

Expertise: Backend Development, Problem Solving

Achievements: HackerRank Gold Badge (C++, Python), 300+ LeetCode problems solved

Email: anitpaul12345@gmail.com

GitHub: github.com/Anit-Paul
