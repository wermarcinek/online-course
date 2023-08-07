from flask import Flask, request, redirect, url_for, flash, render_template, session

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY='haslo',
))

@app.route('/')
def index():  # put application's code here
    return redirect('/20_marcinek/licencjat/mainPage')

@app.route('/mainPage')
def mainPage():
    return render_template('mainPage.html')

@app.route('/course')
def course():
    return render_template('course.html')

@app.route('/grafika')
def grafika():
    return render_template('grafika.html')

@app.route('/projektowanie')
def projektowanie():
    return render_template('projektowanie.html')

@app.route('/quizy')
def quiz():
    return render_template('quiz.html')

@app.route('/progress')
def progress():
    return render_template('progress.html')

#########
DANE = [{
    'pytanie': 'Ile pikseli szerokości powinien mieć layout strony internetowej:',  # pytanie
    'odpowiedzi': ['1200', '1600', '1800'],  # możliwe odpowiedzi
    'odpok': '1200'},  # poprawna odpowiedź
    {
    'pytanie': 'Objętość sześcianu o boku 6 cm, wynosi:',
    'odpowiedzi': ['36', '216', '18'],
    'odpok': '216'},
    {
    'pytanie': 'Symbol pierwiastka Helu, to:',
    'odpowiedzi': ['Fe', 'H', 'He'],
    'odpok': 'He'},
]

#########
@app.route('/test', methods=['GET', 'POST'])
def test():
    if 'question_index' not in session:
        session['question_index'] = 0
        session['points'] = 0

    if request.method == 'POST':
        odpowiedzi = request.form
        current_question = DANE[session['question_index']]

        if odpowiedzi.get('odpowiedz') == current_question['odpok']:
            session['points'] += 1

        session['question_index'] += 1

        if session['question_index'] >= len(DANE):
            flash('Liczba poprawnych odpowiedzi, to: {0}'.format(session['points']))
            session.pop('question_index')
            session.pop('points')
            return redirect(url_for('wynik'))

    if 'question_index' in session:
        current_question = DANE[session['question_index']]
        return render_template('test.html', pytanie=current_question)

    return redirect(url_for('/wynik'))

@app.route('/wynik')
def wynik():
    return render_template('wynik.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)