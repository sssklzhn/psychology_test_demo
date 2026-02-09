import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
from pathlib import Path

def initialize_firebase():
    """Инициализация Firebase"""
    try:
        # Путь к файлу ключа
        cred_path = Path(__file__).parent.parent / 'firebase-key.json'
        
        if not cred_path.exists():
            print(f"❌ Файл ключа не найден: {cred_path}")
            print("Убедитесь, что firebase-key.json находится в папке backend/")
            return None, None
        
        # Инициализация Firebase
        cred = credentials.Certificate(str(cred_path))
        
        # Проверяем, не инициализирован ли уже Firebase
        if not firebase_admin._apps:
            firebase_app = firebase_admin.initialize_app(cred, {
                'projectId': 'psychologytest-54232'
            })
            print("✅ Firebase Admin SDK успешно инициализирован!")
        else:
            print("ℹ️ Firebase уже инициализирован")
        
        # Получаем экземпляры сервисов
        db = firestore.client()
        firebase_auth = auth
        
        return db, firebase_auth
        
    except Exception as e:
        print(f"❌ Ошибка инициализации Firebase: {e}")
        import traceback
        traceback.print_exc()
        return None, None

# Инициализируем Firebase при импорте
db, firebase_auth = initialize_firebase()

# Константы для коллекций
USERS_COLLECTION = "users"
QUESTIONS_COLLECTION = "Questions"
RESULTS_COLLECTION = "results"
ANSWERS_SUBCOLLECTION = "answers"

print(f"Firebase status: {'Connected' if db else 'Not connected'}")