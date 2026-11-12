# 💰 Personal Expense Tracker

A full-stack personal finance web application developed using **Python, Django, SQLite, HTML, CSS, and Bootstrap 5**.

The Personal Expense Tracker helps users manage their finances in one place. Users can record income and expenses, organize transactions, set monthly budgets, monitor spending habits, and generate financial reports through a clean and responsive dashboard.

## ✨ Features

- User registration, login, and logout
- Personal transactions, categories, and budgets for each user
- Dashboard showing monthly income, expenses, and net balance
- Add, view, update, and delete transactions
- Custom income and expense categories
- Search and filter transactions by keyword, type, category, and date
- Monthly budgets with spending progress and status
- Financial reports with monthly and category summaries
- Export filtered transactions to CSV
- Django administration panel
- Responsive Bootstrap 5 interface
- Interactive charts using Chart.js

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python 3.10+ |
| Backend Framework | Django 5.2 |
| Database | SQLite |
| Frontend | HTML5, CSS3 |
| CSS Framework | Bootstrap 5 |
| Icons | Bootstrap Icons |
| Data Visualization | Chart.js |
| Development Tools | VS Code, Git, GitHub |

## 🚀 Getting Started

Follow these steps to run the project on your Windows computer.

### 1. Clone the repository

```bash
git clone https://github.com/Binod-Shrestha-Debug/Personal-Expense-Tracker-Django.git
```

### 2. Open the project folder

```bash
cd Personal-Expense-Tracker-Django
```

### 3. Create a virtual environment

```bash
py -m venv .venv
```

### 4. Activate the virtual environment

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Create database migrations

```bash
python manage.py makemigrations tracker
```

### 7. Apply database migrations

```bash
python manage.py migrate
```

### 8. Create an admin account (optional)

```bash
python manage.py createsuperuser
```

### 9. Start the development server

```bash
python manage.py runserver
```

Open the application in your browser:

**http://127.0.0.1:8000/**

## 🔗 Main Application URLs

| URL | Description |
|---|---|
| `/` | Dashboard |
| `/accounts/signup/` | Create an account |
| `/accounts/login/` | Sign in |
| `/transactions/` | View and filter transactions |
| `/transactions/add/` | Add a transaction |
| `/categories/` | Manage categories |
| `/budgets/` | Manage monthly budgets |
| `/reports/` | View financial reports |
| `/reports/export/` | Export transactions to CSV |
| `/admin/` | Django administration |

## 📁 Project Structure

```text
Personal-Expense-Tracker-Django/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── tracker/
│   ├── migrations/
│   ├── templates/
│   │   ├── registration/
│   │   └── tracker/
│   ├── static/
│   │   └── tracker/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 📊 How It Works

1. Create an account and sign in.
2. Set up categories for income and expenses.
3. Record transactions with amounts, dates, categories, and notes.
4. Set monthly budgets to monitor spending.
5. Visit the dashboard to review your financial activity.
6. Explore reports and export transaction records as CSV files.

## 🔒 Data and Privacy

- SQLite stores application data during local development.
- Each user's transactions, categories, and budgets are associated with their account.
- Application views restrict access to the signed-in user's records.
- Deleting a category preserves existing transactions without a category assignment.

## 🌐 Production Considerations

This project is configured for local development. Before deploying it publicly:

- Store the Django `SECRET_KEY` in an environment variable.
- Set `DEBUG=False`.
- Configure `ALLOWED_HOSTS`.
- Enable HTTPS and secure cookie settings.
- Configure production static-file serving.
- Set up database backups and appropriate logging.
- Review authentication and deployment security.

## 👨‍💻 About the Developer

**Binod Shrestha**  
Data Analyst | Python Developer | SQL Enthusiast

I enjoy working with data, building practical applications, and developing solutions that make information easier to understand and manage.

This project is part of my journey in Python and Django development, with a focus on database management, financial data analysis, and web application development.

📍 Nepal 🇳🇵

- **GitHub:** [Binod-Shrestha-Debug](https://github.com/Binod-Shrestha-Debug)
- **LinkedIn:** [Binod Shrestha](https://www.linkedin.com/in/binod-shrestha-3b6103439/)

---

⭐ If you find this project interesting, feel free to explore the repository and share your feedback.

**Built with Python, Django, and a passion for learning.**