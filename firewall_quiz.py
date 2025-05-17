import random

# 문제 데이터: 두 종류 (입력형, 빈칸형)
input_quiz = [
    {
        "type": "input",
        "question": "INPUT 체인에 프로토콜이 tcp이며 목적지 포트가 22번인 패킷을 허용하는 명령어는?",
        "answer": "iptables -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT"
    },
    {
        "type": "input",
        "question": "INPUT 체인에 대한 기본 정책을 드롭(DROP) 하도록 설정하는 명령어는?",
        "answer": "iptables -P INPUT DROP"
    },
    {
        "type": "input",
        "question": "체인에 정의된 모든 규칙을 출력하는 명령어는?",
        "answer": "iptables -L"
    },
    {
        "type": "input",
        "question": "체인에 정의된 모든 규칙을 삭제하는 명령어는?",
        "answer": "iptables -F"
    },
    {
        "type": "input",
        "question": "INPUT 체인의 기본 정책을 ACCEPT로 변경하는 명령어는?",
        "answer": "iptables -P INPUT ACCEPT"
    }
]

fill_quiz = [
    {
        "type": "fill",
        "question": "INPUT 체인에 프로토콜이 tcp이며 목적지 포트가 22번인 패킷을 허용하는 명령어는?\niptables -A INPUT ___ tcp -m tcp _______ 22 -j ACCEPT",
        "answer": ["-p", "--dport"]
    },
    {
        "type": "fill",
        "question": "INPUT 체인의 기본 정책을 DROP으로 설정(변경)하는 명령어는?\niptables __ INPUT ___",
        "answer": ["-P", "DROP"]
    },
    {
        "type": "fill",
        "question": "INPUT 체인의 기본 정책을 ACCEPT로 변경하는 명령어는?\niptables -P ___ ___",
        "answer": ["INPUT", "ACCEPT"]
    }
]

# 전체 퀴즈 통합
quiz_data = input_quiz + fill_quiz

def run_quiz():
    print("🛡️ iptables 방화벽 명령어 퀴즈를 시작합니다!\n")
    random.shuffle(quiz_data)
    score = 0

    for i, item in enumerate(quiz_data, 1):
        print(f"Q{i}. {item['question']}")

        if item['type'] == "input":
            user_input = input("👉 명령어 전체 입력: ").strip()
            if user_input == item["answer"]:
                print("✅ 정답입니다!\n")
                score += 1
            else:
                print(f"❌ 오답입니다. 정답: {item['answer']}\n")

        elif item['type'] == "fill":
            user_answers = []
            for j in range(len(item["answer"])):
                user_input = input(f"빈칸 {j+1}: ").strip()
                user_answers.append(user_input)
            
            if user_answers == item["answer"]:
                print("✅ 정답입니다!\n")
                score += 1
            else:
                correct = ', '.join(item['answer'])
                print(f"❌ 오답입니다. 정답: {correct}\n")

    print(f"🎯 퀴즈 완료! 총 {len(quiz_data)}문제 중 {score}문제 맞았습니다.")

if __name__ == "__main__":
    run_quiz()
