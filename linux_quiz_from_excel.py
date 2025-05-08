import pandas as pd
import random

# 엑셀 파일 로드
df = pd.read_excel("linux_commands.xlsx")  # 같은 폴더에 있어야 함

score = 0

def make_multiple_choice(qdata):
    global score
    wrongs = df[df['command'] != qdata['command']]['command'].sample(3).tolist()
    choices = wrongs + [qdata['command']]
    random.shuffle(choices)
    
    print(f"\n[객관식] '{qdata['description']}' 명령어는 무엇인가?")
    for i, choice in enumerate(choices):
        print(f"{chr(97+i)}) {choice}")  # a), b), c) ...

    user = input("👉 정답 입력 (a, b, c, d): ").strip().lower()
    correct_letter = chr(97 + choices.index(qdata['command']))

    if user == correct_letter:
        print("✅ 정답입니다!")
        score += 1
    else:
        print(f"❌ 오답입니다. 정답: {correct_letter}) {qdata['command']}")
        print(f"🔗 참고: {qdata['reference']}")

def make_fill_blank(qdata):
    global score
    print(f"\n[빈칸 채우기] '{qdata['description']}'하려면 ______ 명령어를 사용한다.")
    user = input("👉 입력: ").strip()
    if user == qdata['command']:
        print("✅ 정답입니다!")
        score += 1
    else:
        print(f"❌ 오답입니다. 정답: {qdata['command']}")

def make_short_answer(qdata):
    global score
    print(f"\n[단답형] {qdata['command']} 명령어는 무엇을 하는가?")
    user = input("👉 입력: ").strip()
    if user == qdata['description']:
        print("✅ 정답입니다!")
        score += 1
    else:
        print(f"❌ 오답입니다. 정답: {qdata['description']}")

# 퀴즈 3문제 랜덤 출제
samples = df.sample(3)

for _, row in samples.iterrows():
    qtype = random.choice(['mc', 'fill', 'short'])
    if qtype == 'mc':
        make_multiple_choice(row)
    elif qtype == 'fill':
        make_fill_blank(row)
    else:
        make_short_answer(row)

print(f"\n🎯 총 점수: {score}/{len(samples)}")
