# # save_wrong_backup.py
# import pandas as pd
# import os
# from datetime import datetime

# def save_wrong_note_backup(wrong_note, filename="오답_백업.xlsx"):
#     if not wrong_note:
#         print("✅ 저장할 오답이 없습니다.")
#         return

#     df = pd.DataFrame(wrong_note)
#     sheet_name = datetime.now().strftime("%Y-%m-%d")

#     try:
#         if os.path.exists(filename):
#             with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
#                 df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=writer.sheets[sheet_name].max_row if sheet_name in writer.sheets else 0, header=not sheet_name in writer.sheets)
#         else:
#             with pd.ExcelWriter(filename, engine='openpyxl') as writer:
#                 df.to_excel(writer, sheet_name=sheet_name, index=False)

#         print(f"📁 오답이 '{filename}' 파일에 시트 [{sheet_name}]에 저장되었습니다.")
#     except Exception as e:
#         print(f"❌ 저장 실패: {e}")

# save_wrong_backup.py
import pandas as pd
import os

def save_wrong_note_backup(wrong_note, filename="오답_백업.xlsx"):
    if not wrong_note:
        print("✅ 저장할 오답이 없습니다.")
        return

    new_df = pd.DataFrame(wrong_note)
    new_df = new_df[["문제", "내 답", "정답"]]  # 순서 정리

    if os.path.exists(filename):
        try:
            old_df = pd.read_excel(filename)
            if "번호" in old_df.columns:
                old_df = old_df.drop(columns=["번호"])  # ✅ 기존 번호 열 제거
            combined_df = pd.concat([old_df, new_df], ignore_index=True)
        except:
            combined_df = new_df
    else:
        combined_df = new_df

    combined_df.insert(0, "번호", range(1, len(combined_df) + 1))

    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            combined_df.to_excel(writer, index=False)
        print(f"📁 오답이 '{filename}'에 저장되었습니다.")
    except Exception as e:
        print(f"❌ 저장 실패: {e}")
