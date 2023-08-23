from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, Points, Rank, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from .questions import *


auth = Blueprint('auth', __name__)

# ścieżka do strony głównej na serwerze limba.wzks.uj.edu.pl

@auth.route('/')
def index():  # put application's code here
    return redirect('/20_marcinek/licencjat/mainPage')

# ścieżka do strony głównej

@auth.route('/mainPage')
def mainPage():
    return render_template("mainPage.html", user=current_user)

# ścieżka do strony z nauką

@auth.route('/course')
def course():
    return render_template('course.html', user=current_user)

# ścieżka do podstrony z materiałami do nauki z projektowania stron

@auth.route('/projektowanie')
def projektowanie():
    return render_template('projektowanie.html', user=current_user)

@auth.route('/proj1')
def proj1():
    return render_template('proj1.html', user=current_user)

@auth.route('/proj2')
def proj2():
    return render_template('proj2.html', user=current_user)

@auth.route('/proj3')
def proj3():
    return render_template('proj3.html', user=current_user)

@auth.route('/proj4')
def proj4():
    return render_template('proj4.html', user=current_user)

# ścieżka do podstrony z materiałami do nauki z programów graficznych

@auth.route('/grafika')
def grafika():
    return render_template('grafika.html', user=current_user)

# śledzenie postępów

@auth.route('/progress')
@login_required
def progress():
    CU_name=current_user.first_name
    x=None
    tt1=Points.query.filter_by(data='QUIZ1 - wprowadzenie').join(User).filter_by(first_name=CU_name).order_by(Points.points.desc()).first() ###tutaj skopiować
    if (tt1==x):###
        tt1='Nie brałeś udziału'###
    else:###
        tt1=tt1.points###
    tt2=Points.query.filter_by(data='QUIZ2 - parametry techniczne stron').join(User).filter_by(first_name=CU_name).order_by(Points.points.desc()).first()
    if (tt2==x):
        tt2='Nie brałeś udziału'
    else:
        tt2=tt2.points
    tt3 = Points.query.filter_by(data='QUIZ1 - Figma wprowadzenie').join(User).filter_by(
        first_name=CU_name).order_by(Points.points.desc()).first()
    if (tt3 == x):
        tt3 = 'Nie brałeś udziału'
    else:
        tt3 = tt3.points
    tt4 = Points.query.filter_by(data='QUIZ2 - Figma funkcje i narzędzia').join(User).filter_by(
        first_name=CU_name).order_by(Points.points.desc()).first()
    if (tt4 == x):
        tt4 = 'Nie brałeś udziału'
    else:
        tt4 = tt4.points
    tt5 = Points.query.filter_by(data='QUIZ3 - Figma skróty klawiaturowe').join(User).filter_by(
        first_name=CU_name).order_by(Points.points.desc()).first()
    if (tt5 == x):
        tt5 = 'Nie brałeś udziału'
    else:
        tt5 = tt5.points

    #### USUWANIE STRINGÓW Z WYNIKÓW ZEBY MÓC ZSUMOWAĆ
    lista_braku_udzialu_INT=[]
    lista_braku_udzialu=[tt1,tt2,tt3,tt4,tt5] ###tutaj zmienić
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


    return render_template('progress.html',tt1=tt1,tt2=tt2,tt3=tt3,tt4=tt4,tt5=tt5, user=current_user)###tutaj pododawać

# ranking

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
    if current_user.is_authenticated:
        check_your_rank = Rank.query.order_by(Rank.rank_points.desc()).all()
        rank_plaec_CU = 1
        for i in range(len(check_your_rank)):
            if check_your_rank[i].name == current_user.first_name:
                break
            else:
                rank_plaec_CU += 1

        your_rank = Rank.query.filter_by(name=current_user.first_name).first()
    else:
        your_rank = ''
        rank_plaec_CU = ''
    return render_template('rank.html', rank1=rank1, rank2=rank2, your_rank=your_rank, rank3=rank3, rank4=rank4,
                           rank5=rank5, rank6=rank6, rank7=rank7, rank8=rank8, rank9=rank9, rank10=rank10,
                           user=current_user, rank_plaec_CU=rank_plaec_CU)

# odświeżanie rankingu

@auth.route('/refresh_rank')
@login_required
def refresh_rank():
    CU_name = current_user.first_name
    x = None
    tt1 = Points.query.filter_by(data='QUIZ1 - wprowadzenie').join(User).filter_by(first_name=CU_name).order_by(Points.points.desc()).first()###tu
    if (tt1 == x):###
        tt1 = 'Nie brałeś udziału'###
    else:###
        tt1 = tt1.points###tu
    tt2 = Points.query.filter_by(data='QUIZ2 - parametry techniczne stron').join(User).filter_by(first_name=CU_name).order_by(Points.points.desc()).first()
    if (tt2 == x):
        tt2 = 'Nie brałeś udziału'
    else:
        tt2 = tt2.points
    tt3 = Points.query.filter_by(data='QUIZ1 - Figma wprowadzenie').join(User).filter_by(
        first_name=CU_name).order_by(Points.points.desc()).first()
    if (tt3 == x):
        tt3 = 'Nie brałeś udziału'
    else:
        tt3 = tt3.points
    tt4 = Points.query.filter_by(data='QUIZ2 - Figma funkcje i narzędzia').join(User).filter_by(
        first_name=CU_name).order_by(Points.points.desc()).first()
    if (tt4 == x):
        tt4 = 'Nie brałeś udziału'
    else:
        tt4 = tt4.points
    tt5 = Points.query.filter_by(data='QUIZ3 - Figma skróty klawiaturowe').join(User).filter_by(
        first_name=CU_name).order_by(Points.points.desc()).first()
    if (tt5 == x):
        tt5 = 'Nie brałeś udziału'
    else:
        tt5 = tt5.points

 # USUWANIE STRINGÓW Z WYNIKÓW ZEBY MÓC ZSUMOWAĆ

    lista_braku_udzialu_INT = []
    lista_braku_udzialu = [tt1, tt2, tt3, tt4, tt5]###tutaj
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

# forum z postami użytkowników

@auth.route('/forum', methods=['GET', 'POST'])
def forum():

    if request.method == 'POST':
        note = request.form.get('note')  # Gets the note from the HTML

        if len(note) < 3:
            flash('Wpis jest zbyt krótki!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.first_name)  # providing the schema for the note
            db.session.add(new_note)  # adding the note to the database
            db.session.commit()
            flash('Dodano wpis!', category='success')


    all_notes = Note.query.all()

    return render_template('forum.html', user=current_user, notes=all_notes)

# usuwanie wpisów z forum

@auth.route('/delete_note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)

    # Check if the current user is the owner of the note
    if note.user_id == current_user.first_name or current_user.first_name == 'admin':
        db.session.delete(note)
        db.session.commit()
        flash('Usunięto wpis!', category='success')
    else:
        flash('Nie masz uprawnień żeby usunąć ten wpis.', category='error')

    return redirect(url_for('auth.forum'))

# ścieżka do strony z quizami

@auth.route('/quizy')
def quiz():
    return render_template('quiz.html', user=current_user)

# podstrona dla quizów z pogramów graficznych

@auth.route('/quizFig')
def quizFig():
    return render_template('quizFig.html', user=current_user)

# podstrona z quizami do projektowania

@auth.route('/quizProj')
def quizProj():
    return render_template('quizProj.html', user=current_user )

# quiz1

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

            flash('Liczba poprawnych odpowiedzi, to: {0}'.format(points), category='success')
            return redirect(url_for('auth.progress'))

    if 'question_index' in session:
        current_question = DANE1[session['question_index']]
        return render_template('test1.html', pytanie=current_question, user=current_user)


# quiz2

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
            return redirect(url_for('auth.progress'))

    if 'question_index' in session:
        current_question = DANE2[session['question_index']]
        return render_template('test2.html', pytanie=current_question, user=current_user)


@auth.route('/testf1', methods=['GET', 'POST'])
def testf1():
    nazwa='QUIZ1 - Figma wprowadzenie'
    if 'question_index' not in session:
        session['question_index'] = 0
        session['points'] = 0

    if request.method == 'POST':
        odpowiedzi = request.form
        current_question = DANEF1[session['question_index']]

        if odpowiedzi.get('odpowiedz') == current_question['odpok']:
            session['points'] += 1

        session['question_index'] += 1

        if session['question_index'] >= len(DANEF1):
            points = session['points']
            session.pop('question_index')
            session.pop('points')

            if current_user.is_authenticated:
                new_points = Points(user_id=current_user.id, points=points, data=nazwa)  # Provide the user_id
                db.session.add(new_points)
                db.session.commit()

            flash('Liczba poprawnych odpowiedzi, to: {0}'.format(points), category='success')
            return redirect(url_for('auth.progress'))

    if 'question_index' in session:
        current_question = DANEF1[session['question_index']]
        return render_template('testf1.html', pytanie=current_question, user=current_user)


@auth.route('/testf2', methods=['GET', 'POST'])
def testf2():
    nazwa='QUIZ2 - Figma funkcje i narzędzia'
    if 'question_index' not in session:
        session['question_index'] = 0
        session['points'] = 0

    if request.method == 'POST':
        odpowiedzi = request.form
        current_question = DANEF2[session['question_index']]

        if odpowiedzi.get('odpowiedz') == current_question['odpok']:
            session['points'] += 1

        session['question_index'] += 1

        if session['question_index'] >= len(DANEF2):
            points = session['points']
            session.pop('question_index')
            session.pop('points')

            if current_user.is_authenticated:
                new_points = Points(user_id=current_user.id, points=points, data=nazwa)  # Provide the user_id
                db.session.add(new_points)
                db.session.commit()

            flash('Liczba poprawnych odpowiedzi, to: {0}'.format(points), category='success')
            return redirect(url_for('auth.progress'))

    if 'question_index' in session:
        current_question = DANEF2[session['question_index']]
        return render_template('testf2.html', pytanie=current_question, user=current_user)

@auth.route('/testf3', methods=['GET', 'POST'])
def testf3():
    nazwa='QUIZ3 - Figma skróty klawiaturowe'
    if 'question_index' not in session:
        session['question_index'] = 0
        session['points'] = 0

    if request.method == 'POST':
        odpowiedzi = request.form
        current_question = DANEF3[session['question_index']]

        if odpowiedzi.get('odpowiedz') == current_question['odpok']:
            session['points'] += 1

        session['question_index'] += 1

        if session['question_index'] >= len(DANEF3):
            points = session['points']
            session.pop('question_index')
            session.pop('points')

            if current_user.is_authenticated:
                new_points = Points(user_id=current_user.id, points=points, data=nazwa)  # Provide the user_id
                db.session.add(new_points)
                db.session.commit()

            flash('Liczba poprawnych odpowiedzi, to: {0}'.format(points), category='success')
            return redirect(url_for('auth.progress'))

    if 'question_index' in session:
        current_question = DANEF3[session['question_index']]
        return render_template('testf3.html', pytanie=current_question, user=current_user)

# panel administratora

@auth.route('/adminpanel')
@login_required
def adminpanel():
    if current_user.first_name != 'admin':
        return redirect(url_for('auth.mainPage'))

    all_users = User.query.all()
    return render_template('adminpanel.html', user=current_user, users=all_users)

# zarządzanie użytkownikami

@auth.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    Rank.query.filter_by(name=user.first_name).delete()
    Note.query.filter_by(user_id=user.first_name).delete()
    Points.query.filter_by(user_id=user.id).delete()

    # Delete the user
    db.session.delete(user)
    db.session.commit()
    flash('Poprawnie usunięto użytkownika powiązane z nim dane.', category='success')
    flash('Akcja zakończona niepowodzeniem.', category='error')
    return redirect(url_for('auth.adminpanel'))


# formualrz kontaktowy

@auth.route('/contact')
@login_required
def contact():

    return render_template("contact.html", user=current_user)

@auth.route('/contact_refresh', methods=['GET'])
@login_required
def contact_refresh():
    flash('Wiadomość wysłana.', category='success')
    return redirect(url_for('auth.contact'))


@auth.before_request
def restrict_access_to_auth_routes():
    if current_user.is_authenticated and request.endpoint in ['auth.login', 'auth.sign_up']:
        return redirect(url_for('auth.mainPage'))

# logowanie użytkownika

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Zalogowano!', category='success')
                login_user(user, remember=True)
                return redirect('mainPage')
            else:
                flash('Niepoprawne hasło.', category='error')
        else:
            flash('Podany email nie istnieje.', category='error')

    return render_template('login.html', user=current_user)

# wylogowanie użytkownika

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Wylogowano.', category='success')
    return redirect(url_for('auth.login'))

# rejestracja użytkownika

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
            flash('Podany email już istnieje. Podaj inny.', category='error')
        elif name:
            flash('Podany login już istnieje. Podaj inny.', category='error')
        elif len(email) < 4:
            flash('Email musi mieć przynajmniej 4 znaki.', category='error')
        elif len(first_name) < 2:
            flash('Login musi mieć przynajmniej 2 znaki.', category='error')
        elif password1 != password2:
            flash('Podane hasła nie są identyczne.', category='error')
        elif len(password1) < 8:
            flash('Hasło musi mieć co najmniej 8 znaków.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Utworzono konto!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("signup.html", user=current_user)

# zmiana hasła użytkownika


@auth.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password1 = request.form.get('new_password1')
        new_password2 = request.form.get('new_password2')

        if not check_password_hash(current_user.password, old_password):
            flash('Niepoprawne hasło.', category='error')
        elif new_password1 != new_password2:
            flash('Podane hasła nie są identyczne.', category='error')
        elif len(new_password1) < 7:
            flash('Hasło musi mieć co najmniej 8 znaków.', category='error')
        else:
            current_user.password = generate_password_hash(new_password1, method='sha256')
            db.session.commit()
            flash('Hasło zostało zmienione!', category='success')
            return redirect(url_for('auth.mainPage'))

    return render_template("changepassword.html", user=current_user)