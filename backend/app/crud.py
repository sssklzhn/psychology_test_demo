from datetime import datetime
import random
import string
from app.database import db, USERS_COLLECTION, QUESTIONS_COLLECTION, RESULTS_COLLECTION


QUESTIONS_COLLECTION = 'Questions' 
USERS_COLLECTION = 'users'
RESULTS_COLLECTION = 'results'

def generate_password(length=8):
    """Генерация случайного пароля"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# ===== РАБОТА С ВОПРОСАМИ =====

# app/crud.py
# app/crud.py - ОБНОВЛЕННАЯ ФУНКЦИЯ:

async def load_questions_from_firestore():
    """Загрузка вопросов из Firebase"""
    print("🔥 ЗАПУСК load_questions_from_firestore()")
    
    if not db:
        print("❌ Firebase не подключен")
        return []
    
    try:
        print(f"🔍 Обращаюсь к коллекции: 'Questions'")
        
        # 🔥 ПРЯМОЙ ЗАПРОС БЕЗ .limit()
        docs = db.collection('Questions').get()
        
        print(f"📊 Найдено документов: {len(docs)}")
        
        questions = []
        for i, doc in enumerate(docs):
            data = doc.to_dict()
            
            # 🔥 ВАЖНО: добавляем ID если его нет
            if 'id' not in data:
                data['id'] = doc.id
            
            questions.append(data)
            
            # Покажем первые 3 для отладки
            if i < 3:
                print(f"📝 Документ {i+1}:")
                print(f"   ID документа: {doc.id}")
                print(f"   ID в данных: {data.get('id')}")
                print(f"   questionID: {data.get('questionID')}")
                print(f"   Типы: {data.get('types', [])}")
                print(f"   Текст: {data.get('text', '')[:50]}...")
        
        print(f"✅ УСПЕХ: Загружено {len(questions)} вопросов")
        
        # Сортируем
        if questions:
            questions.sort(key=lambda x: x.get('questionNumber', x.get('questionID', 0)))
            print(f"📋 После сортировки первый вопрос: ID={questions[0].get('id')}")
        
        return questions
        
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА в load_questions_from_firestore: {e}")
        import traceback
        traceback.print_exc()
        return []
async def get_question_count():
    """Получение количества вопросов"""
    if not db:
        return 0
    
    try:
        questions_ref = db.collection(QUESTIONS_COLLECTION)
        count = len(list(questions_ref.stream()))
        return count
    except:
        return 0

# ===== РАБОТА С ПОЛЬЗОВАТЕЛЯМИ =====

async def create_test_users(count=10):
    """Создание тестовых пользователей с проверкой существующих"""
    if not db:
        return {"error": "Firebase не подключен"}
    
    try:
        # 🔥 Сначала получаем существующих пользователей
        existing_users_ref = db.collection(USERS_COLLECTION)
        existing_users = existing_users_ref.stream()
        
        # Собираем существующие логины
        existing_logins = set()
        existing_numbers = set()
        
        for user_doc in existing_users:
            user_data = user_doc.to_dict()
            login = user_data.get("login", "")
            if login.startswith("Тестируемый"):
                try:
                    # Извлекаем номер из логина
                    num = int(login.replace("Тестируемый", ""))
                    existing_numbers.add(num)
                except:
                    pass
                existing_logins.add(login)
        
        print(f"📊 Найдено существующих пользователей: {len(existing_logins)}")
        print(f"📝 Существующие номера: {sorted(existing_numbers)}")
        
        users = []
        created_count = 0
        
        # Находим максимальный номер
        next_number = 1
        if existing_numbers:
            next_number = max(existing_numbers) + 1
        
        for i in range(count):
            login = f"Тестируемый{next_number}"
            password = generate_password()
            
            # Проверяем, не существует ли уже такой логин
            if login in existing_logins:
                print(f"⚠️ Пользователь {login} уже существует, пропускаем")
                next_number += 1
                continue
            
            user_data = {
                "login": login,
                "password": password,
                "email": f"{login}@psychologytest.com",
                "isCompleted": False,
                "createdAt": datetime.now().isoformat(),
                "role": "user"
            }
            
            try:
                # Создаем документ с произвольным ID
                doc_ref = db.collection(USERS_COLLECTION).document()
                doc_ref.set(user_data)
                
                users.append({
                    "id": doc_ref.id,
                    "login": login,
                    "password": password,
                    "email": user_data["email"]
                })
                
                print(f"✅ Создан: {login} / {password}")
                created_count += 1
                
                # Добавляем в множества чтобы избежать дубликатов в этой же сессии
                existing_logins.add(login)
                existing_numbers.add(next_number)
                
            except Exception as e:
                print(f"Ошибка создания пользователя {login}: {e}")
            
            next_number += 1
        
        print(f"🎉 Итого создано: {created_count} пользователей")
        
        return users
        
    except Exception as e:
        print(f"❌ Ошибка в create_test_users: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

async def get_all_users():
    """Получение всех пользователей"""
    if not db:
        return []
    
    try:
        users_ref = db.collection(USERS_COLLECTION)
        docs = users_ref.stream()
        
        users = []
        for doc in docs:
            user_data = doc.to_dict()
            users.append({
                "id": doc.id,
                **user_data
            })
        
        return users
        
    except Exception as e:
        print(f"Ошибка получения пользователей: {e}")
        return []

async def get_user_by_login(login):
    """Поиск пользователя по логину"""
    if not db:
        return None
    
    try:
        users_ref = db.collection(USERS_COLLECTION)
        query = users_ref.where("login", "==", login).limit(1)
        docs = query.stream()
        
        for doc in docs:
            return {
                "id": doc.id,
                **doc.to_dict()
            }
        
        return None
        
    except Exception as e:
        print(f"Ошибка поиска пользователя: {e}")
        return None

# async def save_answers(user_id, answers):
#     """Сохранение ответов пользователя"""
#     print(f"💾 Сохранение ответов для пользователя {user_id}")
    
#     if not db:
#         print("❌ Firebase не подключен")
#         return False
    
#     try:
#         user_ref = db.collection('users').document(user_id)
        
#         # Проверяем существует ли пользователь
#         user_doc = user_ref.get()
#         if not user_doc.exists:
#             print(f"❌ Пользователь {user_id} не найден")
#             # Создаем временного пользователя
#             user_ref.set({
#                 "login": f"user_{user_id}",
#                 "createdAt": datetime.now().isoformat(),
#                 "role": "user",
#                 "isCompleted": False
#             })
        
#         # Сохраняем ответы
#         answers_dict = {}
#         for i, answer in enumerate(answers):
#             # 🔥 ИСПРАВЛЕНИЕ: обращаемся к атрибутам объекта Answer, а не используем .get()
#             question_id = str(answer.question_id)  # напрямую, без .get()
#             answer_value = bool(answer.answer)     # напрямую, без .get()
            
#             answers_dict[question_id] = answer_value
            
#             if i < 3:  # Покажем первые 3 ответа для отладки
#                 print(f"   Ответ {i+1}: вопрос {question_id} = {answer_value}")
        
#         # Обновляем документ пользователя
#         user_ref.update({
#             "answers": answers_dict,
#             "isCompleted": True,
#             "completedAt": datetime.now().isoformat()
#         })
        
#         print(f"✅ Ответы сохранены: {len(answers_dict)} ответов")
#         return True
        
#     except Exception as e:
#         print(f"❌ Ошибка сохранения ответов: {e}")
#         import traceback
#         traceback.print_exc()
#         return False
async def save_answers(user_id, answers, questions_map):
    """Сохранение ответов пользователя с вычислением баллов для каждого ответа"""
    print(f"💾 Сохранение ответов для пользователя {user_id}")
    
    if not db:
        print("❌ Firebase не подключен")
        return False
    
    try:
        user_ref = db.collection('users').document(user_id)
        
        # Проверяем существует ли пользователь
        user_doc = user_ref.get()
        if not user_doc.exists:
            print(f"❌ Пользователь {user_id} не найден")
            raise ValueError(f"Пользователь {user_id} не найден")
        
        user_data = user_doc.to_dict()
        print(f"   Сохраняем для: {user_data.get('login', 'Неизвестно')}")
        
        # Проверяем, не завершил ли уже тест
        if user_data.get('isCompleted', False):
            print(f"⚠️ Пользователь уже завершил тест ранее")
            raise ValueError("Тест уже был завершен")
        
        # Создаем подколлекцию answers
        answers_collection = user_ref.collection('answers')
        
        # Удаляем старые ответы если есть
        old_answers = answers_collection.stream()
        for doc in old_answers:
            doc.reference.delete()
        
        # Сохраняем каждый ответ с вычислением баллов
        total_answers = 0
        for i, answer in enumerate(answers):
            # Получаем данные ответа
            if hasattr(answer, 'question_id'):
                question_id = str(answer.question_id)
                answer_value = bool(answer.answer)
            else:
                question_id = str(answer.get("question_id", ""))
                answer_value = bool(answer.get("answer", False))
            
            # Получаем вопрос для вычисления баллов
            question = questions_map.get(question_id)
            if not question:
                print(f"⚠️ Вопрос {question_id} не найден, пропускаем")
                continue
            
            # Вычисляем баллы за ответ
            if answer_value:  # Ответ "Да"
                points = question.get("pointsIfYes", 0)
            else:  # Ответ "Нет"
                points = question.get("pointsIfNo", 0)
            
            # Сохраняем в подколлекцию
            answer_data = {
                "questionID": question_id,
                "answer": answer_value,
                "points": points,
                "answeredAt": datetime.now().isoformat(),
                "questionText": question.get("text", "")[:100] + "..." if len(question.get("text", "")) > 100 else question.get("text", "")
            }
            
            answers_collection.document(question_id).set(answer_data)
            total_answers += 1
            
            if i < 3:  # Покажем первые 3 ответа для отладки
                print(f"   Ответ {i+1}: вопрос {question_id} = {'Да' if answer_value else 'Нет'}, баллы: {points}")
        
        # Обновляем основной документ пользователя
        user_ref.update({
            "isCompleted": True,
            "completedAt": datetime.now().isoformat(),
            "totalAnswers": total_answers
        })
        
        print(f"✅ Ответы сохранены в подколлекцию: {total_answers} ответов")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка сохранения ответов: {e}")
        import traceback
        traceback.print_exc()
        return False
# ===== РАБОТА С РЕЗУЛЬТАТАМИ =====
async def verify_admin(user_id: str):
    """Проверка, что пользователь является администратором"""
    if not db:
        return False
    
    try:
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return user_data.get('role') == 'admin'
        
        return False
        
    except Exception as e:
        print(f"Ошибка проверки прав администратора: {e}")
        return False
async def save_results(user_id, scores, interpretations, recommendation):
    """Сохранение результатов"""
    if not db:
        return False
    
    try:
        result_data = {
            "userId": user_id,
            "scores": scores,
            "interpretations": interpretations,
            "recommendation": recommendation,
            "createdAt": datetime.now().isoformat()
        }
        
        db.collection(RESULTS_COLLECTION).add(result_data)
        return True
        
    except Exception as e:
        print(f"Ошибка сохранения результатов: {e}")
        return False

async def get_user_results(user_id):
    """Получение результатов пользователя"""
    if not db:
        return None
    
    try:
        results_ref = db.collection(RESULTS_COLLECTION)
        query = results_ref.where("userId", "==", user_id).limit(1)
        docs = query.stream()
        
        for doc in docs:
            return {
                "id": doc.id,
                **doc.to_dict()
            }
        
        return None
        
    except Exception as e:
        print(f"Ошибка получения результатов: {e}")
        return None