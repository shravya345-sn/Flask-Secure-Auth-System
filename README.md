# Secure Flask Authentication System (MySQL & Bcrypt)

A robust User Authentication and Management system built with **Python Flask**, featuring secure password hashing and role-based access control.

## 🚀 Features
* **Secure Hashing**: Utilizes `Bcrypt` for one-way password hashing to ensure user data protection.
* **Role-Based Access**: Separate dashboards for **Users** and **Administrators**.
* **Admin Security**: Restrictive registration logic that prevents unauthorized users from creating Admin accounts.
* **Database Management**: Full integration with **MySQL** for persistent data storage.
* **Responsive UI**: Modern CSS styling with customized action buttons and flash message notifications.

## 🛠️ Technology Stack
* **Backend**: Flask (Python)
* **Database**: MySQL
* **Security**: Flask-Bcrypt, Flask-SQLAlchemy
* **Frontend**: HTML5, CSS3 (Jinja2 Templates)

## 📋 How to Run
1.  **Clone the repo**: `git clone <your-repo-link>`
2.  **Install dependencies**: `pip install -r requirements.txt`
3.  **Setup Database**: Create a MySQL database named `auth_db`.
4.  **Configure app.py**: Update the `SQLALCHEMY_DATABASE_URI` with your MySQL root password.
5.  **Run**: `python app.py`

## 🛡️ Security Implementation
This project demonstrates industry-standard security by never storing passwords in plain text. Even the fixed admin credentials are automatically hashed upon the first server start.

## ⚙️ System Logic & Security Rules

### 1. Restricted Admin Registration
To maintain system integrity, the registration of new **Admin** accounts via the public sign-up form is strictly prohibited.
* **Logic**: If a user selects 'Admin' during registration, the system intercepts the request, blocks the database entry, and displays a restricted access notification.
* **Fixed Admin**: Administrative access is reserved for the pre-configured system admin defined in the backend.

### 2. User Lifecycle & Deletion
The system supports full administrative control over user accounts.
* **Real-time Updates**: When an Admin deletes a user from the dashboard, the record is immediately removed from the MySQL database.
* **Re-registration**: Once an account is deleted, all associated data is purged. If that individual wishes to access the platform again, they must undergo the standard registration process as a new user.

## 📂 Project Structure

auth_project/
├── static/
│   └── style.css            # Custom CSS for UI & Buttons
├── templates/
│   ├── login.html           # Login interface with flash notifications
│   ├── register.html        # Secured registration with admin-block logic
│   ├── user_dashboard.html  # Standard user landing page
│   ├── admin_dashboard.html # Administrative user management panel
│   └── profile.html         # User account details page
├── .gitignore               # Instruction file for repository hygiene
├── app.py                   # Main Flask application & MySQL logic
├── requirements.txt         # List of Python dependencies
└── README.md                # Project documentation and setup guide                 

