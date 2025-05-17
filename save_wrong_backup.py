# save_wrong_backup.py
import pandas as pd
import os
from datetime import datetime

def save_wrong_note_backup(wrong_note, filename="오답_백업.xlsx"):
    if not wrong_note:
        print("✅ 저장할 오답이 없습니다.")
        return

    df = pd.DataFrame(wrong_note)
    sheet_name = datetime.now().strftime("%Y-%m-%d")

    try:
        if os.path.exists(filename):
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=writer.sheets[sheet_name].max_row if sheet_name in writer.sheets else 0, header=not sheet_name in writer.sheets)
        else:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"📁 오답이 '{filename}' 파일에 시트 [{sheet_name}]에 저장되었습니다.")
    except Exception as e:
        print(f"❌ 저장 실패: {e}")
