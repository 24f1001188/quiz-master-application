
Quiz Master Application

Overview

Quiz Master is a web-based application designed to facilitate quiz management. It enables administrators to create subjects, chapters, quizzes, and questions while allowing users to attempt quizzes and review their performance.

Features

Admin Features:

*Admin is the superuser of the app and requires no registration(also known as the quiz master) 
*There is only one admin to this application
*The administrator login redirects to the admin dashboard
*Change Password
*Add,Edit,Delete subjects, chapters, quizzes, and questions.
*Search Users by user id,username,Name of the user.
*Search subjects,chapters by name.
*Search quizzes by quiz id and its scheduled date.
*Search questions by question id,question statement.
*Secure admin login.

User Features:

*Attempt quizzes of their choice and view scores and past attempts of the quizzes they have attempted
*Attempt only the quizzes that are scheduled to that particular date.
*Change password.
*Search subjects,chapters by name.
*Search quizzes by quiz id and its scheduled date.
*Change password.


Technologies Used

*Backend: Flask (Python)
*Frontend: Jinja2 templating,HTML, CSS, Bootstrap
*Database: SQLite

File Structure

quiz_master_24f1001188
    templates 
    controllers
    .env.sample
    app.py
    requirements.txt


Running the Application:

*Clone the repository from git and change directory to that folder.
*Now setup the virtual environment and install the required packages by running the below commands in the terminal:
>python -m venv venv
>source venv/bin/activate
>pip install -r requirements.txt

*Copy the .env.sample to a file .env
>cp .env.sample .env

*Provide the secret key into the .env file in the placeholder <secretkey>.
*Run the application using the below command.
>flask run

*Open "http://127.0.0.1:5000/" in browser.

*Admin can login and add,edit and delete subjects,chapters,quizzes,questions.
*Users can register and login to attempt the quizzes and can view feedback and their past attempts.






