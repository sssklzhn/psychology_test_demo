# backend/check_users.py
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def check_users():
    print("=== ПРОВЕРКА ПОЛЬЗОВАТЕЛЕЙ В FIRESTORE ===\n")
    
    try:
        users_ref = db.collection("users")
        docs = list(users_ref.stream())
        
        print(f"Всего пользователей: {len(docs)}")
        
        for doc in docs:
            data = doc.to_dict()
            print(f"\n👤 Пользователь: {data.get('login', 'Без логина')}")
            print(f"   ID: {doc.id}")
            print(f"   Пароль: {data.get('password', 'Нет пароля')}")
            print(f"   Email: {data.get('email', 'Нет email')}")
            print(f"   Статус: {'Завершен' if data.get('isCompleted') else 'В процессе'}")
            
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    check_users()