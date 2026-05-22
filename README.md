# Secure Login System

A production-style Flask authentication project designed for cybersecurity portfolios, internship demonstrations, academic mini projects, and resume showcases. This application focuses on implementing secure authentication mechanisms and modern web security best practices.

---

## Features

* Secure user registration system
* Duplicate email prevention
* Strong password validation policy
* bcrypt password hashing with automatic salting
* Secure login authentication
* Generic login error messages
* Account lockout after repeated failed attempts
* Flask-Login session management
* Secure logout functionality
* Protected dashboard and profile routes
* CSRF protection using Flask-WTF
* HTTPOnly and SameSite session cookie settings
* Optional Google Authenticator compatible TOTP 2FA
* Password reset token flow
* Remember me functionality
* Login history tracking
* Responsive Bootstrap 5 UI

---

## Tech Stack

| Technology   | Purpose                   |
| ------------ | ------------------------- |
| Python       | Backend programming       |
| Flask        | Web framework             |
| SQLite       | Database                  |
| Flask-Bcrypt | Password hashing          |
| Flask-Login  | Session management        |
| Flask-WTF    | Form validation & CSRF    |
| Bootstrap 5  | Responsive frontend       |
| pyotp        | Two-Factor Authentication |

---

## Project Structure

```bash
SECURELOGINSYSTEM/
│
├── demo/
│   └── secure-login-demo.mp4
│ 
├── forms/
│   └──auth_forms.py
│ 
├── routes/
│    ├── auth.py
│    └── dashboard.py
│
├── screenshots/
│   ├── 2fa.png
│   ├── 2fa1.png
│   ├── dashboard.png
│   ├── folder.png
│   ├── login.png
│   ├── logout.png
│   ├── profile.png
│   ├── register1.png
│   ├── register2.png
│   ├── secure_login.png
│   ├── set_2fa.png
│   └── set_2fa1.png
│
├── static/
│   ├── css/styles.css
│   └── js/main.js  
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── forgot_password.html
│   ├── login.html
│   ├── profile.html
│   ├── register.html
│   ├── reset_password.html
│   ├── setup_2fa.html
│   └── verify_2fa.html
│
├── utils/
│   └──security.py
├── .env
├── .gitignore
├── app_factory.py
├── app.py
├── README.md
└── requirements.txt
```

---

## Project Demo

Complete application demonstration video:

[Watch Demo Video][security-login-demo.mp4](demo/security-login-demo.mp4)
---

## Installation

```bash
git clone <your-github-repo-link>
cd CYBERSECURELOGIN

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

python app.py
```

Open the application in browser:

```text
http://127.0.0.1:5000
```

---

## Environment Variables

Configure `.env` file:

```text
SECRET_KEY=use-a-long-random-secret-here
DATABASE_URL=sqlite:///database.db
SESSION_COOKIE_SECURE=False
SESSION_MINUTES=30
```

Set:

```text
SESSION_COOKIE_SECURE=True
```

when deploying with HTTPS.

---

## Authentication Workflow

1. User registers with validated credentials
2. Password is hashed using bcrypt before storage
3. User logs in securely using hashed password verification
4. Flask session is created securely
5. Optional TOTP 2FA verification is performed
6. Protected routes become accessible
7. Session is destroyed securely on logout

---





### Two-Factor Authentication

2FA is implemented using `pyotp` and Google Authenticator compatible TOTP verification codes.



---


## Screenshots

### 1. User Registration Page
The registration page allows users to create secure accounts with password policy validation and duplicate email prevention.

![Register Page](Screenshots/register1.png)

---

### 2. Registration Validation
This screen demonstrates secure input validation and strong password requirement enforcement during user registration.

![Registration Validation](Screenshots/register2.png)

---

### 3. Secure Login Page
The login page implements secure authentication with bcrypt password verification, CSRF protection, and session handling.

![Login Page](Screenshots/login.png)

---

### 4. Secure Dashboard
The dashboard is protected and accessible only after successful user authentication.

![Dashboard](Screenshots/dashboard.png)

---

### 5. User Profile Page
The profile page allows users to manage account settings and security configurations.

![Profile Page](Screenshots/profile.png)

---

### 6. Two-Factor Authentication Setup
Users can enable Google Authenticator compatible TOTP-based Two-Factor Authentication for enhanced account security.

![2FA Setup](Screenshots/set_2fa.png)

---

### 7. Additional 2FA Configuration
Additional configuration workflow for enabling and managing Two-Factor Authentication.

![2FA Configuration](Screenshots/set_2fa1.png)

---

### 8. Secure Logout Workflow
The logout functionality securely destroys active sessions and prevents unauthorized session reuse.

![Logout](Screenshots/logout.png)

---

### 9. Complete Application Preview
Overall preview of the Secure Login System application interface.

![Application Preview](Screenshots/secure_login.png)

---

### 10. Two-Factor Authentication Verification
Users must verify their identity using a secure 6-digit TOTP verification code during login.

![2FA Verification](Screenshots/2fa.png)

---

### 11. Additional 2FA Verification Screen
Additional authentication verification workflow screen for enhanced account protection.

![2FA Verification Additional](Screenshots/2fa1.png)


### 12. Complete Project Folder Structure
The project follows a modular and organized Flask application structure for maintainability and scalability.

![Folder Structure](Screenshots/folder.png)

---


## Learning Outcomes

Through this project, I gained practical experience with:

* Secure authentication system development
* Password hashing using bcrypt
* Session and cookie security
* CSRF protection implementation
* SQL injection prevention
* Flask backend architecture
* Two-Factor Authentication integration
* Secure coding practices

---

## Future Improvements

* Add QR code rendering for TOTP setup
* Add SMTP email integration
* Add Flask-Limiter for IP-based rate limiting
* Add Content Security Policy headers
* Add automated testing with pytest
* Add Docker deployment support
* Add production WSGI deployment configuration

---

## Portfolio Use

This project was developed to demonstrate practical cybersecurity and secure authentication concepts for internships, GitHub portfolios, resume projects, and academic submissions.

---

## Conclusion

This project demonstrates how secure authentication systems can be implemented using Flask and modern cybersecurity best practices. It combines usability with strong defensive mechanisms to protect authentication workflows and user accounts.
