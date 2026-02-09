# backend/test_frontend_backend.py
import requests
import json
import time

class BackendTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.token = None
        self.user = None
        
    def test_login(self):
        """Тест логина"""
        print("1. Тестирование логина...")
        
        # Тест админа
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={"login": "admin", "password": "admin123"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.user = data.get("user")
                print(f"✅ Логин админа успешен")
                print(f"   Токен: {self.token[:20]}...")
                print(f"   Пользователь: {self.user}")
                return True
            else:
                print(f"❌ Ошибка логина админа: {response.status_code}")
                print(f"   Ответ: {response.text}")
                
        except Exception as e:
            print(f"❌ Ошибка соединения: {e}")
        
        return False
    
    def test_get_questions(self):
        """Тест получения вопросов"""
        print("\n2. Тестирование получения вопросов...")
        
        if not self.token:
            print("❌ Нет токена для запроса")
            return False
        
        try:
            response = requests.get(
                f"{self.base_url}/api/questions",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Вопросы получены успешно")
                
                # Проверяем структуру ответа
                if "questions" in data:
                    questions = data["questions"]
                    print(f"   Получено вопросов: {len(questions)}")
                    
                    # Проверяем структуру первого вопроса
                    if questions:
                        first_q = questions[0]
                        required_fields = ["id", "text", "types", "pointsIfYes", "pointsIfNo"]
                        missing_fields = [f for f in required_fields if f not in first_q]
                        
                        if not missing_fields:
                            print(f"✅ Структура вопроса корректна")
                            print(f"   Пример: ID={first_q['id']}, Типы={first_q['types']}")
                        else:
                            print(f"❌ Отсутствуют поля: {missing_fields}")
                            
                    return True
                else:
                    print(f"❌ Нет поля 'questions' в ответе")
                    print(f"   Ответ: {json.dumps(data, indent=2, ensure_ascii=False)}")
            else:
                print(f"❌ Ошибка запроса: {response.status_code}")
                print(f"   Ответ: {response.text}")
                
        except Exception as e:
            print(f"❌ Ошибка соединения: {e}")
        
        return False
    
    def test_admin_functions(self):
        """Тест админских функций"""
        print("\n3. Тестирование админских функций...")
        
        if not self.token or self.user.get("login") != "admin":
            print("❌ Нет прав администратора")
            return False
        
        # 3.1 Получение пользователей
        try:
            response = requests.get(
                f"{self.base_url}/api/admin/users",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Пользователи получены")
                
                if "users" in data:
                    print(f"   Найдено пользователей: {len(data['users'])}")
                else:
                    print(f"   Нет поля 'users' в ответе")
            else:
                print(f"❌ Ошибка получения пользователей: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка соединения: {e}")
        
        # 3.2 Генерация пользователей
        print("\n4. Тестирование генерации пользователей...")
        try:
            response = requests.post(
                f"{self.base_url}/api/admin/generate-users?count=3",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Пользователи сгенерированы")
                
                if "success" in data and data["success"]:
                    print(f"   Сгенерировано: {data.get('count', 0)} пользователей")
                    print(f"   Пример пользователя: {data.get('users', [{}])[0]}")
                else:
                    print(f"   Ответ без success=True: {data}")
            else:
                print(f"❌ Ошибка генерации: {response.status_code}")
                print(f"   Ответ: {response.text}")
                
        except Exception as e:
            print(f"❌ Ошибка соединения: {e}")
    
    def test_complete_flow(self):
        """Тест полного цикла: логин -> тест -> отправка"""
        print("\n" + "="*50)
        print("ТЕСТ ПОЛНОГО ЦИКЛА ФРОНТЕНДА")
        print("="*50)
        
        # 1. Логин тестируемого
        print("\n1. Создание и логин тестируемого...")
        
        # Сначала создаем тестового пользователя
        if self.user and self.user.get("login") == "admin":
            # Генерируем одного пользователя
            try:
                response = requests.post(
                    f"{self.base_url}/api/admin/generate-users?count=1",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success") and data.get("users"):
                        test_user = data["users"][0]
                        print(f"✅ Создан тестовый пользователь: {test_user['login']}")
                        
                        # Логинимся как тестовый пользователь
                        test_login_response = requests.post(
                            f"{self.base_url}/api/auth/login",
                            json={"login": test_user["login"], "password": test_user["password"]}
                        )
                        
                        if test_login_response.status_code == 200:
                            test_data = test_login_response.json()
                            test_token = test_data.get("access_token")
                            print(f"✅ Логин тестируемого успешен")
                            print(f"   Токен: {test_token[:20]}...")
                            
                            # Тест получения вопросов для тестируемого
                            print("\n2. Тест получения вопросов для тестируемого...")
                            questions_response = requests.get(
                                f"{self.base_url}/api/questions",
                                headers={"Authorization": f"Bearer {test_token}"}
                            )
                            
                            if questions_response.status_code == 200:
                                questions_data = questions_response.json()
                                questions = questions_data.get("questions", [])
                                print(f"✅ Тестируемый получил {len(questions)} вопросов")
                                
                                # Тест отправки ответов
                                print("\n3. Тест отправки теста...")
                                
                                # Создаем тестовые ответы (все "Да")
                                test_answers = []
                                for i, q in enumerate(questions[:5]):  # Только первые 5 для теста
                                    test_answers.append({
                                        "question_id": q["id"],
                                        "answer": True  # Все отвечаем "Да"
                                    })
                                
                                submit_response = requests.post(
                                    f"{self.base_url}/api/test/submit",
                                    headers={
                                        "Authorization": f"Bearer {test_token}",
                                        "Content-Type": "application/json"
                                    },
                                    json={"answers": test_answers}
                                )
                                
                                if submit_response.status_code == 200:
                                    submit_data = submit_response.json()
                                    print(f"✅ Тест отправлен успешно!")
                                    print(f"   Результаты: {submit_data.get('results', {})}")
                                else:
                                    print(f"❌ Ошибка отправки теста: {submit_response.status_code}")
                                    print(f"   Ответ: {submit_response.text}")
                                    
                            else:
                                print(f"❌ Ошибка получения вопросов: {questions_response.status_code}")
                                
                        else:
                            print(f"❌ Ошибка логина тестируемого: {test_login_response.status_code}")
                            
                else:
                    print(f"❌ Ошибка генерации пользователя: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Ошибка в процессе теста: {e}")
        
        print("\n" + "="*50)

def run_all_tests():
    """Запуск всех тестов"""
    tester = BackendTester()
    
    print("🚀 ЗАПУСК ТЕСТОВ ИНТЕГРАЦИИ ФРОНТЕНД-БЭКЕНД")
    print("="*50)
    
    # Проверяем что сервер запущен
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"✅ Сервер запущен: {response.status_code}")
    except:
        print("❌ Сервер не запущен! Запустите: uvicorn services.main:app --reload --port 8000")
        return
    
    # Запускаем тесты
    if tester.test_login():
        tester.test_get_questions()
        tester.test_admin_functions()
        tester.test_complete_flow()
    
    print("\n" + "="*50)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")

if __name__ == "__main__":
    run_all_tests()