# backend/upload_questions_fixed.py
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from datetime import datetime

# Инициализация Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def upload_questions_fixed():
    """Загрузка вопросов с правильной структурой для фронтенда"""
    
    excel_file = "psychological_test_questions.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ Файл {excel_file} не найден!")
        return
    
    # Загружаем маппинг шкал
    mapping_file = 'scales_mapping_complete.json'
    if not os.path.exists(mapping_file):
        mapping_file = 'scales_mapping.json'
    
    with open(mapping_file, 'r', encoding='utf-8') as f:
        scales_mapping = json.load(f)
    
    scales_mapping = {int(k): v for k, v in scales_mapping.items()}
    
    # Читаем Excel
    print("📖 Чтение Excel файла...")
    df_answers = pd.read_excel(excel_file, sheet_name='Ответы', header=2)
    
    # Правильное переименование колонок
    df_answers = df_answers.rename(columns={
        'Утверждения, относящиеся ко мне (моему характеру)': 'text',
        '№': 'number'
    })
    
    # Очищаем данные
    df_answers = df_answers.dropna(subset=['number'])
    df_answers['number'] = df_answers['number'].astype(int)
    
    print(f"📊 Найдено {len(df_answers)} вопросов в Excel")
    print("🔄 Начинаю загрузку в Firebase...\n")
    
    questions_loaded = 0
    errors = 0
    
    for idx, row in df_answers.iterrows():
        try:
            question_num = int(row['number'])
            question_text = str(row['text']).strip()
            
            if pd.isna(question_text) or question_text in ['nan', 'NaN', '']:
                continue
            
            # Определяем баллы (столбцы 'Да' и 'Нет' могут иметь разные названия)
            points_if_yes = 0
            points_if_no = 0
            
            # Проверяем столбец 'Да'
            if 'Да' in row and pd.notna(row['Да']):
                points_if_yes = 1 if row['Да'] == 1 else 0
            elif 'yes' in row and pd.notna(row['yes']):
                points_if_yes = 1 if row['yes'] == 1 else 0
            
            # Проверяем столбец 'Нет'
            if 'Нет' in row and pd.notna(row['Нет']):
                points_if_no = 1 if row['Нет'] == 1 else 0
            elif 'no' in row and pd.notna(row['no']):
                points_if_no = 1 if row['no'] == 1 else 0
            
            # Получаем шкалы
            types = scales_mapping.get(question_num, ['Общие'])
            
            # 🔥 КЛЮЧЕВОЕ: Правильная структура для фронтенда
            question_data = {
                'id': str(question_num),  # Обязательное поле для React!
                'questionID': question_num,
                'text': question_text,
                'types': types,  # Массив шкал
                'pointsIfYes': points_if_yes,
                'pointsIfNo': points_if_no,
                'questionNumber': question_num,
                'createdAt': datetime.now().isoformat()
            }
            
            # Сохраняем в Firebase с ID = номер вопроса
            doc_ref = db.collection('Questions').document(str(question_num))
            doc_ref.set(question_data)
            
            questions_loaded += 1
            
            # Прогресс
            if question_num <= 5 or question_num % 25 == 0:
                print(f"✅ Вопрос {question_num}: '{question_text[:50]}...'")
                print(f"   Шкалы: {types}, Баллы: Да={points_if_yes}, Нет={points_if_no}")
                
        except Exception as e:
            errors += 1
            print(f"❌ Ошибка вопроса {row.get('number', 'N/A')}: {e}")
            continue
    
    print(f"\n{'='*60}")
    print(f"🎉 ЗАГРУЗКА ЗАВЕРШЕНА!")
    print(f"📦 Успешно загружено: {questions_loaded} вопросов")
    print(f"❌ Ошибок: {errors}")
    print(f"📈 Ожидалось: {len(df_answers)} вопросов")
    print(f"{'='*60}")
    
    # Создаем тестовых пользователей
    create_test_users()
    
    # Проверяем загрузку
    verify_upload()

def create_test_users():
    """Создание тестовых пользователей"""
    
    print("\n👤 Создание тестовых пользователей...")
    
    test_users = [
        {
            'id': 'admin_001',
            'login': 'admin',
            'password': 'admin123',
            'email': 'admin@test.com',
            'isCompleted': False,
            'role': 'admin',
            'createdAt': datetime.now().isoformat()
        },
        {
            'id': 'user_001',
            'login': 'Тестируемый1',
            'password': 'password123',
            'email': 'user1@test.com',
            'isCompleted': False,
            'role': 'user',
            'createdAt': datetime.now().isoformat()
        },
        {
            'id': 'user_002',
            'login': 'Тестируемый2',
            'password': 'password456',
            'email': 'user2@test.com',
            'isCompleted': True,
            'role': 'user',
            'createdAt': datetime.now().isoformat(),
            'completedAt': datetime.now().isoformat()
        }
    ]
    
    created = 0
    for user in test_users:
        try:
            db.collection('users').document(user['id']).set(user)
            created += 1
            print(f"   ✓ {user['login']} ({user['role']})")
        except Exception as e:
            print(f"   ✗ Ошибка создания {user['login']}: {e}")
    
    print(f"✅ Создано {created} пользователей")

def verify_upload():
    """Проверка загруженных данных"""
    
    print("\n🔍 Проверка загрузки...")
    
    try:
        # Получаем все вопросы
        questions_ref = db.collection('Questions')
        docs = list(questions_ref.limit(5).stream())
        
        print(f"📊 В Firebase: {len(list(questions_ref.stream()))} вопросов")
        
        if docs:
            print("\n📋 Пример загруженных вопросов:")
            for i, doc in enumerate(docs, 1):
                data = doc.to_dict()
                print(f"\n{i}. ID документа: {doc.id}")
                print(f"   ID в данных: {data.get('id')}")
                print(f"   Текст: {data.get('text', '')[:60]}...")
                print(f"   Типы: {data.get('types', [])}")
                print(f"   Баллы: Да={data.get('pointsIfYes')}, Нет={data.get('pointsIfNo')}")
                print(f"   Все поля: {list(data.keys())}")
        
        # Проверяем API endpoint
        print("\n🌐 Проверка API...")
        print("   Откройте в браузере: http://localhost:8000/api/questions")
        print("   Должен вернуть JSON с вопросами")
        
    except Exception as e:
        print(f"❌ Ошибка проверки: {e}")

if __name__ == "__main__":
    upload_questions_fixed()