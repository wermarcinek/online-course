from flask import Flask, request, redirect, url_for, flash, render_template

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
    if request.method == 'POST':
        punkty = 0
        odpowiedzi = request.form

        for pnr, odp in odpowiedzi.items():
            if odp == DANE[int(pnr)]['odpok']:
                punkty += 1

        flash('Liczba poprawnych odpowiedzi, to: {0}'.format(punkty))
        return redirect(url_for('test'))
    return render_template('test.html',pytania=DANE)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)