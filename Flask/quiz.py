# Flask 웹 프레임워크에서 필요한 모듈 불러오기
from flask import Flask, request, render_template

# 다른 도메인/포트에서 접근할 수 있도록 CORS 허용 모듈
from flask_cors import CORS

# MariaDB와 연동하기 위한 pymysql 모듈
import pymysql

# 문제와 보기들을 랜덤하게 섞기 위한 모듈
import random

# Flask 앱 객체 생성
app = Flask(__name__)

# 모든 경로에서 CORS 허용 설정 (다른 포트에서 접속 허용됨)
CORS(app)

# MariaDB 연결 함수
def get_db_connection():
    # pymysql을 이용하여 dbmaria라는 MariaDB 컨테이너에 접속
    return pymysql.connect(
        host='dbmaria',    # Docker 내 서비스명
        user='user',        # DB 사용자명
        password='password',  # DB 비밀번호
        db='quizdb',        # 사용할 데이터베이스 이름
        charset='utf8'        # 문자 인코딩
    )

# 여러 개의 카테고리를 받아 해당하는 문제들을 DB에서 불러오는 함수
def get_multiple_quiz_data(category_list):
    conn = get_db_connection() # DB 연결 객체
    try:
        with conn.cursor() as cursor:  # 커서 객체 생성
            # IN (%s, %s, %s, ...) 형태로 카테고리 개수만큼 SQL 플레이스홀더 생성
            placeholders = ','.join(['%s'] * len(category_list))
            # 해당 카테고리들에 포함된 문제들을 불러오는 쿼리
            sql = f"SELECT question, answer FROM quiz WHERE category IN ({placeholders})"
            cursor.execute(sql, category_list)   # 실제 카테고리 리스트 전달
            return cursor.fetchall()    # 결과 반환 (리스트로 반환)
    finally:
        conn.close()   # 사용 후 연결 닫기

# 가져온 문제를 보기 포함 형식으로 가공하는 함수
def format_questions(raw_questions):
    # 전체 문제 중 최대 15개를 랜덤하게 뽑음
    sampled = random.sample(raw_questions, min(15, len(raw_questions)))    # 최대 15개 샘플링
    formatted = []   # 반환할 형식 리스트
    for i, (q, a) in enumerate(sampled, 1):   # 번호와 함께 문제와 정답 꺼내기
        # 정답을 제외한 나머지 보기 후보들 수집
        pool = [x[1] for x in raw_questions if x[1] != a]
        random.shuffle(pool)   # 보기 섞기
        
        # 보기 중 정답 포함하여 최대 4개 선택
        options = random.sample(pool, k=min(3, len(pool))) + [a]
        random.shuffle(options) # 정답도 포함한 상태로 섞기
        
        # 하나의 문제 데이터 구성
        formatted.append({
            'index': i,        # 문제 번호
            'question': q,     # 문제 텍스트
            'choices': options,  # 보기 목록 (리스트)
            'answer': a          # 정답 텍스트

        })
    return formatted            # 포맷 완료된 퀴즈 리스트 반환


# ------------------------------------
# 아래는 각각의 카테고리(라우트) 정의
# 사용자가 URL로 접근 시 HTML 템플릿을 보여줌
# ------------------------------------


@app.route('/Basic')
def Basic_quiz():
    categories = ['Basic']   # 카테고리 리스트
    data = get_multiple_quiz_data(categories)  # DB에서 문제 조회
    questions = format_questions(data)      # 보기 포함 포맷 적용
    return render_template('Basic.html', questions=questions)   
    # Flask/templates/Basic.html 템플릿에 전달

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


# ------------------------------------
# 앱을 0.0.0.0 IP(모든인터페이스)와 포트 5000에서 실행 (도커 외부에서도 접근 가능하게)
# 컨테이너 내부에서 Flask는 5000번 포트에서 동작
# ------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




