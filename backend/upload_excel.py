#!/usr/bin/env python3
"""
ПРОСТОЙ скрипт для загрузки вопросов из Excel в Firebase
"""
import pandas as pd
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Добавляем путь к app
sys.path.append(str(Path(__file__).parent))

# Импортируем после добавления пути
from app.database import db

def load_excel_questions():
    """Загружаем вопросы из Excel"""
    
    excel_file = "Тест 160 для охранника (характер)_с оценкой_доработан.xlsx"
    excel_path = Path(excel_file)
    
    if not excel_path.exists():
        print(f"❌ Файл {excel_file} не найден!")
        print(f"📁 Текущая папка: {Path.cwd()}")
        print("📁 Содержимое папки:")
        for file in Path.cwd().iterdir():
            print(f"  - {file.name}")
        return []
    
    print(f"✅ Найден файл: {excel_path}")
    print(f"📖 Размер: {excel_path.stat().st_size / 1024:.1f} KB")
    
    try:
        # Читаем Excel
        print("📊 Чтение Excel файла...")
        xls = pd.ExcelFile(excel_path)
        print(f"✅ Листы: {xls.sheet_names}")
        
        # Читаем все листы
        sheet_data = {}
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            sheet_data[sheet_name] = df
            print(f"  {sheet_name}: {df.shape[0]} строк, {df.shape[1]} столбцов")
        
        # Определяем какой лист содержит вопросы
        questions_df = None
        if 'Ответы' in sheet_data:
            questions_df = sheet_data['Ответы']
        elif len(sheet_data) > 0:
            # Берем первый лист
            first_sheet = list(sheet_data.keys())[0]
            questions_df = sheet_data[first_sheet]
        
        if questions_df is None:
            print("❌ Не найден лист с вопросами")
            return []
        
        print(f"📝 Парсим вопросы из листа с {questions_df.shape[0]} строками")
        
        questions = []
        
        # Парсим вопросы (предполагаем, что вопросы начинаются с 3 строки)
        for i in range(3, min(170, len(questions_df))):
            # Столбец B (индекс 1) содержит текст вопроса
            if 1 < len(questions_df.iloc[i]):
                cell_value = questions_df.iloc[i, 1]
                
                if pd.isna(cell_value):
                    continue
                
                question_text = str(cell_value).strip()
                
                # Пропускаем пустые строки
                if not question_text:
                    continue
                
                # Извлекаем номер вопроса (первое число перед точкой)
                question_num = i - 2  # Просто порядковый номер
                
                # Очищаем текст
                if '.' in question_text:
                    parts = question_text.split('.', 1)
                    try:
                        # Пробуем извлечь номер из текста
                        num_from_text = parts[0].strip()
                        if num_from_text.isdigit():
                            question_num = int(num_from_text)
                        question_text = parts[1].strip()
                    except:
                        question_text = parts[1].strip()
                
                # Ищем шкалы в листе 'Шкала' если есть
                scales = []
                yes_points = {}
                no_points = {}
                
                if 'Шкала' in sheet_data:
                    scales_df = sheet_data['Шкала']
                    if i < len(scales_df):
                        # Маппинг столбцов на шкалы
                        scale_mapping = {
                            3: 'Isk',  # D
                            4: 'Con',  # E
                            5: 'Ast',  # F
                            6: 'Ist',  # G
                            7: 'Psi',  # H
                            8: 'NPN'   # I
                        }
                        
                        for col_idx, scale in scale_mapping.items():
                            if col_idx < scales_df.shape[1]:
                                cell_val = scales_df.iloc[i, col_idx]
                                if not pd.isna(cell_val):
                                    # Если ячейка не пустая, вопрос относится к этой шкале
                                    scales.append(scale)
                                    yes_points[scale] = 1
                                    no_points[scale] = 0
                else:
                    # Если нет листа 'Шкала', используем простую логику
                    scales = ['Con']  # По умолчанию
                    yes_points = {'Con': 1}
                    no_points = {}
                
                # Создаем вопрос
                question = {
                    "questionId": f"q{question_num:03d}",
                    "number": question_num,
                    "text": question_text,
                    "scales": scales,
                    "yes_points": yes_points,
                    "no_points": no_points,
                    "createdAt": datetime.now().isoformat(),
                    "source": "excel_import"
                }
                
                questions.append(question)
                
                # Логируем прогресс
                if len(questions) % 20 == 0:
                    print(f"  Обработано: {len(questions)} вопросов")
        
        print(f"✅ Всего распарсено: {len(questions)} вопросов")
        
        # Сохраняем в JSON для проверки
        with open('questions_parsed.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        print("💾 Сохранено в questions_parsed.json")
        
        return questions
        
    except Exception as e:
        print(f"❌ Ошибка при чтении Excel: {e}")
        import traceback
        traceback.print_exc()
        return []

def upload_to_firebase(questions):
    """Загружаем вопросы в Firebase"""
    
    if not db:
        print("❌ Firebase не подключен!")
        return False
    
    try:
        questions_ref = db.collection('questions')
        
        print("🗑️  Очистка старых вопросов...")
        # Удаляем старые вопросы
        docs = list(questions_ref.stream())
        deleted_count = 0
        for doc in docs:
            doc.reference.delete()
            deleted_count += 1
        print(f"✅ Удалено: {deleted_count} вопросов")
        
        print("📤 Загрузка новых вопросов в Firebase...")
        uploaded_count = 0
        
        for question in questions:
            try:
                doc_id = question['questionId']
                questions_ref.document(doc_id).set(question)
                uploaded_count += 1
                
                if uploaded_count % 20 == 0:
                    print(f"  Загружено: {uploaded_count}/{len(questions)}")
                    
            except Exception as e:
                print(f"  Ошибка загрузки вопроса {question['number']}: {e}")
        
        print(f"✅ Загружено: {uploaded_count} вопросов")
        
        # Проверяем
        final_count = len(list(questions_ref.stream()))
        print(f"📊 Проверка: в базе {final_count} вопросов")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка Firebase: {e}")
        return False

def main():
    """Основная функция"""
    print("=" * 60)
    print("📊 ЗАГРУЗКА ВОПРОСОВ ИЗ EXCEL В FIREBASE")
    print("=" * 60)
    
    # Загружаем вопросы
    questions = load_excel_questions()
    
    if not questions:
        print("❌ Не удалось загрузить вопросы")
        print("\n📋 Попробуйте:")
        print("1. Убедитесь, что Excel файл в папке backend/")
        print("2. Проверьте имя файла")
        print("3. Запустите скрипт еще раз")
        return
    
    print(f"\n📝 Примеры вопросов:")
    for i in range(min(3, len(questions))):
        q = questions[i]
        print(f"  {i+1}. №{q['number']}: {q['text'][:60]}...")
        print(f"     Шкалы: {q['scales']}")
    
    print(f"\n📊 Всего вопросов: {len(questions)}")
    
    print("\n⚠️  Загрузить в Firebase?")
    confirm = input("Введите 'yes' для подтверждения: ")
    
    if confirm.lower() != 'yes':
        print("❌ Отменено пользователем")
        return
    
    # Загружаем в Firebase
    if upload_to_firebase(questions):
        print("\n" + "=" * 60)
        print("✅ УСПЕШНО ЗАГРУЖЕНО!")
        print("=" * 60)
        
        # Статистика
        scale_stats = {}
        for q in questions:
            for scale in q['scales']:
                scale_stats[scale] = scale_stats.get(scale, 0) + 1
        
        print("\n📊 Статистика по шкалам:")
        all_scales = ['Isk', 'Con', 'Ast', 'Ist', 'Psi', 'NPN']
        for scale in all_scales:
            count = scale_stats.get(scale, 0)
            print(f"  {scale}: {count} вопросов ({count/len(questions)*100:.1f}%)")
        
        print("\n🔗 Проверьте:")
        print("  1. В браузере: http://localhost:8000/api/questions/count")
        print("  2. В Firebase Console: Firestore → коллекция 'questions'")
        
    else:
        print("❌ Ошибка загрузки в Firebase")

if __name__ == "__main__":
    main()




    # НЕ НУЖЕН ЭТОТ ФАЙЛ, НО ПУСТЬ БУДЕТ ЗДЕСЬ ДЛЯ СРАВНЕНИЯ