# backend/check_excel_structure.py
import pandas as pd

def check_excel_structure():
    excel_file = "psychological_test_questions.xlsx"
    
    print("=== ПРОВЕРКА СТРУКТУРЫ EXCEL ФАЙЛА ===")
    
    # Проверяем листы
    xls = pd.ExcelFile(excel_file)
    print(f"Листы в файле: {xls.sheet_names}")
    
    # Лист "Ответы"
    print("\n=== Лист 'Ответы' ===")
    df_answers = pd.read_excel(excel_file, sheet_name='Ответы', header=None)
    print(f"Всего строк: {len(df_answers)}")
    print(f"Всего столбцов: {len(df_answers.columns)}")
    
    # Покажем первые 5 вопросов
    print("\nПервые 5 вопросов:")
    for i in range(3, 8):  # Строки 3-7 (первые 5 вопросов)
        print(f"{df_answers.iloc[i, 2]}. {df_answers.iloc[i, 1][:50]}...")
        print(f"  Да: {df_answers.iloc[i, 3]}, Нет: {df_answers.iloc[i, 4]}")
    
    # Лист "Шкала"
    print("\n=== Лист 'Шкала' ===")
    df_scale = pd.read_excel(excel_file, sheet_name='Шкала', header=None)
    print(f"Всего строк: {len(df_scale)}")
    
    # Проверим шкалы для первых 5 вопросов
    print("\nШкалы для первых 5 вопросов:")
    for i in range(3, 8):
        question_num = df_scale.iloc[i, 2]
        print(f"\nВопрос {question_num}: {df_scale.iloc[i, 1][:50]}...")
        scales = ["Достоверность", "Аутоагрессия", "Ранимость", "Истероидность", "Психопатическая", "НПН"]
        for j, scale in enumerate(scales, start=3):
            cell_value = df_scale.iloc[i, j]
            if pd.notna(cell_value):
                print(f"  {scale}: {cell_value}")

if __name__ == "__main__":
    check_excel_structure()



    # ОДНОРАЗЫВЫЙ ТОЖ НЕ НУЖЕН ФАЙЛ, НО ПУСТЬ БУДЕТ ЗДЕСЬ ДЛЯ СРАВНЕНИЯ