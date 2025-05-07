import random

quiz_data = [
    {
        "type": "객관식",
        "question": "디렉토리 변경 명령어는 무엇인가?",
        "choices": ["a) ls", "b) cd", "c) rm", "d) touch"],
        "answer": "b",
        "reference": "https://man7.org/linux/man-pages/man1/cd.1p.html"
    },
    {
        "type": "빈칸 채우기",
        "question": "빈 파일을 생성하려면 ______ 명령어를 사용한다.",
        "answer": "touch"
    },
    {
        "type": "단답형",
        "question": "ls 명령어는 무엇을 출력하는가?",
        "answer": "디렉토리 내용 목록 출력"
    }
]

def run_quiz():
    score = 0
    for q in quiz_data:
        print(f"\n[{q['type']}] {q['question']}")
        if q["type"] == "객관식":
            for choice in q["choices"]:
                print(choice)
            user_input = input("👉 정답 입력 (예: a, b): ").strip().lower()
            if user_input == q["answer"]:
                print("✅ 정답!")
                score += 1
            else:
                print(f"❌ 오답. 정답은 {q['answer']} / 참고: {q['reference']}")
        else:
            user_input = input("👉 입력: ").strip()
            if user_input == q["answer"]:
                print("✅ 정답!")
                score += 1
            else:
                print(f"❌ 오답. 정답은 {q['answer']}")
    print(f"\n🎉 최종 점수: {score}/{len(quiz_data)}")

if __name__ == "__main__":
    run_quiz()



