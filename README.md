# Quiz Master – Quiz Management Web Application

A web-based quiz management platform built with **Flask, Python, SQLite, HTML, CSS, Bootstrap, and Jinja2**. The application enables administrators to manage quizzes and their associated subjects, chapters, and questions, while registered users can attempt scheduled quizzes, view their scores, and track their past attempts.

## Overview

Quiz Master is a web application designed to simplify the creation, management, scheduling, and participation of quizzes through a centralized platform.

The application supports two types of users: an administrator (Quiz Master) and registered users. The administrator manages the quiz content and user-related operations, while users can explore available quizzes, attempt quizzes scheduled for the current date, and review their performance.

The project demonstrates full-stack web development using Flask, server-side rendering with Jinja2, database management with SQLite, and user authentication.

## Key Features

### Admin Dashboard

The administrator acts as the superuser of the application. There is a single administrator account, which does not require registration.

**Authentication and Account Management**
- Secure administrator login.
- Redirect to the admin dashboard after successful login.
- Change password functionality.

**Quiz Content Management**
- Create, view, edit, and delete subjects.
- Organize subjects into chapters.
- Create and manage quizzes.
- Add, edit, and delete quiz questions.
- Manage the quiz hierarchy: Subjects → Chapters → Quizzes → Questions.

**Search and Discovery**
- Search users by user ID, username, or name.
- Search subjects and chapters by name.
- Search quizzes by quiz ID and scheduled date.
- Search questions by question ID or question statement.

### User Features

**User Authentication**
- Register for an account and log in.
- Change password.

**Quiz Participation**
- Browse and attempt quizzes of their choice.
- Attempt only quizzes scheduled for the current date.
- View scores after attempting quizzes.
- Access past attempts and review previous quiz performance.

**Search Functionality**
- Search subjects and chapters by name.
- Search quizzes by quiz ID and scheduled date.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, Bootstrap |
| Templating Engine | Jinja2 |
| Database | SQLite |
| Configuration | Environment variables using `.env` |
| Dependency Management | Python `requirements.txt` |

### Architecture

The application follows a Flask-based web architecture:

1. **Presentation Layer:** HTML, CSS, Bootstrap, and Jinja2 templates provide the user interface.
2. **Application Layer:** Flask handles incoming requests, authentication, quiz management, search operations, and application workflows.
3. **Data Layer:** SQLite stores the application's persistent data.
4. **Configuration Layer:** Environment variables allow application configuration, including the secret key.

## Application Workflow

### Administrator Workflow

1. Log in using the administrator credentials.
2. Access the admin dashboard.
3. Create and manage subjects and chapters.
4. Create quizzes and add questions.
5. Manage existing quiz content using editing and deletion operations.
6. Search for users, subjects, chapters, quizzes, and questions.

### User Workflow

1. Register for an account.
2. Log in to the application.
3. Browse subjects, chapters, and quizzes.
4. Select a quiz scheduled for the current date.
5. Attempt the quiz.
6. View the score and access past quiz attempts.

## Project Structure

The repository contains the following main components:

```text
quiz_master_24f1001188/
├── templates/
├── controllers/
├── .env.sample
├── app.py
└── requirements.txt
```

- **`app.py`** – Main Flask application entry point.
- **`templates/`** – Jinja2 templates used to render the web pages.
- **`controllers/`** – Application controller modules.
- **`.env.sample`** – Sample environment configuration.
- **`requirements.txt`** – Python dependencies required to run the application.

## Getting Started

Follow these instructions to run the application locally.

### Prerequisites

Ensure that the following are installed:

- Python 3
- Git
- A terminal or command-line interface
- A web browser

### 1. Clone the Repository

Replace `YOUR_GITHUB_USERNAME` with your GitHub username and use the actual repository name if it differs.

```bash
git clone https://github.com/24f1001188/quiz-master-application.git
cd quiz_master_24f1001188
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows (Command Prompt)**

```cmd
venv\Scripts\activate
```

**Windows (PowerShell)**

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file from the provided sample.

**macOS / Linux**

```bash
cp .env.sample .env
```

**Windows (Command Prompt)**

```cmd
copy .env.sample .env
```

Open `.env` and provide a secure secret key in the designated placeholder.

Keep the `.env` file private. Do not commit real secrets or credentials to GitHub.

### 5. Run the Application

Start the Flask development server:

```bash
flask run
```

Open the following URL in your browser:

http://127.0.0.1:5000/

If Flask cannot locate the application automatically, configure the appropriate Flask application entry point according to the project setup.

## Usage

### Administrator

Log in using the configured administrator credentials to access the dashboard and manage subjects, chapters, quizzes, questions, and user searches.

### Registered Users

Create a user account, log in, browse available quizzes, attempt quizzes scheduled for the current date, and review scores and previous attempts.

## Security Considerations

- Configure a strong, private Flask secret key through environment variables.
- Never commit the `.env` file or sensitive credentials to version control.
- Use the provided `.env.sample` as a configuration template.
- Keep dependencies installed within the project's virtual environment.

## Skills Demonstrated

This project demonstrates practical experience in:

- Full-stack web application development.
- Python and Flask application development.
- Server-side rendering using Jinja2.
- Relational data management with SQLite.
- CRUD operations for subjects, chapters, quizzes, and questions.
- User authentication and password management.
- Search and filtering functionality.
- Date-based quiz scheduling and participation.
- Environment-based application configuration.
- Dependency management and local application setup.

## Future Enhancements

Potential improvements to extend the application include:

- Add quiz analytics and performance dashboards.
- Introduce quiz timers and automatic submission.
- Provide more detailed performance reports.
- Add pagination and advanced filtering for large datasets.
- Add automated tests for authentication, quiz management, and scoring.
- Deploy the application to a cloud hosting platform.

## Author

**Hemalatha Baskar**

Final-year B.Tech student in Computer Science and Engineering.

Interested in full-stack development, machine learning, artificial intelligence, and building practical software applications.

---

*Quiz Master was developed as a web application project to demonstrate quiz management, user interaction, and full-stack development using Flask and SQLite.*
