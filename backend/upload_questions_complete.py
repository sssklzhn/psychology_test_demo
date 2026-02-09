# backend/upload_questions_complete.py
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Инициализация Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def clear_all_questions():
    """Очистка всех вопросов перед загрузкой"""
    try:
        questions_ref = db.collection('Questions')
        docs = questions_ref.stream()
        
        deleted = 0
        for doc in docs:
            doc.reference.delete()
            deleted += 1
        
        print(f"Очищено {deleted} вопросов")
    except Exception as e:
        print(f"Ошибка при очистке: {e}")

def upload_questions_complete():
    """Полная загрузка всех вопросов с правильными шкалами"""
    
    excel_file = "psychological_test_questions.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"Файл {excel_file} не найден!")
        return
    
    # Загружаем полный маппинг
    mapping_file = 'scales_mapping_complete.json'
    if not os.path.exists(mapping_file):
        mapping_file = 'scales_mapping.json'
    
    with open(mapping_file, 'r', encoding='utf-8') as f:
        scales_mapping = json.load(f)
    
    # Конвертируем ключи в int
    scales_mapping = {int(k): v for k, v in scales_mapping.items()}
    
    print(f"Загружен маппинг для {len(scales_mapping)} вопросов")
    
    # Проверяем покрытие
    all_questions = set(range(1, 161))
    mapped_questions = set(scales_mapping.keys())
    missing = all_questions - mapped_questions
    
    if missing:
        print(f"⚠️  Внимание: {len(missing)} вопросов без маппинга: {sorted(missing)}")
        # Добавляем дефолтные шкалы для недостающих
        for q in missing:
            scales_mapping[q] = ['Общие']
    
    # Читаем вопросы из Excel
    df_answers = pd.read_excel(excel_file, sheet_name='Ответы', header=2)
    df_answers = df_answers.rename(columns={
        'Утверждения, относящиеся ко мне (моему характеру)': 'text',
        '№': 'number',
        'Да': 'yes',
        'Нет': 'no'
    })
    
    # Очищаем данные
    df_answers = df_answers.dropna(subset=['number'])
    df_answers['number'] = df_answers['number'].astype(int)
    
    print(f"\nНайдено {len(df_answers)} вопросов в Excel")
    
    # Очищаем старые данные
    clear_all_questions()
    
    # Загружаем вопросы
    questions_loaded = 0
    
    for idx, row in df_answers.iterrows():
        try:
            question_num = int(row['number'])
            question_text = str(row['text']).strip()
            
            if pd.isna(question_text) or question_text == 'nan':
                continue
            
            # Определяем баллы
            points_if_yes = 1 if pd.notna(row.get('yes')) and row['yes'] == 1 else 0
            points_if_no = 1 if pd.notna(row.get('no')) and row['no'] == 1 else 0
            
            # Получаем шкалы
            types = scales_mapping.get(question_num, ['Не определено'])
            
            # Подготавливаем данные
            question_data = {
                'questionID': question_num,
                'text': question_text,
                'types': types,
                'pointsIfYes': points_if_yes,
                'pointsIfNo': points_if_no,
                'questionNumber': question_num
            }
            
            # Сохраняем в Firebase
            db.collection('Questions').document(str(question_num)).set(question_data)
            questions_loaded += 1
            
            # Показываем прогресс для первых 10 и каждых 20 вопросов
            if question_num <= 10 or question_num % 20 == 0:
                print(f"✅ {question_num}/160: {question_text[:40]}...")
                print(f"   Баллы: Да={points_if_yes}, Нет={points_if_no} | Шкалы: {types}")
                
        except Exception as e:
            print(f"❌ Ошибка вопроса {row.get('number', 'N/A')}: {e}")
    
    print(f"\n{'='*50}")
    print(f"ЗАГРУЗКА ЗАВЕРШЕНА!")
    print(f"Успешно загружено: {questions_loaded} вопросов")
    print(f"Ожидалось: {len(df_answers)} вопросов")
    print(f"{'='*50}")
    
    # Загружаем информацию о шкалах
    upload_scales_info()
    
    # Тестируем загрузку
    test_loaded_questions()

def upload_scales_info():
    """Загрузка информации о шкалах"""
    
    print("\nЗагрузка информации о шкалах...")
    
    scales_data = [
        {
            'name': 'Достоверность',
            'code': 'Isk',
            'description': 'Шкала социальной желательности. Высокие значения (>9) указывают на недостаточную искренность ответов.',
            'max_score': 17,
            'norm_low': 0,
            'norm_high': 9,
            'interpretation': '0-9: Достоверный результат\n>9: Недостаточная достоверность (рекомендуется ретест через 2 недели)'
        },
        {
            'name': 'Аутоагрессия',
            'code': 'Con',
            'description': 'Склонность к саморазрушающему поведению, самокритике и самоповреждению.',
            'max_score': 14,
            'norm_low': 0,
            'norm_high': 6,
            'interpretation': '0-6: Норма\n7-8: Условно рекомендован\n>8: Нерекомендован'
        },
        {
            'name': 'Ранимость',
            'code': 'Ast',
            'description': 'Повышенная чувствительность, эмоциональная ранимость.',
            'max_score': 19,
            'norm_low': 0,
            'norm_high': 15,
            'interpretation': '0-14: Норма\n15-19: Условно рекомендован\n>19: Повышенная ранимость'
        },
        {
            'name': 'Истероидность',
            'code': 'Ist',
            'description': 'Склонность к демонстративному поведению, потребность во внимании.',
            'max_score': 30,
            'norm_low': 0,
            'norm_high': 27,
            'interpretation': '0-26: Норма\n27-30: Условно рекомендован\n>30: Высокая истероидность'
        },
        {
            'name': 'Психопатическая',
            'code': 'Psi',
            'description': 'Вероятность неадекватных реакций на стрессовые ситуации.',
            'max_score': 30,
            'norm_low': 0,
            'norm_high': 13,
            'interpretation': '0-13: Норма\n>13: Возможна неадекватная реакция на стимул'
        },
        {
            'name': 'НПН',
            'code': 'NPN',
            'description': 'Нервно-психическая неустойчивость. Показатель общей эмоциональной нестабильности.',
            'max_score': 67,
            'norm_low': 0,
            'norm_high': 23,
            'interpretation': '0-22: Рекомендован\n23-30: Условно рекомендован\n>30: Нерекомендован'
        }
    ]
    
    for scale in scales_data:
        try:
            db.collection('Scales').document(scale['name']).set(scale)
            print(f"✅ Шкала: {scale['name']} (норма: {scale['norm_low']}-{scale['norm_high']})")
        except Exception as e:
            print(f"❌ Ошибка шкалы {scale['name']}: {e}")

def test_loaded_questions():
    """Тестирование загруженных вопросов"""
    
    print("\nТестирование загрузки...")
    
    try:
        # Проверяем количество
        questions_ref = db.collection('Questions')
        docs = list(questions_ref.stream())
        
        print(f"Найдено в Firebase: {len(docs)} вопросов")
        
        # Проверяем первые 5
        print("\nПервые 5 вопросов:")
        for i, doc in enumerate(docs[:5]):
            data = doc.to_dict()
            print(f"\n{i+1}. Вопрос {data.get('questionID')}:")
            print(f"   Текст: {data.get('text', '')[:50]}...")
            print(f"   Шкалы: {data.get('types', [])}")
            print(f"   Баллы: Да={data.get('pointsIfYes', 0)}, Нет={data.get('pointsIfNo', 0)}")
        
        # Проверяем случайные вопросы
        import random
        print("\nСлучайные вопросы:")
        for _ in range(3):
            if docs:
                doc = random.choice(docs)
                data = doc.to_dict()
                print(f"\nВопрос {data.get('questionID')}: {data.get('types', [])}")
        
        # Проверяем шкалы
        print("\nПроверка шкал:")
        scales_ref = db.collection('Scales')
        scales_docs = list(scales_ref.stream())
        print(f"Найдено {len(scales_docs)} шкал")
        for doc in scales_docs:
            data = doc.to_dict()
            print(f"  - {data.get('name')}: норма {data.get('norm_low')}-{data.get('norm_high')}")
            
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")

if __name__ == "__main__":
    upload_questions_complete()