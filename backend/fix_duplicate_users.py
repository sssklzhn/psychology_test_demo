# backend/fix_duplicate_users.py
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def fix_duplicate_users():
    """Удаление дубликатов пользователей"""
    
    print("=== УДАЛЕНИЕ ДУБЛИКАТОВ ПОЛЬЗОВАТЕЛЕЙ ===\n")
    
    try:
        users_ref = db.collection("users")
        
        # Находим всех пользователей
        docs = list(users_ref.stream())
        print(f"Всего пользователей до очистки: {len(docs)}")
        
        # Словарь для отслеживания уникальных логинов
        unique_logins = {}
        deleted_count = 0
        
        for doc in docs:
            data = doc.to_dict()
            login = data.get('login', '')
            
            if login in unique_logins:
                # Удаляем дубликат
                doc.reference.delete()
                deleted_count += 1
                print(f"🗑️ Удален дубликат: {login} (ID: {doc.id})")
            else:
                # Первое вхождение - оставляем
                unique_logins[login] = doc.id
                print(f"✅ Оставлен уникальный: {login} (ID: {doc.id})")
        
        print(f"\nУдалено {deleted_count} дубликатов")
        print(f"Осталось {len(unique_logins)} уникальных пользователей")
        
        # Создаем одного тестового пользователя с известным паролем
        test_login = "Тестируемый1"
        test_password = "test123"
        
        if test_login in unique_logins:
            # Обновляем существующего
            user_ref = users_ref.document(unique_logins[test_login])
            user_ref.update({
                "password": test_password,
                "email": f"{test_login}@psychologytest.com",
                "isCompleted": False
            })
            print(f"\n✅ Обновлен пользователь {test_login}: пароль = {test_password}")
        else:
            # Создаем нового
            user_data = {
                "login": test_login,
                "password": test_password,
                "email": f"{test_login}@psychologytest.com",
                "isCompleted": False,
                "role": "user"
            }
            users_ref.document().set(user_data)
            print(f"\n✅ Создан пользователь {test_login}: пароль = {test_password}")
        
        # Проверяем результат
        print("\n=== ТЕКУЩИЕ ПОЛЬЗОВАТЕЛИ ===")
        final_docs = list(users_ref.stream())
        for doc in final_docs:
            data = doc.to_dict()
            print(f"👤 {data.get('login')}: пароль = {data.get('password')}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    fix_duplicate_users()