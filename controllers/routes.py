from flask import render_template,request,redirect,url_for,flash,session,jsonify
from app import app
from models import db,Admin,User,Subject,Chapter,Quiz,Questions,Scores
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime,date
from functools import wraps
import re

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/user_login')
def user_login():
    return render_template('user_login.html')

@app.route('/user_login',methods=['POST'])
def user_login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Filling out all the fields is mandatory!')
        return redirect(url_for('user_login'))
    
    user=User.query.filter_by(username=username).first()

    if not user:
        flash('The E-mail is not registered.Kindly register before login or login with a registered E-mail')
        return redirect(url_for('user_login'))
    
    if not check_password_hash(user.passhash,password):
        flash('Incorrect password,Try again!')
        return redirect(url_for('user_login'))
    
    session['user_id']=user.id
    flash('Logged in Successfully!!')

    return redirect(url_for('user_dashboard'))

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin_login',methods=['POST'])
def admin_login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Filling out all the fields is mandatory!')
        return redirect(url_for('admin_login'))
    
    admin=Admin.query.filter_by(username=username).first()

    if not admin:
        flash('Wrong e-mail for admin login')
        return redirect(url_for('admin_login'))
    
    if not check_password_hash(admin.passhash,password):
        flash('Incorrect password,Try again!')
        return redirect(url_for('admin_login'))
    
    session['admin_id']=admin.id
    flash('Logged in Successfully!!')

    return redirect(url_for('admin_dashboard',id=admin.id))

@app.route('/new_user_registration')
def new_user_registration():
    return render_template('register.html')

@app.route('/set_credentials')
def reg_next_page():
    return render_template('reg_next_page.html')

@app.route('/set_credentials', methods=['POST'])
def reg_next_page_post():
    full_name = request.form.get('full_name')
    qualification = request.form.get('qualification')
    dob = request.form.get('dob')

    if not full_name or not qualification or not dob:
        flash('Filling out all the fields is mandatory!')
        return redirect(url_for('new_user_registration'))

    return render_template('reg_next_page.html', full_name=full_name, qualification=qualification, dob=dob)

@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    full_name = request.form.get('full_name')
    qualification = request.form.get('qualification')
    dob_string = request.form.get('dob')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    dob=datetime.strptime(dob_string, '%Y-%m-%d').date()

    if not username or not password or not confirm_password:
        flash('Filling out all the fields is mandatory!')
        return render_template('reg_next_page.html',full_name=full_name, qualification=qualification, dob=dob)

    if password!=confirm_password:
        flash('Passwords do not match!!')
        return render_template('reg_next_page.html',full_name=full_name, qualification=qualification, dob=dob)

    user=User.query.filter_by(username=username).first()
    if user:
        flash('The E-mail is already registered.Try again with a new E-mail or login with the existing email')
        return render_template('reg_next_page.html',full_name=full_name, qualification=qualification, dob=dob)
    
    passhash=generate_password_hash(password)

    New_User=User(username=username,passhash=passhash,Full_Name=full_name,Qualification=qualification,DOB=dob)
    db.session.add(New_User)
    db.session.commit()

    return render_template('reg_finished.html',name=full_name)

#decorators for user and admin authentication
#-------

def user_auth(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if 'user_id' in session:
            return func(*args,**kwargs)
        else:
            flash('Please Login to continue further!')
            return redirect(url_for('user_login'))
    return inner
    
def admin_auth(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if 'admin_id' in session:
            return func(*args,**kwargs)
        else:
            flash('Please Login to continue further!')
            return redirect(url_for('admin_login'))
    return inner

#-------

@app.route('/user_dashboard')
@user_auth
def user_dashboard():
        user=User.query.get(session['user_id'])

        query=request.args.get('query')
        if query:
             subjects=Subject.query.filter(Subject.Name.ilike(f'%{query}%'))
             return render_template('user_dashboard.html',user=user,subjects=subjects)
        subjects=Subject.query.all()

        return render_template('user_dashboard.html',user=user,subjects=subjects)

@app.route('/admin_dashboard')
@admin_auth
def admin_dashboard():
        admin=Admin.query.get(session['admin_id'])

        query=request.args.get('query')
        if query:
             subjects=Subject.query.filter(Subject.Name.ilike(f'%{query}%'))
             return render_template('admin_dashboard.html',admin=admin,subjects=subjects)

        subjects=Subject.query
        return render_template('admin_dashboard.html',admin=admin,subjects=subjects)
    
@app.route('/user_logout')
@user_auth
def user_logout():
        session.pop('user_id')
        return render_template('logout.html')
    
@app.route('/admin_logout')
@admin_auth
def admin_logout():
        session.pop('admin_id')
        return render_template('logout.html')
    
@app.route('/change_password_user')
@user_auth
def change_pswd_user():
        return render_template('change_pswd.html')
    
@app.route('/change_password_admin')
@admin_auth
def change_pswd_admin():
        return render_template('change_pswd.html')
    
@app.route('/change_password_user',methods=['POST'])
@user_auth
def change_pswd_user_post():
        curr_password=request.form.get('curr_password')
        new_password=request.form.get('new_password')
        confirm_new_password=request.form.get('confirm_new_password')

        if not curr_password or not new_password:
            flash('Filling out all the fields is mandatory')
            return redirect(url_for('change_pswd_user'))
        
        user=User.query.get(session['user_id'])

        if not check_password_hash(user.passhash,curr_password):
            flash('Incorrect Password')
            return redirect(url_for('change_pswd_user'))
        
        if new_password!=confirm_new_password:
            flash('New password and Confirm new password does not match.Please try again!')
            return redirect(url_for('change_pswd_user'))
        
        new_passhash=generate_password_hash(new_password)
        user.passhash=new_passhash
        db.session.commit()

        flash('Password Updated successfully!!')
        return redirect(url_for('user_dashboard'))
    
@app.route('/change_password_admin',methods=['POST'])
@admin_auth
def change_pswd_admin_post():
        curr_password=request.form.get('curr_password')
        new_password=request.form.get('new_password')
        confirm_new_password=request.form.get('confirm_new_password')

        if not curr_password or not new_password:
            flash('Filling out all the fields is mandatory')
            return redirect(url_for('change_pswd_admin'))
        
        admin=Admin.query.get(session['admin_id'])

        if not check_password_hash(admin.passhash,curr_password):
            flash('Incorrect Password')
            return redirect(url_for('change_pswd_admin'))
        
        if new_password!=confirm_new_password:
            flash('New password and Confirm new password does not match.Please try again!')
            return redirect(url_for('change_pswd_admin'))
        
        new_passhash=generate_password_hash(new_password)
        admin.passhash=new_passhash
        db.session.commit()

        flash('Password Updated successfully!!')
        return redirect(url_for('admin_dashboard'))


@app.route('/add/subject')
@admin_auth
def add_sub():
     return render_template('add_sub.html')

@app.route('/add/subject',methods=['POST'])
@admin_auth
def add_sub_post():
     sub_name=request.form.get('Name')
     des=request.form.get('Description')

     if not sub_name or not des:
          flash("Filling out all the fields is mandatory")
          return redirect(url_for('add_sub'))

     subject=Subject(Name=sub_name,Description=des)
     db.session.add(subject)
     db.session.commit()
     admin=Admin.query.first()
     flash('Subject added successfully!!')
     return redirect(url_for('admin_dashboard'))

@app.route('/display/chapters/<int:id>/')
@admin_auth
def display_chap(id):
     subject=Subject.query.get(id)

     query=request.args.get('query')
     if query:
            chapters=Chapter.query.filter(Chapter.Name.ilike(f'%{query}%'))
            return render_template('chap.html',subject=subject,chapters=chapters)

     chapters=Chapter.query.filter_by(subject_id=id)
     return render_template('chap.html',subject=subject,chapters=chapters)

@app.route('/edit/subject/<int:id>/')
@admin_auth
def edit_sub(id):
     subject=Subject.query.get(id)
     return render_template('edit_sub.html',subject=subject)

@app.route('/edit/subject/<int:id>/',methods=['POST'])
@admin_auth
def edit_sub_post(id):
     sub=Subject.query.get(id)
     name=request.form.get('Name')
     des=request.form.get('Description')
     if not name or not des:
          flash("Filling out all the fields is mandatory")
          return redirect(url_for('edit_sub',id=id))
     sub.Name=name
     sub.Description=des
     db.session.commit()
     admin=Admin.query.first()
     flash('Updated subject successfully!!')
     return redirect(url_for('admin_dashboard'))

@app.route('/delete/subject/<int:id>/')
@admin_auth
def delete_sub(id):
     sub=Subject.query.get(id)
     if sub:
        db.session.delete(sub)
        db.session.commit()
     admin=Admin.query.first()
     flash('Subject deleted Successfully!!')
     return redirect(url_for('admin_dashboard'))

@app.route('/add/chapter/<int:id>')
@admin_auth
def add_chap(id):
     return render_template('add_chap.html')

@app.route('/add/chapter/<int:id>',methods=['POST'])
@admin_auth
def add_chap_post(id):
     chap_name=request.form.get('Name')
     des=request.form.get('Description')

     if not chap_name or not des:
          flash("Filling out all the fields is mandatory")
          return redirect(url_for('add_chap',id=id))

     chapter=Chapter(Name=chap_name,Description=des,subject_id=id)
     db.session.add(chapter)
     db.session.commit()
    
     sub=Subject.query.get(id)

     flash(chapter.Name+' Chapter added successfully to the '+ sub.Name + ' subject!!')
     return redirect(url_for('display_chap',id=id))


@app.route('/edit/chapter/<int:id>')
@admin_auth
def edit_chap(id):
     chap=Chapter.query.get(id)
     return render_template('edit_chap.html',chapter=chap)

@app.route('/edit/chapter/<int:id>/',methods=['POST'])
@admin_auth
def edit_chap_post(id):
     chap=Chapter.query.get(id)
     name=request.form.get('Name')
     des=request.form.get('Description')
     if not name or not des:
          flash("Filling out all the fields is mandatory")
          return redirect(url_for('edit_chap',id=id))
     chap.Name=name
     chap.Description=des
     db.session.commit()
     flash('Updated chapter successfully!!')
     return redirect(url_for('display_chap',id=chap.subject_id))

@app.route('/delete/chap/<int:id>')
@admin_auth
def delete_chap(id):
     
     chapter=Chapter.query.get(id)
     sub_id=chapter.subject_id

     if chapter:
        db.session.delete(chapter)
        db.session.commit()
    
     flash('Chapter deleted successfully!!')
     return redirect(url_for('display_chap',id=sub_id))



@app.route('/display/quizzes/<int:id>')
@admin_auth
def display_quiz(id):
     chapter=Chapter.query.get(id)
     
     parameter=request.args.get('parameter')
     query=request.args.get('query')

     if parameter=="date":
          quizzes=Quiz.query.filter(Quiz.date_of_quiz.ilike(f'%{query}%'),Quiz.chapter_id==id).all()
          return render_template('quiz.html',quizzes=quizzes,chapter=chapter)
     
     if parameter=="id":
          quizzes=Quiz.query.filter(Quiz.id==query,Quiz.chapter_id==id).all()
          return render_template('quiz.html',quizzes=quizzes,chapter=chapter)
     
     if parameter=="marks":
          quizzes=Quiz.query.filter(Quiz.total_marks==query,Quiz.chapter_id==id).all()
          print(query)
          return render_template('quiz.html',quizzes=quizzes,chapter=chapter)

     quizzes=Quiz.query.filter_by(chapter_id=id).order_by(Quiz.date_of_quiz.desc()).all()
     return render_template('quiz.html',quizzes=quizzes,chapter=chapter)

@app.route('/add/quiz/<int:id>')
@admin_auth
def add_quiz(id):
     return render_template('add_quiz.html')

@app.route('/add/quiz/<int:id>',methods=['POST'])
@admin_auth
def add_quiz_post(id):
    dur_str=request.form.get('Duration')
    date_sche_str=request.form.get('Date')
    rem=request.form.get('Remarks')
    tot_marks=request.form.get('tot_marks')
    qual_marks=request.form.get('Q_marks')

    date_sche=datetime.strptime(date_sche_str, '%Y-%m-%d').date()
    pattern = r"^([0-4]):([0-5][0-9])$"

    if not dur_str or not date_sche_str or not tot_marks:
        flash("Filling out Duration,Scheduled Date and Total marks fields is mandatory")
        return redirect(url_for('add_quiz',id=id))
    
    if not re.match(pattern, dur_str):
        flash("Invalid time format! Use h:mm and max 5 hours.")
        return redirect(url_for("add_quiz",id=id))

    quiz=Quiz(chapter_id=id,date_of_quiz=date_sche,time_duration=dur_str,Remarks=rem,total_marks=tot_marks,Qualifying_marks=qual_marks)
    db.session.add(quiz)
    db.session.commit()
    
    chap=Chapter.query.get(id)

    flash('Quiz added successfully to the '+ chap.Name + ' chapter!!')
    return redirect(url_for('display_quiz',id=id))


@app.route('/display/questions/<int:id>/')
@admin_auth
def display_questions(id):
     quiz=Quiz.query.get(id)

     parameter=request.args.get('parameter')
     query=request.args.get('query')

     if parameter=="question":
          questions=Questions.query.filter(Questions.question_statement.ilike(f'%{query}%'),Questions.quiz_id==id)
          return render_template('questions.html',quiz=quiz,questions=questions)
     
     if parameter=="id":
          questions=Questions.query.filter(Questions.id==query,Questions.quiz_id==id)
          return render_template('questions.html',quiz=quiz,questions=questions)
     
     questions=Questions.query.filter_by(quiz_id=id)
     return render_template('questions.html',quiz=quiz,questions=questions)


@app.route('/edit/quiz/<int:id>')
@admin_auth
def edit_quiz(id):
     quiz=Quiz.query.get(id)
     return render_template('edit_quiz.html',quiz=quiz)

@app.route('/edit/quiz/<int:id>',methods=['POST'])
@admin_auth
def edit_quiz_post(id):
    dur_str=request.form.get('Duration')
    date_sche_str=request.form.get('Date')
    rem=request.form.get('Remarks')
    tot_marks=request.form.get('tot_marks')
    qual_marks=request.form.get('Q_marks')

    date_sche=datetime.strptime(date_sche_str, '%Y-%m-%d').date()
    pattern = r"^([0-4]):([0-5][0-9])$"

    if not dur_str or not date_sche_str or not tot_marks:
        flash("Filling out Duration,Scheduled Date and Total marks fields is mandatory")
        return redirect(url_for('edit_quiz',id=id))
    
    if not re.match(pattern, dur_str):
        flash("Invalid time format! Use h:mm and max 5 hours.")
        return redirect(url_for("edit_quiz",id=id))

    quiz=Quiz.query.get(id)
    quiz.date_of_quiz=date_sche
    quiz.time_duration=dur_str
    quiz.Remarks=rem
    quiz.Qualifying_marks=qual_marks
    quiz.total_marks=tot_marks
    db.session.commit()
    
    chap_id=quiz.chapter_id

    flash('Quiz editted successfully!!')
    return redirect(url_for('display_quiz',id=chap_id))


@app.route('/delete/quiz/<int:id>')
@admin_auth
def delete_quiz(id):
    quiz=Quiz.query.get(id)
    
    if quiz:
        db.session.delete(quiz)
        db.session.commit()
    
    flash('Quiz deleted successfully!!')
    
    return redirect(url_for('display_quiz',id=quiz.chapter_id))

@app.route('/edit/question/<int:id>')
@admin_auth
def edit_question(id):
     question=Questions.query.get(id)
     return render_template('edit_question.html',question=question)


@app.route('/edit/question/<int:id>',methods=['POST'])
@admin_auth
def edit_question_post(id):
    ques_stmt=request.form.get('q_stmt')
    o1=request.form.get('op1')
    o2=request.form.get('op2')
    o3=request.form.get('op3')
    o4=request.form.get('op4')
    ans_op=request.form.get('ans_op')
    ans=request.form.get('ans')

    if not ques_stmt or not o1 or not o2 or not o3 or not o4 or not ans_op:
        flash("Filling out all the fields is mandatory")
        return redirect(url_for('edit_question',id=id))
    
    question=Questions.query.get(id)
    question.question_statement=ques_stmt
    question.Option_1=o1
    question.Option_2=o2
    question.Option_3=o3
    question.Option_4=o4
    question.Answer_option_no=ans_op
    question.Answer=ans

    db.session.commit()
    
    quiz_id=question.quiz_id

    flash('Question editted successfully!!')
    return redirect(url_for('display_questions',id=quiz_id))

@app.route('/add/question/<int:id>')
@admin_auth
def add_question(id):
     return render_template('add_question.html')

@app.route('/add/question/<int:id>',methods=['POST'])
@admin_auth
def add_question_post(id):
    ques_stmt=request.form.get('q_stmt')
    o1=request.form.get('op1')
    o2=request.form.get('op2')
    o3=request.form.get('op3')
    o4=request.form.get('op4')
    ans_op=request.form.get('ans_op')
    ans=request.form.get('ans')

    if not ques_stmt or not o1 or not o2 or not o3 or not o4 or not ans_op or not ans:
        flash("Filling out all the fields is mandatory")
        return redirect(url_for('add_question',id=id))

    question=Questions(Answer=ans,quiz_id=id,question_statement=ques_stmt,Option_1=o1,Option_2=o2,Option_3=o3,Option_4=o4,Answer_option_no=ans_op)
    db.session.add(question)
    db.session.commit()

    flash('Question added successfully to the Quiz!!')
    return redirect(url_for('display_questions',id=id))

@app.route('/delete/question/<int:id>')
@admin_auth
def delete_question(id):
     question=Questions.query.get(id)
     

     if question:
        db.session.delete(question)
        db.session.commit()
    
     flash('Question deleted successfully!!')

     return redirect(url_for('display_questions',id=question.quiz_id))

@app.route('/display/user_details')
@admin_auth
def display_user_details():

     parameter=request.args.get('parameter')
     query=request.args.get('query')

     if parameter=='name':
          users=User.query.filter(User.Full_Name.ilike(f'%{query}%')).all()
          return render_template('user_details.html',users=users)
     if parameter=='id':
          users=User.query.filter(User.id.ilike(f'%{query}%')).all()
          return render_template('user_details.html',users=users)

     if parameter=='username':
          users=User.query.filter(User.username.ilike(f'%{query}%')).all()
          return render_template('user_details.html',users=users)

     users=User.query.all()
     return render_template('user_details.html',users=users)

@app.route('/display/chapters/user/<int:id>')
@user_auth
def display_chap_user(id):
     subject=Subject.query.get(id)

     query=request.args.get('query')
     if query:
            chapters=Chapter.query.filter(Chapter.Name.ilike(f'%{query}%'))
            return render_template('chap_user.html',subject=subject,chapters=chapters)
     
     chapters=Chapter.query.filter_by(subject_id=id)
     return render_template('chap_user.html',chapters=chapters,subject=subject)

@app.route('/display/quiz/user/<int:id>')
@user_auth
def display_quiz_user(id):
     chapter=Chapter.query.get(id)

     parameter=request.args.get('parameter')
     query=request.args.get('query')
     today=date.today()
     if parameter=="date":
          quizzes=Quiz.query.filter(Quiz.date_of_quiz.ilike(f'%{query}%'),Quiz.chapter_id==id).all()
          return render_template('quiz_user.html',today=today,quizzes=quizzes,chapter=chapter)
     
     if parameter=="id":
          quizzes=Quiz.query.filter(Quiz.id==query,Quiz.chapter_id==id).all()
          return render_template('quiz_user.html',today=today,quizzes=quizzes,chapter=chapter)
     
     if parameter=="marks":
          quizzes=Quiz.query.filter(Quiz.total_marks==query,Quiz.chapter_id==id).all()
          return render_template('quiz_user.html',today=today,quizzes=quizzes,chapter=chapter)
     
     quizzes=Quiz.query.filter_by(chapter_id=id).order_by(Quiz.date_of_quiz.desc()).all()
     
     return render_template('quiz_user.html',today=today,quizzes=quizzes,chapter=chapter)

@app.route('/display/questions/user/<int:id>')
@user_auth
def display_questions_user(id):
     questions=Questions.query.filter_by(quiz_id=id)
     quiz=Quiz.query.get(id)
     return render_template('questions_user.html',questions=questions,quiz=quiz)

@app.route('/display/questions/user/<int:id>',methods=['POST'])
@user_auth
def display_questions_user_post(id):
     questions=Questions.query.filter_by(quiz_id=id)
     quiz=Quiz.query.get(id)
     marks=[]
     user_response=[]
     correct_answer=[]
     is_passed=True
     for question in questions:
          ans=request.form.get(f'{question.id}')
          user_response.append(ans)
          correct_answer.append(question.Answer)
          if ans and int(ans)==question.Answer_option_no:
               marks.append(1)
          else:
               marks.append(0)
     score=sum(marks)
     if quiz.Qualifying_marks:
          if score<quiz.Qualifying_marks:
               is_passed=False
     user_id = session.get('user_id')
     timestamp=datetime.now()
     if is_passed:
          status='passed'
     else:
          status='failed'
     score_db=Scores(time_stamp_of_event=timestamp,user_id=user_id,quiz_id=quiz.id,total_scored=score,is_passed=is_passed)
     db.session.add(score_db)  
     db.session.commit()
       
     return render_template('display_result.html',status=status,questions=questions,quiz=quiz,score=score,user_response=user_response,correct_answer=correct_answer,marks=marks)

@app.route('/display/past_quiz_attempts/user/<int:quiz_id>')
@user_auth
def display_past_quiz_attempts_user(quiz_id):
     user_id=session.get('user_id')
     user=User.query.get(user_id)
     quiz=Quiz.query.get(quiz_id)
     attempts=Scores.query.filter_by(user_id=user_id,quiz_id=quiz_id).order_by(Scores.time_stamp_of_event.desc()).all()
     tot_attempts = len(attempts)
     avg = sum(a.total_scored for a in attempts) / tot_attempts if tot_attempts > 0 else 0
     avg_score=round(avg)
     return render_template('display_attempts_user.html',avg_score=avg_score,attempts=attempts,quiz=quiz,user=user)

@app.route('/display/quiz_details/<int:quiz_id>')
@user_auth
def display_quiz_details(quiz_id):
     
     quiz=Quiz.query.get(quiz_id)
     chap_id=quiz.chapter_id
     chapter=Chapter.query.get(chap_id)
     subject=Subject.query.get(chapter.subject_id)
     chap_name=chapter.Name

     return render_template('quiz_details.html',subject=subject,ch_name=chap_name,quiz=quiz)


    
     




