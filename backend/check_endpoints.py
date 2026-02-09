# backend/check_endpoints.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Тестирование доступности эндпоинтов бэкенда"""
    
    endpoints = [
        "/api/auth/login",
        "/api/questions",
        "/api/admin/users",
        "/api/admin/generate-users",
        "/api/test/submit"
    ]
    
    print("=== ТЕСТИРОВАНИЕ ЭНДПОИНТОВ БЭКЕНДА ===\n")
    
    # 1. Тест доступности сервера
    try:
        response = requests.get(BASE_URL + "/")
        print(f"Сервер доступен: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Сервер не запущен! Запустите: uvicorn services.main:app --reload")
        return False
    
    # 2. Тест логина админа
    print("\n1. Тест логина администратора:")
    try:
        response = requests.post(
            BASE_URL + "/api/auth/login",
            json={"login": "admin", "password": "admin123"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Успешно! Токен получен")
            token = data.get("access_token")
            return token
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(f"Ответ: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")
    
    return None

def test_questions_endpoint(token):
    """Тест получения вопросов"""
    print("\n2. Тест получения вопросов:")
    try:
        response = requests.get(
            BASE_URL + "/api/questions",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Успешно! Получено вопросов: {len(data.get('questions', []))}")
            
            # Покажем первый вопрос
            if data.get('questions'):
                first_question = data['questions'][0]
                print(f"\nПример вопроса:")
                print(f"ID: {first_question.get('id')}")
                print(f"Текст: {first_question.get('text', '')[:50]}...")
                print(f"Типы: {first_question.get('types', [])}")
                
                return True
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(f"Ответ: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")
    
    return False

def test_admin_endpoints(token):
    """Тест админских эндпоинтов"""
    print("\n3. Тест админских эндпоинтов:")
    
    # 3.1 Получение пользователей
    try:
        response = requests.get(
            BASE_URL + "/api/admin/users",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Получение пользователей: успешно")
            print(f"   Найдено пользователей: {len(data.get('users', []))}")
        else:
            print(f"❌ Ошибка получения пользователей: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")
    
    # 3.2 Генерация пользователей
    print("\n4. Тест генерации пользователей:")
    try:
        response = requests.post(
            BASE_URL + "/api/admin/generate-users?count=2",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Генерация пользователей: успешно")
            print(f"   Сгенерировано: {data.get('count')} пользователей")
        else:
            print(f"❌ Ошибка генерации пользователей: {response.status_code}")
            print(f"   Ответ: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")

if __name__ == "__main__":
    print("Тестирование интеграции фронтенда и бэкенда")
    print("=" * 50)
    
    # Тестируем эндпоинты
    token = test_endpoints()
    
    if token:
        test_questions_endpoint(token)
        test_admin_endpoints(token)
    
    print("\n" + "=" * 50)
    print("Тестирование завершено!")