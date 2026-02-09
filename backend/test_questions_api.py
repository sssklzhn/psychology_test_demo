# backend/test_questions_api.py
import requests
import json

def test_questions_api():
    print("=== ТЕСТ API ВОПРОСОВ ===\n")
    
    # 1. Тест без авторизации (должна быть ошибка)
    print("1. Тест без авторизации:")
    response = requests.get("http://localhost:8000/api/questions")
    print(f"   Статус: {response.status_code}")
    print(f"   Ответ: {response.text[:100]}...")
    
    # 2. Создаем тестового пользователя и получаем токен
    print("\n2. Создание тестового пользователя и получение токена:")
    
    # Сначала создаем пользователя
    create_response = requests.post("http://localhost:8000/api/admin/generate-users?count=1")
    if create_response.status_code == 200:
        user_data = create_response.json()
        test_user = user_data['users'][0]
        print(f"   Создан: {test_user['login']}")
        
        # Входим
        login_response = requests.post(
            "http://localhost:8000/api/auth/login",
            json={"login": test_user['login'], "password": test_user['password']}
        )
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            token = login_data['access_token']
            print(f"   Токен получен: {token[:20]}...")
            
            # 3. Тест с авторизацией
            print("\n3. Тест с авторизацией:")
            headers = {"Authorization": f"Bearer {token}"}
            questions_response = requests.get("http://localhost:8000/api/questions", headers=headers)
            
            print(f"   Статус: {questions_response.status_code}")
            
            if questions_response.status_code == 200:
                questions_data = questions_response.json()
                print(f"   Успех: {questions_data['success']}")
                print(f"   Сообщение: {questions_data['message']}")
                print(f"   Количество: {questions_data['count']}")
                
                if questions_data['questions']:
                    print(f"\n   Первый вопрос:")
                    first_q = questions_data['questions'][0]
                    print(f"     ID: {first_q.get('id')}")
                    print(f"     Текст: {first_q.get('text', '')[:50]}...")
                    print(f"     Типы: {first_q.get('types', [])}")
                    print(f"     Баллы Да: {first_q.get('pointsIfYes')}, Нет: {first_q.get('pointsIfNo')}")
            else:
                print(f"   Ответ: {questions_response.text}")
        else:
            print(f"   Ошибка входа: {login_response.text}")
    else:
        print(f"   Ошибка создания пользователя: {create_response.text}")

if __name__ == "__main__":
    test_questions_api()