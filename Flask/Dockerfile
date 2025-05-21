FROM python:3.10-slim

WORKDIR /app

COPY quiz.py .

RUN pip install flask pymysql

RUN pip install flask-cors 
#s내가 추가한 줄 

CMD ["python", "quiz.py"]

