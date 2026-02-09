# backend/clear_database.py
import firebase_admin
from firebase_admin import credentials, firestore

# Инициализация Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def clear_all_data():
    """Полная очистка базы данных"""
    
    collections = ['Questions', 'users', 'results', 'Scales']
    
    for collection_name in collections:
        try:
            docs = db.collection(collection_name).stream()
            deleted = 0
            
            for doc in docs:
                doc.reference.delete()
                deleted += 1
            
            print(f"✓ Очищена коллекция '{collection_name}': {deleted} документов")
            
        except Exception as e:
            print(f"✗ Ошибка очистки '{collection_name}': {e}")
    
    print("\n✅ База данных полностью очищена!")

if __name__ == "__main__":
    clear_all_data()