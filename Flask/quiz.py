from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import random
import sys

app = Flask(__name__)
CORS(app) # 내가 추가한 줄임 ****

def get_db_connection():
    return pymysql.connect(
        host='dbmaria',
        user='user',
        password='password',  # 실제 비밀번호
        db='quizdb',
        charset='utf8'
    )

def get_quiz_data(category):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT question, answer FROM quiz WHERE category=%s"
            cursor.execute(sql, (category,))
            return cursor.fetchall()
    finally:
        conn.close()

@app.route('/quiz', methods=['GET'])
def quiz_api():
    category = request.args.get('category', 'Basic')
    questions = get_quiz_data(category)
    if not questions:
        return "카테고리가 없습니다.", 404

    sampled = random.sample(questions, min(len(questions), 15))
    result = []

    for i, (question, correct) in enumerate(sampled, 1):
        pool = [q[1] for q in questions if q[1] != correct]
        options = random.sample(pool, k=min(3, len(pool))) + [correct]
        random.shuffle(options)
        answer_idx = options.index(correct) + 1

        item = {
            "question_num": f"Q{i}: {question}",
            "choices": {f"선지 {j+1}": opt for j, opt in enumerate(options)},
            "answer": f"{answer_idx}번, {correct}"
        }
        result.append(item)

    return jsonify(result)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

