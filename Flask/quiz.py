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

def run_console_quiz():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT DISTINCT category FROM quiz")
        categories = [row[0] for row in cursor.fetchall()]
    
    print("리눅스 퀴즈를 시작합니다!\n카테고리 목록:")
    category_dict = {str(i+1): cat for i, cat in enumerate(categories)}
    for num, cat in category_dict.items():
        print(f"{num}. {cat}")
    
    choice = input("\n카테고리 번호 입력: ").strip()
    selected = category_dict.get(choice)
    if not selected:
        print("잘못된 선택입니다.")
        return

    print(f"\n선택한 카테고리: {selected}")
    questions = get_quiz_data(selected)
    total = min(15, len(questions))
    quiz = random.sample(questions, total)

    score = 0
    for i, (question, correct) in enumerate(quiz, 1):
        # 보기 생성
        pool = [q[1] for q in questions if q[1] != correct]
        options = random.sample(pool, k=min(3, len(pool))) + [correct]
        random.shuffle(options)

        print(f"\nQ{i}. {question}")
        for idx, opt in enumerate(options, 1):
            print(f"{idx}. {opt}")

        try:
            ans = int(input("번호를 선택하세요: "))
            if options[ans - 1] == correct:
                print("정답입니다!")
                score += 1
            else:
                print(f"오답입니다. 정답: {correct}")
        except:
            print(f"입력 오류입니다. 정답: {correct}")

    print(f"\n최종 점수: {score}/{total}")

@app.route('/quiz', methods=['GET'])
def quiz_api():
    category = request.args.get('category', 'Basic')
    questions = get_quiz_data(category)
    if not questions:
        return "카테고리가 없습니다.", 404

    sampled = random.sample(questions, min(len(questions), 5))
    return jsonify([{'question': q[0], 'answer': q[1]} for q in sampled])

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'console':
        run_console_quiz()
    else:
        app.run(host='0.0.0.0', port=5000)

