from flask import Flask, render_template, request, url_for, redirect, escape, session
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)


app.config['MYSQL_USER'] = 'c17420_sopu_na4u_ru'
app.config['MYSQL_PASSWORD'] = 'GeTfoVefxobih80'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'c17420_sopu_na4u_ru'

app.config['SECRET_KEY'] = 'Очень длинный рандомный секретный ключ'

mysql = MySQL(app)

@app.route('/', methods=['POST', 'GET'])
def return_login_page():
    return redirect(url_for('login'))

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('visits', None)
    return redirect(url_for('login'))


@app.route('/redirect_to_my_parents', methods=['POST', 'GET'])
def return_my_parents_page():
    return redirect(url_for('my_parents'))

@app.route('/my_parents', methods=['POST', 'GET'])
def my_parents():
    message = ''
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        message = 'Пожалуйста, введите Ваши данные ниже'
        name = str(request.form.get('name'))
        secondname = str(request.form.get('secondname'))
        surname = str(request.form.get('surname'))
        years = str(request.form.get('yearsIn')) + '-' + str(request.form.get('yearsOut'))
        place = str(request.form.get('place'))
        work = str(request.form.get('work'))

        if name == None or name == 'None' or name == '':
            message = 'Данные пусты'
        else:
            cur.execute('''INSERT INTO parents VALUES (%s, %s, %s, %s, %s, %s)''',(name, secondname, surname, years, place, work))
            mysql.connection.commit()
            message = name + ' ' + secondname + ' ' + 'добавлен'
            return render_template('my_parents.html', message=message)

    return render_template('my_parents.html', message=message)



@app.route('/login', methods=['POST', 'GET'])
def login():
    message = ''
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        username = str(request.form.get('username'))
        password = str(request.form.get('password'))
        cur.execute('''SELECT * FROM users''')
        rows_of_userdata = cur.fetchall()
        mysql.connection.commit()

        for row in rows_of_userdata:
            if (username == row[0]) and (password == row[1]):
                return render_template('index.html', message = message + username)

        else:
            message = 'Введены некорректные данные, попробуйте ещё раз'
            return render_template('login.html', message = message)

    return render_template('login.html', message = message)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    message = ''
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        username = str(request.form.get('username'))
        password = str(request.form.get('password'))
        repeat_password = str(request.form.get('repeat_password'))
        # создаем пустой словарь и наполняем данными из БД
        cur.execute('''SELECT * FROM users''')
        all_of_usernames = cur.fetchall()
        mysql.connection.commit()
        i = 0

        for item in all_of_usernames:
            if (username == item[0]):
                i+=1

        if i> 0:
            message = 'Пользователь {} уже существует'.format(username)
            return render_template('registration.html', message=message)
        elif len(password)<4:
            message = 'Пароль должен быть длиннее 4 символов'
            return render_template('registration.html', message=message)
        elif password != repeat_password:
            message = 'Пароли не совпадают'
            return render_template('registration.html', message=message)

        else:
            username = str(request.form.get('username'))
            password = str(request.form.get('password'))
            cur.execute('''INSERT INTO users VALUES (%s,  %s)''', (username, password))
            mysql.connection.commit()
            message = 'Теперь Вы можете войти, '
            return redirect(url_for('login'))

    return render_template('registration.html')

@app.route('/index', methods=['post','get'])
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return render_template('index.html')


@app.route('/parents_mapping', methods = ['post', 'get'])
def parents_mapping():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM parents''')
    parents = cur.fetchall()
    mysql.connection.commit()

    return render_template('parents_mapping.html', parents = parents)


@app.route('/my_contacts', methods=['POST','GET'])
def my_contacts():
    message = ''
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM contacts''')
    contacts_added = cur.fetchall()
    mysql.connection.commit()

    if request.method == 'POST':
        contact_name = str(request.form.get('contact_name'))
        number = str(request.form.get('number'))
        if contact_name == None or contact_name == 'None' or contact_name == '':
            message = 'Данные пусты'

        else:
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO contacts VALUES (%s, %s)''',(contact_name, number))
            mysql.connection.commit()
            message = contact_name + ' ' + 'добавлен'
            return redirect(url_for('my_contacts'))

    return render_template('my_contacts.html', contacts_added = contacts_added)


@app.route('/feedback', methods = ['post', 'get'])
def feedback():
    message = ''
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM feedback''')
    feedback = cur.fetchall()
    mysql.connection.commit()

    if request.method == 'POST':
        text = str(request.form.get('text'))
        date = str(datetime.now())
        if text == None or text == 'None' or text == '':
            message = 'Данные пусты'
        else:
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO feedback VALUES (%s, %s)''',(text, date))
            mysql.connection.commit()
            message = 'Ваш комментарий добавлен'
            return redirect(url_for('feedback'))

    return render_template('feedback.html', feedback = feedback)



if __name__ == '__main__':
    app.run(debug=True)

