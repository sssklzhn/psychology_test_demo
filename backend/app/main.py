# main.py - В НАЧАЛЕ файла:
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import asyncio
import csv
import io
from fastapi.responses import Response 

# Импортируем наши модули
from app.services.pdf_generator import generate_user_pdf, generate_summary_pdf
from app.services.csv_generator import generate_summary_csv  # создайте этот файл
from app.database import db
from app.crud import (
    create_test_users, get_all_users, get_user_by_login,
    save_answers, save_results,
    load_questions_from_firestore, get_question_count
)
from app.services.scoring import calculate_scores, interpret_scores

# Pydantic модели
class UserCreate(BaseModel):
    login: str
    password: str

class Answer(BaseModel):
    question_id: str
    answer: bool

class TestSubmission(BaseModel):
    answers: List[Answer]

# Создаем приложение
app = FastAPI(
    title="Psychology Testing API",
    version="1.0.0",
    description="API для психологического тестирования охранников"
)

# Настройка CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# Настройка CORS - ОБНОВИТЕ В НАЧАЛЕ main.py:
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",           # локальная разработка
        "http://127.0.0.1:3000",           # локальная разработка
        "https://psychology-test-demo-usfg.vercel.app",  # ваш фронтенд на Vercel
        "https://psychology-test-demo.vercel.app",       # если есть другой домен
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Универсальная проверка токена"""
    print(f"🔐 ВЫЗВАНА verify_token")
    
    if not credentials:
        print("❌ Нет credentials в запросе")
        raise HTTPException(status_code=401, detail="Токен не предоставлен")
    
    token = credentials.credentials
    
    print(f"🔐 Токен получен: {token}")
    
    if not token:
        print("❌ Пустой токен")
        raise HTTPException(status_code=401, detail="Токен не предоставлен")
    
    try:
        # УНИВЕРСАЛЬНЫЙ ПАРСИНГ
        if token.startswith("user_token_"):
            # Убираем префикс
            token_without_prefix = token[11:]  # "user_token_"
            
            # Разбиваем
            parts = token_without_prefix.split("_")
            print(f"📊 Части без префикса: {parts}")
            
            # 🔥 ИСПРАВЛЕННЫЙ АЛГОРИТМ:
            # Определяем где timestamp
            # Timestamp: последняя часть, содержит точку или очень большое число
            
            if len(parts) >= 2:
                # Пробуем найти timestamp (последняя часть с точкой или большое число)
                timestamp_index = -1
                last_part = parts[-1]
                
                # Проверяем последнюю часть
                try:
                    # Пробуем преобразовать в float
                    timestamp_val = float(last_part)
                    # Если это число и (содержит точку ИЛИ больше 1000000000 - примерное время с 2001 года)
                    if "." in last_part or timestamp_val > 1000000000:
                        timestamp_index = len(parts) - 1
                except ValueError:
                    pass
                
                if timestamp_index >= 0:
                    # Есть timestamp
                    user_id_parts = parts[:timestamp_index]
                    timestamp = parts[timestamp_index]
                    
                    user_id = "_".join(user_id_parts) if user_id_parts else parts[0]
                    
                    print(f"🎯 Извлечен user_id: {user_id}")
                    print(f"⏰ Timestamp: {timestamp}")
                    
                    # Проверяем в базе
                    user_ref = db.collection('users').document(user_id)
                    user_doc = user_ref.get()
                    
                    if user_doc.exists:
                        user_data = user_doc.to_dict()
                        print(f"✅ ПОЛЬЗОВАТЕЛЬ НАЙДЕН: {user_data.get('login')}")
                        return {"token": token, "user_id": user_id, "user_data": user_data}
                else:
                    # Нет timestamp, или timestamp - последний элемент без точки
                    # Для админа: ['admin', '001', '1769966427.944128']
                    # Последний: '1769966427.944128' - содержит точку, это timestamp
                    # Для обычных: ['DimAyb6gpboTaLO1JHAX', '1769965951.244964']
                    # Последний: '1769965951.244964' - содержит точку, это timestamp
                    
                    # Проверяем последнюю часть еще раз внимательнее
                    last_part = parts[-1]
                    if "." in last_part and len(last_part) > 10:
                        # Содержит точку и длинная - это timestamp
                        user_id = "_".join(parts[:-1]) if len(parts) > 1 else parts[0]
                        print(f"🎯 Извлечен user_id (timestamp в конце): {user_id}")
                        
                        user_ref = db.collection('users').document(user_id)
                        user_doc = user_ref.get()
                        
                        if user_doc.exists:
                            user_data = user_doc.to_dict()
                            print(f"✅ ПОЛЬЗОВАТЕЛЬ НАЙДЕН: {user_data.get('login')}")
                            return {"token": token, "user_id": user_id, "user_data": user_data}
                    else:
                        # Не нашли timestamp, берем все как user_id
                        user_id = "_".join(parts)
                        print(f"🎯 Извлечен user_id (без timestamp): {user_id}")
                        
                        user_ref = db.collection('users').document(user_id)
                        user_doc = user_ref.get()
                        
                        if user_doc.exists:
                            user_data = user_doc.to_dict()
                            print(f"✅ ПОЛЬЗОВАТЕЛЬ НАЙДЕН: {user_data.get('login')}")
                            return {"token": token, "user_id": user_id, "user_data": user_data}
            
            print(f"❌ Не удалось извлечь user_id из токена")
            raise HTTPException(status_code=401, detail="Неверный токен")
                
        else:
            # Если токен не в формате user_token_
            print("⚠️ Токен не в формате user_token_")
            raise HTTPException(status_code=401, detail="Неверный токен")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Ошибка проверки токена: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=401, detail="Ошибка проверки токена")
# Корневой endpoint
@app.get("/")
async def root():
    return {
        "message": "Psychology Testing API",
        "status": "running",
        "firebase": "connected" if db else "disconnected",
        "version": "1.0.0"
    }
def verify_admin(token_data: dict = Depends(verify_token)):
    """Проверка, что пользователь - администратор"""
    print(f"🛡️ Проверка админа для user_id: {token_data['user_id']}")
    
    user_id = token_data["user_id"]
    
    # Прямая проверка через Firebase (синхронно)
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    
    if not user_doc.exists:
        print(f"❌ Пользователь {user_id} не найден в базе")
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )
    
    user_data = user_doc.to_dict()
    print(f"📋 Данные пользователя: {user_data.get('login')}, роль: {user_data.get('role')}")
    
    # Проверяем роль
    if user_data.get('role') != 'admin':
        print(f"❌ У пользователя {user_data.get('login')} нет прав администратора")
        raise HTTPException(
            status_code=403,
            detail="Доступ запрещен. Требуются права администратора"
        )
    
    print(f"✅ Администратор авторизован: {user_data.get('login')}")
    return token_data


@app.post("/api/admin/generate-and-download-users")
async def generate_and_download_users(
    count: int = 10,
    admin_data: dict = Depends(verify_admin)  # Добавить проверку
):
    """Генерация и скачивание CSV с пользователями"""
    if count > 100:
        raise HTTPException(status_code=400, detail="Максимум 100 пользователей за раз")
    
    users = await create_test_users(count)
    
    # Создаем CSV с правильной кодировкой
    output = io.StringIO()
    output.write('\ufeff')  # BOM для Excel
    
    writer = csv.writer(output, delimiter=';')
    writer.writerow(['№', 'Логин', 'Пароль', 'Email', 'Статус'])
    
    for i, user in enumerate(users, 1):
        writer.writerow([
            i,
            user['login'],
            user['password'],
            user['email'],
            'Ожидает'
        ])
    
    csv_content = output.getvalue()
    
    return Response(
        content=csv_content.encode('utf-8'),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f"attachment; filename=users_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        }
    )

@app.post("/api/admin/generate-users")
async def generate_users(
    count: int = 10, 
    admin_data: dict = Depends(verify_admin)  # Добавить проверку
):
    """Генерация тестовых пользователей с правильным CSV"""
    if count > 100:
        raise HTTPException(status_code=400, detail="Максимум 100 пользователей за раз")
    
    users = await create_test_users(count)
    
    # Создаем CSV с правильной кодировкой
    output = io.StringIO()
    
    # Добавляем BOM для UTF-8 (Excel)
    output.write('\ufeff')
    
    writer = csv.writer(output, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Заголовок
    writer.writerow(['Логин', 'Пароль', 'Email', 'Статус'])
    
    # Данные
    for user in users:
        writer.writerow([
            user['login'],
            user['password'],
            user['email'],
            'Ожидает тестирования'
        ])
    
    csv_content = output.getvalue()
    
    return {
        "success": True,
        "message": f"Создано {len(users)} пользователей",
        "users": users,
        "count": len(users),
        "csv_content": csv_content
    }

@app.get("/api/admin/users")
async def get_users(admin_data: dict = Depends(verify_admin)):  # Добавить проверку
    """Получение всех пользователей"""
    users = await get_all_users()
    return {
        "success": True,
        "count": len(users),
        "users": users
    }

# Аутентификация

@app.post("/api/auth/login")
async def login(login_data: UserCreate):
    """Вход пользователя"""
    user = await get_user_by_login(login_data.login)
    
    if not user or user.get("password") != login_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )
    
    # ВЕРНУТЬ старый формат: user_token_{user_id}_{timestamp}
    timestamp = datetime.now().timestamp()
    token = f"user_token_{user['id']}_{timestamp}"
    
    print(f"🔑 Сгенерирован токен: {token}")
    print(f"📋 Данные пользователя: id={user['id']}, login={user['login']}")
    
    return {
        "success": True,
        "message": "Вход выполнен успешно",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "login": user["login"],
            "isCompleted": user.get("isCompleted", False),
            "role": user.get("role", "user")
        }
    }

@app.get("/api/questions")
async def get_questions(token_data: dict = Depends(verify_token)):
    """Получение всех вопросов теста из Firebase"""
    print("=" * 60)
    print("🔍 API /questions ВЫЗВАН")
    print("=" * 60)
    
    # Получаем пользователя
    user_id = token_data["user_id"]
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    
    if user_doc.exists:
        user_data = user_doc.to_dict()
        print(f"👤 Пользователь: {user_data.get('login', 'Неизвестно')}")
        
        # Проверяем, не завершил ли уже тест
        if user_data.get('isCompleted', False):
            raise HTTPException(
                status_code=400,
                detail="Вы уже завершили тестирование"
            )
    print("🔄 Загрузка вопросов из Firebase...")
    print(f"📦 load_questions_from_firestore: {load_questions_from_firestore}")
    print(f"📦 db: {db}")
    try:
        # Прямой доступ к Firebase (для отладки)
        if not db:
            print("❌ Firebase не подключен")
        else:
            print("✅ Firebase подключен")
            docs = db.collection('Questions').limit(5).stream()
            count = 0
            for doc in docs:
                count += 1
                data = doc.to_dict()
                print(f"📝 Документ {count}: ID={doc.id}, data_id={data.get('id')}")
    
    except Exception as e:
        print(f"⚠️  Прямая проверка Firebase: {e}")
    
    # Теперь через нашу функцию
    questions = await load_questions_from_firestore()
    
    print(f"📊 Результат load_questions_from_firestore(): {len(questions)} вопросов")
    
    if not questions:
        print("❌ ВОПРОСЫ НЕ ЗАГРУЖЕНЫ!")
        print("   Проверьте логи выше...")
        return {
            "success": False,
            "message": "Вопросы не найдены в базе данных. Загрузите вопросы из Excel.",
            "questions": [],
            "count": 0
        }
    
    # 🔥 ПРОВЕРКА СТРУКТУРЫ
    print("\n📋 СТРУКТУРА ПЕРВОГО ВОПРОСА:")
    first_q = questions[0]
    print(f"   Тип: {type(first_q)}")
    print(f"   Ключи: {list(first_q.keys())}")
    print(f"   ID: {first_q.get('id')} (тип: {type(first_q.get('id'))})")
    print(f"   Типы: {first_q.get('types', [])}")
    
    # Форматируем для фронтенда
    formatted_questions = []
    for q in questions:
        # 🔥 ВАЖНО: убедимся что id - строка
        question_id = str(q.get('id', ''))
        if not question_id:
            question_id = str(q.get('questionID', ''))
        
        formatted_questions.append({
            "id": question_id,
            "text": q.get('text', ''),
            "types": q.get('types', []),  # Оставляем русские названия
            "pointsIfYes": q.get('pointsIfYes', 0),
            "pointsIfNo": q.get('pointsIfNo', 0),
            "questionNumber": q.get('questionNumber', q.get('questionID', 0))
        })
    
    print(f"\n✅ Отправляю {len(formatted_questions)} вопросов")
    print(f"📋 Пример отправляемого вопроса:")
    print(f"   ID: {formatted_questions[0].get('id')}")
    print(f"   Тип ID: {type(formatted_questions[0].get('id'))}")
    print("=" * 60)
    
    return {
        "success": True,
        "message": f"Найдено {len(questions)} вопросов",
        "count": len(questions),
        "questions": formatted_questions
    }
@app.get("/api/questions/count")
async def get_questions_count():
    """Получение количества вопросов"""
    count = await get_question_count()
    return {
        "success": True,
        "count": count,
        "message": f"В базе {count} вопросов"
    }

# Отправка теста
# @app.post("/api/test/submit")
# async def submit_test(submission: TestSubmission):
#     """Отправка ответов на тест"""
#     print("=" * 60)
#     print("📤 API /test/submit ВЫЗВАН")
#     print("=" * 60)
    
#     try:
#         # Временно используем тестового пользователя
#         user_id = "test_user_001"
        
#         print(f"👤 Пользователь: {user_id}")
#         print(f"📝 Ответов: {len(submission.answers)}")
        
#         # Сохраняем ответы
#         saved = await save_answers(user_id, submission.answers)
#         if not saved:
#             raise HTTPException(status_code=500, detail="Ошибка сохранения ответов")
        
#         # Загружаем вопросы для подсчета
#         questions = await load_questions_from_firestore()
        
#         # Создаем мап вопросов
#         questions_map = {}
#         for q in questions:
#             questions_map[q["id"]] = q
        
#         print(f"📋 Загружено вопросов для подсчета: {len(questions_map)}")
        
#         # Подсчет баллов
#         from app.services.scoring import calculate_scores, interpret_scores
#         scores = calculate_scores(submission.answers, questions_map)
#         interpretations, recommendation = interpret_scores(scores)
        
#         # Сохраняем результаты
#         await save_results(user_id, scores, interpretations, recommendation)
        
#         print(f"✅ Тест успешно обработан!")
#         print(f"📊 Рекомендация: {recommendation}")
        
#         return {
#             "success": True,
#             "message": "Тест успешно завершен!",
#             "results": {
#                 "scores": scores,
#                 "interpretations": interpretations,
#                 "recommendation": recommendation
#             }
#         }
        
#     except Exception as e:
#         print(f"❌ Ошибка обработки теста: {e}")
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=f"Ошибка обработки теста: {str(e)}")

@app.post("/api/test/submit")
async def submit_test(
    submission: TestSubmission,
    token_data: dict = Depends(verify_token)
):
    """Отправка ответов на теста"""
    print("=" * 60)
    print("📤 API /test/submit ВЫЗВАН")
    print("=" * 60)
    
    try:
        # 🔥 ИСПОЛЬЗУЕМ РЕАЛЬНОГО ПОЛЬЗОВАТЕЛЯ ИЗ ТОКЕНА
        user_id = token_data["user_id"]
        
        # Получаем данные пользователя для логирования
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        user_data = user_doc.to_dict()
        print(f"👤 Пользователь: {user_data.get('login', 'Неизвестно')} (ID: {user_id})")
        print(f"📝 Ответов: {len(submission.answers)}")
        
        # Проверяем, не завершил ли уже пользователь тест
        if user_data.get('isCompleted', False):
            completed_at = user_data.get('completedAt', 'неизвестно')
            print(f"⚠️ Пользователь уже завершил тест: {completed_at}")
            
            # Можно либо запретить, либо разрешить перепрохождение
            raise HTTPException(
                status_code=400, 
                detail="Тест уже был завершен ранее"
            )
        
        # Загружаем вопросы для сохранения ответов с баллами
        questions = await load_questions_from_firestore()
        questions_map = {q["id"]: q for q in questions}
        
        # Сохраняем ответы в подколлекцию
        saved = await save_answers(user_id, submission.answers, questions_map)
        if not saved:
            print("⚠️ Не удалось сохранить ответы, но продолжаем...")
        
        # Подсчет баллов
        print("🧮 Подсчет баллов...")
        
        # Преобразуем объекты Answer в словари для scoring
        answers_dicts = []
        for answer in submission.answers:
            answers_dicts.append({
                "question_id": answer.question_id,
                "answer": answer.answer
            })
        
        from app.services.scoring import calculate_scores, interpret_scores
        scores = calculate_scores(answers_dicts, questions_map)
        interpretations, recommendation = interpret_scores(scores)
        
        # Сохраняем результаты
        await save_results(user_id, scores, interpretations, recommendation)
        
        print(f"✅ Тест успешно обработан!")
        print(f"📊 Рекомендация: {recommendation}")
        
        return {
            "success": True,
            "message": "Тест успешно завершен!",
            "results": {
                "scores": scores,
                "interpretations": interpretations,
                "recommendation": recommendation
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Ошибка обработки теста: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка обработки теста: {str(e)}")

# Получение результатов
@app.get("/api/results/{user_id}")
async def get_results(user_id: str):
    """Получение результатов теста пользователя"""
    # Временно возвращаем демо-результаты
    return {
        "success": True,
        "user_id": user_id,
        "results": {
            "scores": {
                "Isk": 5,
                "Con": 3,
                "Ast": 8,
                "Ist": 15,
                "Psi": 7,
                "NPN": 20
            },
            "interpretations": {
                "Isk": "Достоверен (5/9)",
                "Con": "Норма (3/6)",
                "Ast": "Норма (8/15)",
                "Ist": "Норма (15/27)",
                "Psi": "Норма (7/13)",
                "NPN": "Норма (20/23)"
            },
            "recommendation": "рекомендован"
        }
    }
@app.get("/api/admin/check-database")
async def check_database():
    """Проверка состояния базы данных"""
    if not db:
        return {
            "success": False,
            "message": "Firebase не подключен",
            "data": {}
        }
    
    try:
        # Проверяем коллекции
        collections = db.collections()
        collection_names = [col.id for col in collections]
        
        # Считаем документы
        stats = {}
        for collection_name in ['users', 'questions', 'results']:
            try:
                col_ref = db.collection(collection_name)
                count = len(list(col_ref.stream()))
                stats[collection_name] = count
            except:
                stats[collection_name] = 0
        
        return {
            "success": True,
            "message": "База данных подключена",
            "data": {
                "collections": collection_names,
                "counts": stats,
                "firebase": "connected"
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Ошибка проверки базы: {str(e)}",
            "data": {}
        }
# Загрузка вопросов из Excel (будет позже)
@app.post("/api/admin/upload-questions")
async def upload_questions():
    """Загрузка вопросов из Excel в Firebase"""
    return {
        "success": True,
        "message": "Функция загрузки вопросов будет реализована позже",
        "status": "pending"
    }

@app.post("/api/admin/user/{user_id}/reset")
async def reset_user_test(
    user_id: str, 
    admin_data: dict = Depends(verify_admin)
):
    """Сброс теста пользователя (только для админа)"""
    try:
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Удаляем ответы из подколлекции
        answers_collection = user_ref.collection('answers')
        answers_docs = answers_collection.stream()
        deleted_answers = 0
        
        for doc in answers_docs:
            doc.reference.delete()
            deleted_answers += 1
        
        # Удаляем результаты
        results_ref = db.collection('results')
        query = results_ref.where('userId', '==', user_id)
        results_docs = list(query.stream())
        deleted_results = 0
        
        for doc in results_docs:
            doc.reference.delete()
            deleted_results += 1
        
        # Сбрасываем статус пользователя
        user_ref.update({
            "isCompleted": False,
            "completedAt": None,
            "totalAnswers": 0
        })
        
        return {
            "success": True,
            "message": f"Тест пользователя сброшен",
            "deleted": {
                "answers": deleted_answers,
                "results": deleted_results
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сброса теста: {str(e)}")

@app.post("/api/admin/create-admin")
async def create_admin_user(login_data: UserCreate):
    """Создание администратора (первоначальная настройка)"""
    try:
        # Проверяем, существует ли уже пользователь
        existing_user = await get_user_by_login(login_data.login)
        if existing_user:
            raise HTTPException(status_code=400, detail="Пользователь уже существует")
        
        # Создаем администратора
        user_data = {
            "login": login_data.login,
            "password": login_data.password,
            "email": f"{login_data.login}@psychologytest.com",
            "isCompleted": False,
            "createdAt": datetime.now().isoformat(),
            "role": "admin"
        }
        
        doc_ref = db.collection('users').document()
        doc_ref.set(user_data)
        
        return {
            "success": True,
            "message": "Администратор создан",
            "user": {
                "id": doc_ref.id,
                "login": login_data.login,
                "role": "admin"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания администратора: {str(e)}")

@app.get("/api/test/my-results")
async def get_my_results(token_data: dict = Depends(verify_token)):
    """Получение результатов текущего пользователя"""
    user_id = token_data["user_id"]
    
    try:
        # Получаем результаты пользователя
        results_ref = db.collection('results')
        query = results_ref.where('userId', '==', user_id).limit(1)
        results_docs = list(query.stream())
        
        if not results_docs:
            raise HTTPException(status_code=404, detail="Результаты не найдены")
        
        results_data = results_docs[0].to_dict()
        
        # Получаем данные пользователя
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        user_data = user_doc.to_dict() if user_doc.exists else {}
        
        return {
            "success": True,
            "message": "Результаты найдены",
            "user": {
                "id": user_id,
                "login": user_data.get('login', ''),
                "completedAt": user_data.get('completedAt', '')
            },
            "results": results_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения результатов: {str(e)}")

@app.get("/api/admin/user/{user_id}/answers")
async def get_user_answers(
    user_id: str, 
    admin_data: dict = Depends(verify_admin)  # Добавить проверку
):
    """Получение ответов конкретного пользователя (только для админа)"""
    try:
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        user_data = user_doc.to_dict()
        
        # Получаем ответы из подколлекции
        answers_collection = user_ref.collection('answers')
        answers_docs = answers_collection.stream()
        
        answers = []
        for doc in answers_docs:
            answer_data = doc.to_dict()
            answers.append({
                "question_id": doc.id,
                **answer_data
            })
        
        # Получаем результаты
        results_ref = db.collection('results')
        query = results_ref.where('userId', '==', user_id).limit(1)
        results_docs = list(query.stream())
        
        results = None
        if results_docs:
            results = results_docs[0].to_dict()
        
        return {
            "success": True,
            "user": {
                "id": user_id,
                "login": user_data.get('login', ''),
                "isCompleted": user_data.get('isCompleted', False),
                "completedAt": user_data.get('completedAt', '')
            },
            "answers": answers,
            "results": results,
            "count": len(answers)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения ответов: {str(e)}")



@app.get("/api/export/pdf/summary")
async def export_summary_pdf(admin_data: dict = Depends(verify_admin)):
    """Экспорт сводного отчета по всем пользователям в PDF"""
    
    try:
        # Получаем всех пользователей с результатами
        all_results = []
        
        # Получаем всех пользователей
        users_ref = db.collection('users')
        users_docs = users_ref.stream()
        
        for user_doc in users_docs:
            user_data = user_doc.to_dict()
            user_data['id'] = user_doc.id
            
            # Пропускаем незавершивших
            if not user_data.get('isCompleted', False):
                continue
            
            # Получаем результаты пользователя
            results_ref = db.collection('results')
            query = results_ref.where('userId', '==', user_doc.id).limit(1)
            results_docs = list(query.stream())
            
            if results_docs:
                results_data = results_docs[0].to_dict()
                all_results.append({
                    'user': user_data,
                    'scores': results_data.get('scores', {}),
                    'interpretations': results_data.get('interpretations', {}),
                    'recommendation': results_data.get('recommendation', 'ретест')
                })
        
        if not all_results:
            raise HTTPException(status_code=404, detail="Нет данных для отчета")
        
        # 🔥 ВАЖНО: Обрабатываем даты перед генерацией PDF
        for item in all_results:
            if 'completedAt' in item['user'] and item['user']['completedAt']:
                # Конвертируем дату в правильный формат если нужно
                try:
                    # Если дата в формате ISO (например, "2024-01-01T12:00:00")
                    from datetime import datetime as dt
                    iso_date = item['user']['completedAt']
                    if isinstance(iso_date, str):
                        # Пробуем разные форматы дат
                        try:
                            # Формат ISO: "2024-01-01T12:00:00"
                            parsed_date = dt.fromisoformat(iso_date.replace('Z', '+00:00'))
                            item['user']['completedAt'] = parsed_date.strftime('%d.%m.%Y %H:%M')
                        except:
                            try:
                                # Формат Firebase timestamp
                                if '.' in iso_date:
                                    timestamp = float(iso_date)
                                    parsed_date = dt.fromtimestamp(timestamp)
                                    item['user']['completedAt'] = parsed_date.strftime('%d.%m.%Y %H:%M')
                            except:
                                # Оставляем как есть
                                pass
                except Exception as e:
                    print(f"⚠️ Ошибка конвертации даты: {e}")
                    # Продолжаем без изменений
        
        # Генерируем PDF
        pdf_bytes = generate_summary_pdf(all_results)
        
        # Формируем имя файла
        filename = f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Ошибка генерации сводного PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка генерации сводного PDF: {str(e)}")

@app.get("/api/export/csv/summary")
async def export_summary_csv(admin_data: dict = Depends(verify_admin)):
    """Экспорт сводного отчета в CSV"""
    
    try:
        # Получаем всех пользователей с результатами
        all_results = []
        
        users_ref = db.collection('users')
        users_docs = users_ref.stream()
        
        for user_doc in users_docs:
            user_data = user_doc.to_dict()
            
            if not user_data.get('isCompleted', False):
                continue
            
            # Получаем результаты
            results_ref = db.collection('results')
            query = results_ref.where('userId', '==', user_doc.id).limit(1)
            results_docs = list(query.stream())
            
            if results_docs:
                results_data = results_docs[0].to_dict()
                all_results.append({
                    'user': {
                        'login': user_data.get('login', ''),
                        'completedAt': user_data.get('completedAt', ''),
                        'isCompleted': user_data.get('isCompleted', False)
                    },
                    'scores': results_data.get('scores', {}),
                    'interpretations': results_data.get('interpretations', {}),
                    'recommendation': results_data.get('recommendation', 'ретест')
                })
        
        if not all_results:
            raise HTTPException(status_code=404, detail="Нет данных для отчета")
        
        # Используем функцию генератора
        csv_bytes = generate_summary_csv(all_results)
        
        filename = f"results_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        
        return Response(
            content=csv_bytes,
            media_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации CSV: {str(e)}")

@app.get("/api/export/pdf/user/{user_id}")
async def export_user_pdf(
    user_id: str,
    admin_data: dict = Depends(verify_admin)):
    """Экспорт результатов пользователя в PDF"""
    
    try:
        # Получаем данные пользователя
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        user_data = user_doc.to_dict()
        user_data['id'] = user_id
        
        # Получаем результаты
        results_ref = db.collection('results')
        query = results_ref.where('userId', '==', user_id).limit(1)
        results_docs = list(query.stream())
        
        if not results_docs:
            raise HTTPException(status_code=404, detail="Результаты не найдены")
        
        results_data = results_docs[0].to_dict()
        
        # ====== СОЗДАЕМ PDF ПРЯМО ЗДЕСЬ ======
        import io
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # Заголовок (только ASCII)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "PSYCHOLOGY TEST REPORT")
        
        # Информация о пользователе
        c.setFont("Helvetica", 12)
        login = user_data.get('login', 'Unknown')
        # Убираем кириллицу из логина
        login_clean = ''.join(c for c in str(login) if ord(c) < 128)
        if not login_clean:
            login_clean = f"User_{user_id[:8]}"
            
        c.drawString(100, 720, f"User: {login_clean}")
        c.drawString(100, 700, f"User ID: {user_id}")
        
        date_str = user_data.get('completedAt', datetime.now().strftime('%Y-%m-%d'))
        c.drawString(100, 680, f"Date: {date_str}")
        
        # Результаты
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 650, "TEST RESULTS:")
        
        c.setFont("Helvetica", 12)
        y = 630
        scores = results_data.get('scores', {})
        
        # Названия шкал на английском
        scale_names = {
            'Isk': 'Reliability',
            'Con': 'Autoaggression',
            'Ast': 'Vulnerability',
            'Ist': 'Hysteroid',
            'Psi': 'Psychopathic',
            'NPN': 'Neuro-psychic'
        }
        
        for scale_code, scale_name in scale_names.items():
            score = scores.get(scale_code, 0)
            c.drawString(100, y, f"{scale_name}: {score} points")
            y -= 20
        
        # Рекомендация
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, y - 20, "RECOMMENDATION:")
        
        c.setFont("Helvetica", 12)
        recommendation = results_data.get('recommendation', 'no data')
        
        # Преобразуем русские рекомендации в английские
        if recommendation == "рекомендован":
            rec_text = "RECOMMENDED"
        elif recommendation == "условно рекомендован":
            rec_text = "CONDITIONALLY RECOMMENDED"
        elif recommendation == "не рекомендован":
            rec_text = "NOT RECOMMENDED"
        elif recommendation == "ретест":
            rec_text = "RETEST REQUIRED"
        else:
            # Убираем кириллицу
            rec_text = ''.join(c for c in str(recommendation) if ord(c) < 128) or "NO DATA"
        
        c.drawString(100, y - 40, rec_text)
        
        # Подпись
        c.setFont("Helvetica", 10)
        c.drawString(100, 100, "Report generated automatically")
        c.drawString(400, 100, datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        c.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        # ====== КОНЕЦ СОЗДАНИЯ PDF ======
        
        # Формируем имя файла (без кириллицы)
        login_safe = login_clean.replace(' ', '_').replace('/', '_')
        filename = f"report_{login_safe}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Ошибка генерации PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка генерации PDF: {str(e)}")

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    print("🚀 Запуск Psychology Testing API...")
    print("📊 Firebase статус:", "Connected" if db else "Disconnected")
    print("🌐 API доступен по адресу: http://localhost:8000")
    print("📚 Документация: http://localhost:8000/docs")
    print("📊 Health check: http://localhost:8000/")
    print("🔧 Для остановки нажмите Ctrl+C\n")
    
    uvicorn.run(
        "app.main:app",  # Импортируемая строка вместо объекта
        host="0.0.0.0",
        port=8000,
        reload=True
    )