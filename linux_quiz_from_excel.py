import pandas as pd
import random

# 엑셀 파일 로드
df = pd.read_excel("linux_commands.xlsx")  # 같은 폴더에 있어야 함

def make_multiple_choice(qdata):
    # 보기로 쓸 명령어들 중 하나만 정답
    wrongs = df[df['command'] != qdata['command']]['command'].sample(3).tolist()
    choices = wrongs + [qdata['command']]
    random.shuffle(choices)
    
    print(f"\n[객관식] '{qdata['description']}' 명령어는 무엇인가?")
    for i, choice in enumerate(choices):
        print(f"{chr(97+i)}) {choice}")  # a), b), c), ...
    
    answer_letter = chr(97 + choices.index(qdata['command']))
    print(f"👉 정답: {answer_letter} (참고: {qdata['reference']})")

def make_fill_blank(qdata):
    print(f"\n[빈칸 채우기] '{qdata['description']}'하려면 ______ 명령어를 사용한다.")
    print(f"👉 정답: {qdata['command']}")

def make_short_answer(qdata):
    print(f"\n[단답형] {qdata['command']} 명령어는 무엇을 하는가?")
    print(f"👉 정답: {qdata['description']}")

# 퀴즈 3문제만 랜덤으로 추출
samples = df.sample(3)

for i, row in samples.iterrows():
    qtype = random.choice(['mc', 'fill', 'short'])  # 문제 유형 랜덤
    if qtype == 'mc':
        make_multiple_choice(row)
    elif qtype == 'fill':
        make_fill_blank(row)
    elif qtype == 'short':
        make_short_answer(row)
