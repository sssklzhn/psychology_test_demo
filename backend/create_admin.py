# backend/create_admin.py
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os

# Инициализация Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def create_admin_user():
    """Создание администратора в Firebase"""
    
    admin_data = {
        "login": "admin",
        "password": "admin123",  # Пароль для входа
        "email": "admin@psychologytest.com",
        "role": "admin",
        "isCompleted": True,
        "createdAt": datetime.now().isoformat(),
        "completedAt": datetime.now().isoformat()
    }
    
    try:
        # Проверяем, не существует ли уже админ
        users_ref = db.collection("users")
        query = users_ref.where("login", "==", "admin").limit(1)
        existing_admins = list(query.stream())
        
        if existing_admins:
            print("👑 Администратор уже существует")
            # Обновляем пароль
            for doc in existing_admins:
                doc.reference.update({"password": "admin123"})
                print(f"✅ Пароль администратора обновлен")
            return
        
        # Создаем нового админа
        doc_ref = db.collection("users").document()
        doc_ref.set(admin_data)
        
        print(f"✅ Администратор создан!")
        print(f"   Логин: admin")
        print(f"   Пароль: admin123")
        print(f"   ID: {doc_ref.id}")
        
    except Exception as e:
        print(f"❌ Ошибка создания администратора: {e}")

if __name__ == "__main__":
    create_admin_user()