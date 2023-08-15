from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, Points, Rank, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from .questions import *


auth = Blueprint('auth', __name__)


@auth.route('/')
def index():  # put application's code here
    return redirect('/20_marcinek/licencjat/mainPage')

@auth.route('/projektowanie')
def projektowanie():
    return render_template('projektowanie.html', user=current_user)

@auth.route('/grafika')
def grafika():
    return render_template('grafika.html', user=current_user)

@auth.route('/progress')
@login_required
def progress():
    CU_name=current_user.first_name
    x=None
    tt1=Points.query.filter_by(data='QUIZ1 - wprowadzenie').join(User).filter_by(first_name=CU_name).order_by(Points.points.desc()).first()
    if (tt1==x):
        tt1='Nie brałeś udziału'
    else:
        tt1=tt1.points
    tt2=Points.query.filter_by(data='QUIZ2 - parametry techniczne stron').join(User).filter_by(first_name=CU_name).order_by(Points.points.desc()).first()
    if (tt2==x):
        tt2='Nie brałeś udziału'
    else:
        tt2=tt2.points

    #### USUWANIE STRINGÓW Z WYNIKÓW ZEBY MÓC ZSUMOWAĆ
    lista_braku_udzialu_INT=[]
    lista_braku_udzialu=[tt1,tt2]
    for i in range(len(lista_braku_udzialu)):
        if lista_braku_udzialu[i] == 'Nie brałeś udziału':
            lista_braku_udzialu[i] = 0
    for element in lista_braku_udzialu:
        lista_braku_udzialu_INT.append(int(element))


    suma = sum(lista_braku_udzialu_INT)


    if Rank.query.filter_by(name=CU_name).first()==None:
        new_rank = Rank(name=current_user.first_name, rank_points=suma)  # Provide the user_id
        db.session.add(new_rank)
        db.session.commit()
    else:
        Rank.query.filter_by(name=CU_name).update({Rank.rank_points: suma})
        db.session.commit()

    ####################
    return render_template('progress.html',tt1=tt1,tt2=tt2, user=current_user)


@auth.route('/rank')
def rank():
    rankall = Rank.query.order_by(Rank.rank_points.desc()).limit(10).all()

    brakujace_elementy = 10 - len(rankall)
    if brakujace_elementy > 0:
        rankall.extend([''] * brakujace_elementy)
    rank1 = rankall[0]
    rank2 = rankall[1]
    rank3 = rankall[2]
    rank4 = rankall[3]
    rank5 = rankall[4]
    rank6 = rankall[5]
    rank7 = rankall[6]
    rank8 = rankall[7]
    rank9 = rankall[8]
    rank10 = rankall[9]
    check_your_rank = Rank.query.order_by(Rank.rank_points.desc()).all()
    rank_plaec_CU = 1
    for i in range(len(check_your_rank)):
        if check_your_rank[i].name == current_user.first_name:
            break
        else:
            rank_plaec_CU += 1

    your_rank = Rank.query.filter_by(name=current_user.first_name).first()
    return render_template('rank.html', rank1=rank1, rank2=rank2, your_rank=your_rank, rank3=rank3, rank4=rank4,
                           rank5=rank5, rank6=rank6, rank7=rank7, rank8=rank8, rank9=rank9, rank10=rank10,
                           user=current_user, rank_plaec_CU=rank_plaec_CU)


@auth.route('/refresh_rank')
def refresh_rank():
    CU_name = current_user.first_name
    x = None
    tt1 = Points.query.filter_by(data='QUIZ1 - wprowadzenie').join(User).filter_by(first_name=CU_name).order_by(
        Points.points.desc()).first()
    if (tt1 == x):
        tt1 = 'Nie brałeś udziału'
    else:
        tt1 = tt1.points
    tt2 = Points.query.filter_by(data='QUIZ2 - parametry techniczne stron').join(User).filter_by(first_name=CU_name).order_by(
        Points.points.desc()).first()
    if (tt2 == x):
        tt2 = 'Nie brałeś udziału'
    else:
        tt2 = tt2.points

        #### USUWANIE STRINGÓW Z WYNIKÓW ZEBY MÓC ZSUMOWAĆ
    lista_braku_udzialu_INT = []
    lista_braku_udzialu = [tt1, tt2]
    for i in range(len(lista_braku_udzialu)):
        if lista_braku_udzialu[i] == 'Nie brałeś udziału':
            lista_braku_udzialu[i] = 0
    for element in lista_braku_udzialu:
        lista_braku_udzialu_INT.append(int(element))

    suma = sum(lista_braku_udzialu_INT)

    if Rank.query.filter_by(name=CU_name).first() == None:
        new_rank = Rank(name=current_user.first_name, rank_points=suma)  # Provide the user_id
        db.session.add(new_rank)
        db.session.commit()
    else:
        Rank.query.filter_by(name=CU_name).update({Rank.rank_points: suma})
        db.session.commit()

    return redirect(url_for('auth.rank'))

@auth.route('/course')
def course():
    return render_template('course.html', user=current_user)


@auth.route('/forum', methods=['GET', 'POST'])
def forum():

    if request.method == 'POST':
        note = request.form.get('note')  # Gets the note from the HTML

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.first_name)  # providing the schema for the note
            db.session.add(new_note)  # adding the note to the database
            db.session.commit()
            flash('Note added!', category='success')


    all_notes = Note.query.all()

    return render_template('forum.html', user=current_user, notes=all_notes)

@auth.route('/quizFig')
def quizFig():
    return render_template('quizFig.html', user=current_user)

@auth.route('/quizProj')
def quizProj():
    return render_template('quizProj.html', user=current_user )

@auth.route('/quizy')
def quiz():
    return render_template('quiz.html', user=current_user)


@auth.route('/test1', methods=['GET', 'POST'])
def test1():
    nazwa='QUIZ1 - wprowadzenie'
    if 'question_index' not in session:
        session['question_index'] = 0
        session['points'] = 0

    if request.method == 'POST':
        odpowiedzi = request.form
        current_question = DANE1[session['question_index']]

        if odpowiedzi.get('odpowiedz') == current_question['odpok']:
            session['points'] += 1

        session['question_index'] += 1

        if session['question_index'] >= len(DANE1):
            points = session['points']
            session.pop('question_index')
            session.pop('points')

            if current_user.is_authenticated:
                new_points = Points(user_id=current_user.id, points=points, data=nazwa)  # Provide the user_id
                db.session.add(new_points)
                db.session.commit()

            flash('Liczba poprawnych odpowiedzi, to: {0}'.format(points))
            return redirect(url_for('auth.wynik'))

    if 'question_index' in session:
        current_question = DANE1[session['question_index']]
        return render_template('test1.html', pytanie=current_question, user=current_user)

    return redirect(url_for('/wynik'))

@auth.route('/test2', methods=['GET', 'POST'])
def test2():
    nazwa='QUIZ2 - parametry techniczne stron'
    if 'question_index' not in session:
        session['question_index'] = 0
        session['points'] = 0

    if request.method == 'POST':
        odpowiedzi = request.form
        current_question = DANE2[session['question_index']]

        if odpowiedzi.get('odpowiedz') == current_question['odpok']:
            session['points'] += 1

        session['question_index'] += 1

        if session['question_index'] >= len(DANE2):
            points = session['points']
            session.pop('question_index')
            session.pop('points')

            if current_user.is_authenticated:
                new_points = Points(user_id=current_user.id, points=points, data=nazwa)  # Provide the user_id
                db.session.add(new_points)
                db.session.commit()

            flash('Liczba poprawnych odpowiedzi, to: {0}'.format(points))
            return redirect(url_for('auth.wynik'))

    if 'question_index' in session:
        current_question = DANE2[session['question_index']]
        return render_template('test2.html', pytanie=current_question, user=current_user)

    return redirect(url_for('/wynik'))

@auth.route('/wynik')
def wynik():
    return render_template('wynik.html', user=current_user)


###########################

@auth.route('/adminpanel')
def adminpanel():
    return render_template('adminpanel.html', user=current_user)


@auth.route('/mainPage')
def mainPage():
    return render_template("mainPage.html", user=current_user)

@auth.route('/contact')
def contact():

    return render_template("contact.html", user=current_user)

@auth.before_request
def restrict_access_to_auth_routes():
    if current_user.is_authenticated and request.endpoint in ['auth.login', 'auth.sign_up']:
        return redirect(url_for('auth.mainPage'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect('mainPage')
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        name=User.query.filter_by(first_name=first_name).first()
        if user:
            flash('Email already exists.', category='error')
        elif name:
            flash('Name already exist.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("signup.html", user=current_user)

@auth.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password1 = request.form.get('new_password1')
        new_password2 = request.form.get('new_password2')

        if not check_password_hash(current_user.password, old_password):
            flash('Incorrect old password.', category='error')
        elif new_password1 != new_password2:
            flash('New passwords don\'t match.', category='error')
        elif len(new_password1) < 7:
            flash('New password must be at least 7 characters.', category='error')
        else:
            current_user.password = generate_password_hash(new_password1, method='sha256')
            db.session.commit()
            flash('Password changed successfully!', category='success')
            return redirect(url_for('auth.mainPage'))

    return render_template("changepassword.html", user=current_user)