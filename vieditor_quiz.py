from save_wrong_backup import save_wrong_note_backup

import pandas as pd
import random
import subprocess

EXCEL_FILE = '리눅스 기초 디비.xlsx'
SHEET_NAME = 'vieditor'

def load_data():
    return pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

def get_category_choice():
    while True:
        print("\n카테고리를 선택하세요:")
        print("1. vi_input")
        print("2. vi_edit")
        print("3. all")
        choice = input("번호를 입력하세요: ").strip()
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("❌ 1, 2, 3번 중에만 선택하세요.")

def short_answer_quiz(df, used_cmds, wrong_note):
    quiz_df = df[~df['command'].isin(used_cmds)]
    if quiz_df.empty:
        print("✅ 모든 문제를 푸셨습니다!")
        return False, 0
    row = quiz_df.sample().iloc[0]
    print("\n📌 다음을 뜻하는 명령어를 작성하세요:")
    print(f"➡ {row['description']}")
    answer = input("당신의 답변: ").strip()
    used_cmds.add(row['command'])

    if answer == row['command']:
        print("✅ 정답입니다!")
        return True, 1
    else:
        print(f"❌ 오답입니다! 정답은 {row['command']}입니다!")
        wrong_note.append({
            "문제": row['description'],
            "내 답": answer,
            "정답": row['command']
        })
        return True, 0

def multiple_choice_quiz(df, used_cmds, wrong_note):
    quiz_df = df[~df['command'].isin(used_cmds)]
    if quiz_df.empty:
        print("✅ 모든 문제를 푸셨습니다!")
        return False, 0
    row = quiz_df.sample().iloc[0]
    correct_cmd = row['command']
    used_cmds.add(correct_cmd)

    others = df[(df['command'] != correct_cmd) & (~df['command'].isin(used_cmds))]
    if len(others) < 4:
        others = df[df['command'] != correct_cmd]

    options = others['command'].sample(n=min(4, len(others))).tolist() + [correct_cmd]
    random.shuffle(options)

    print("\n📌 다음을 뜻하는 명령어를 아래 보기 중 선택하세요:")
    print(f"➡ {row['description']}")
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")

    try:
        choice = int(input("번호 입력: ").strip())
        if 1 <= choice <= len(options) and options[choice - 1] == correct_cmd:
            print("✅ 정답입니다!")
            return True, 1
        else:
            print(f"❌ 오답입니다! 정답은 {correct_cmd}입니다!")
            wrong_note.append({
                "문제": row['description'],
                "내 답": options[choice - 1] if 1 <= choice <= len(options) else "입력 오류",
                "정답": correct_cmd
            })
            return True, 0
    except:
        print(f"❌ 입력이 잘못되었습니다. 정답은 {correct_cmd}입니다!")
        wrong_note.append({
            "문제": row['description'],
            "내 답": "입력 오류",
            "정답": correct_cmd
        })
        return True, 0

def print_score(score, total):
    print(f"\n📊 현재 점수: {score}/{total}")

def print_wrong_note(wrong_note):
    print("\n📒 오답 노트:")
    if not wrong_note:
        print("👏 오답이 없습니다!")
    for i, item in enumerate(wrong_note, 1):
        print(f"{i}. 문제: {item['문제']}")
        print(f"   내 답: {item['내 답']}")
        print(f"   정답: {item['정답']}\n")

def main():
    df = load_data()
    choice = get_category_choice()

    if choice == '1':
        category_df = df[df['category'] == 'vi_input']
    elif choice == '2':
        category_df = df[df['category'] == 'vi_edit']
    else:
        category_df = df

    score = 0
    total = 0
    used_cmds = set()
    wrong_note = []

    while True:
        print("\n[1] 단답형  [2] 객관식  [3] 종료")
        qtype = input("문제 유형을 선택하세요: ").strip()
        if qtype == '1':
            valid, delta = short_answer_quiz(category_df, used_cmds, wrong_note)
        elif qtype == '2':
            valid, delta = multiple_choice_quiz(category_df, used_cmds, wrong_note)
        elif qtype == '3':
            print_score(score, total)
            print_wrong_note(wrong_note)
            save_wrong_note_backup(wrong_note)  # ✅ 오답 백업 저장
            ## 변경
            # ✅ Git 자동 푸시
            try:
                subprocess.run(["git", "add", "오답_백업.xlsx"], check=True)
                subprocess.run(["git", "commit", "-m", "Update wrong answer backup"], check=True)
                subprocess.run(["git", "push"], check=True)
                print("🚀 오답 파일이 Git에 푸시되었습니다.")
            except subprocess.CalledProcessError:
                print("❌ Git 푸시에 실패했습니다. 수동으로 확인하세요.")
            ## 변경
            
            print("👋 퀴즈를 종료합니다.")
            break
        else:
            print("❌ 1, 2, 3번 중에 선택하세요.")
            continue

        if valid:
            score += delta
            total += 1
            print_score(score, total)

if __name__ == "__main__":
    main()

