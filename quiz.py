import pandas as pd
import random

print("리눅스 퀴즈를 시작합니다!\n")

# 엑셀 파일 읽기
df = pd.read_excel("quiz.xlsx")

# 카테고리 선택
categories = df['category'].unique()
category_dict = {str(i+1): cat for i, cat in enumerate(categories)}
print("카테고리 목록: ")
for num, cat in category_dict.items():
    print(f"{num}. {cat}")
choice = input("\n카테고리 번호 입력: ").strip()
selected = category_dict.get(choice)
if not selected:
    print("잘못된 선택입니다.")
    exit()

print(f"\n선택한 카테고리: {selected}")

# 해당 카테고리의 문제만 추출
cat_df = df[df['category'] == selected].copy()
quiz_questions = cat_df.sample(n=min(15, len(cat_df)))
total_questions = len(quiz_questions)

print(f"총 {total_questions}문제입니다.\n")

score = 0

for i, row in enumerate(quiz_questions.itertuples(), 1):
    correct = row.answer

    # 선지 만들기: 같은 카테고리에서 정답 제외한 랜덤 3개 + 정답
    options_pool = cat_df['answer'].drop_duplicates().tolist()
    options_pool.remove(correct)
    options = random.sample(options_pool, k=min(3, len(options_pool)))
    options.append(correct)
    random.shuffle(options)

    print(f"Q{i}. {row.question}")
    for idx, opt in enumerate(options, 1):
        print(f"{idx}. {opt}")
    try:
        ans = int(input("번호를 선택하세요: "))
        if options[ans - 1] == correct:
            print("\n정답입니다.\n")
            score += 1
        else:
            correct_index = options.index(correct) + 1
            print(f"\n오답입니다. 정답은 {correct_index}. {correct}입니다.\n")
    except:
        correct_index = options.index(correct) + 1
        print(f"입력 오류입니다. 정답은 {correct_index}. {correct}입니다.\n")

print(f"최종 점수: {score}/{total_questions}")
