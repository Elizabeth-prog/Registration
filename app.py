import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database='service',
                        user='postgres',
                        password='11235813',
                        host='localhost',
                        port='5432')

cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    attention = 'Attention'

    if request.method == 'POST':
        if request.form.get('login'):
            username = request.form.get('username')
            password = request.form.get('password')
            if username == '' or password == '':
                return render_template('login.html', attention=attention)
            else:
                cursor.execute('SELECT * FROM users WHERE login=%s AND password=%s',
                               (str(username), str(password)))
                records = list(cursor.fetchall())
                if len(records) != 0:
                    return render_template('account.html', full_name=records[0][1], login=username, password=password)
                else:
                    return render_template('login.html', attention=attention)

        elif request.form.get('registration'):
            return redirect('/registration/')

    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    attention = 'Attention'
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        print(name)
        if name != '' and login != '' and password != '':
            cursor.execute('INSERT INTO users (full_name, login, password) VALUES (%s, %s, %s);',
                           (str(name), str(login), str(password))
                           )
            conn.commit()

            return redirect('/login/')
        else:
            return render_template('registration.html', attention=attention)
    return render_template('registration.html')


if __name__ == '__main__':
    app.run(debug=True)