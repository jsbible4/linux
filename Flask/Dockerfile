FROM python:3.10-slim

WORKDIR /app

# 현재 디렉토리의 quiz.py 파일을 컨테이너의 /app으로 복사
COPY quiz.py .

# templates 폴더 전체를 컨테이너의 /app/templates로 복사
# → Flask의 render_template에서 HTML 템플릿들을 찾기 위해 필요
COPY templates/ ./templates/ 

# flask와 pymysql 패키지 설치 (Flask 웹 서버와 MariaDB 연동용)
RUN pip install flask pymysql

# CORS 허용을 위한 패키지 추가 설치
# → 다른 포트 또는 도메인에서 접근할 수 있도록
RUN pip install flask-cors 


# Flask 앱을 실행하는 명령어 (quiz.py 실행)
# 컨테이너가 시작되면 자동으로 이 명령이 실행됨
CMD ["python", "quiz.py"]

