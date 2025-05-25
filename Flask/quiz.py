from flask import Flask, request, render_template
from flask_cors import CORS
import pymysql
import random

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return pymysql.connect(
        host='dbmaria',
        user='user',
        password='password',
        db='quizdb',
        charset='utf8'
    )

def get_multiple_quiz_data(category_list):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            placeholders = ','.join(['%s'] * len(category_list))
            sql = f"SELECT question, answer FROM quiz WHERE category IN ({placeholders})"
            cursor.execute(sql, category_list)
            return cursor.fetchall()
    finally:
        conn.close()

def format_questions(raw_questions):
    sampled = random.sample(raw_questions, min(15, len(raw_questions)))
    formatted = []
    for i, (q, a) in enumerate(sampled, 1):
        choices = random.sample(
            [a] + [x[1] for x in raw_questions if x[1] != a][:3],
            k=min(4, len(raw_questions))
        )
        formatted.append({
            'index': i,
            'question': q,
            'choices': choices,
            'answer': a
        })
    return formatted

# 라우트 예시: /Basic
@app.route('/Basic')
def Basic_quiz():
    categories = ['Basic']
    data = get_multiple_quiz_data(categories)
    questions = format_questions(data)
    return render_template('Basic.html', questions=questions)

@app.route('/FilesystemLinkNetwork')
def FilesystemLinkNetwork_quiz():
    categories = ['Filesystem', 'Link', 'Network']
    data = get_multiple_quiz_data(categories)
    questions = format_questions(data)
    return render_template('FilesystemLinkNetwork.html', questions=questions)

@app.route('/Process')
def Process_quiz():
    categories = ['Process']
    data = get_multiple_quiz_data(categories)
    questions = format_questions(data)
    return render_template('Process.html', questions=questions)

@app.route('/Firewall')
def Firewall_quiz():
    categories = ['Firewall']
    data = get_multiple_quiz_data(categories)
    questions = format_questions(data)
    return render_template('Firewall.html', questions=questions)

@app.route('/SchedulingInoutputVieditor')
def SchedulingInoutputVieditor_quiz():
    categories = ['Scheduling', 'Inoutput', 'vi Editor']
    data = get_multiple_quiz_data(categories)
    questions = format_questions(data)
    return render_template('SchedulingInoutputVieditor.html', questions=questions)

@app.route('/apache2MariaDBPHP')
def apache2MariaDBPHP_quiz():
    categories = ['apache2', 'MariaDB', 'php']
    data = get_multiple_quiz_data(categories)
    questions = format_questions(data)
    return render_template('apache2MariaDBPHP.html', questions=questions)

@app.route('/Docker')
def Docker_quiz():
    categories = ['Docker', 'Dockerfile', 'Docker compose']
    data = get_multiple_quiz_data(categories)
    questions = format_questions(data)
    return render_template('Docker.html', questions=questions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




