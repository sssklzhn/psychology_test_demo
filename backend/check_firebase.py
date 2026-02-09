# backend/check_firebase.py
import firebase_admin
from firebase_admin import credentials, firestore
import sys

# Инициализация Firebase
try:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase подключен")
except Exception as e:
    print(f"❌ Ошибка подключения Firebase: {e}")
    sys.exit(1)

def check_collections():
    """Проверка всех коллекций"""
    
    print("\n🔍 Проверка коллекций...")
    
    collections = ['Questions', 'users', 'Scales', 'results']
    
    for collection in collections:
        try:
            docs = list(db.collection(collection).stream())
            print(f"📊 {collection}: {len(docs)} документов")
            
            if collection == 'Questions' and docs:
                print("\n📋 ПЕРВЫЕ 3 ВОПРОСА:")
                for i, doc in enumerate(docs[:3], 1):
                    data = doc.to_dict()
                    print(f"\n{i}. ID документа: {doc.id}")
                    print(f"   ID в данных: {data.get('id', 'НЕТ!')}")
                    print(f"   questionID: {data.get('questionID')}")
                    print(f"   Текст: {data.get('text', '')[:60]}...")
                    print(f"   Все поля: {list(data.keys())}")
                    
        except Exception as e:
            print(f"❌ Ошибка коллекции {collection}: {e}")

def check_single_question():
    """Проверка конкретного вопроса"""
    
    print("\n🔍 Проверка вопроса №1...")
    
    try:
        doc_ref = db.collection('Questions').document('1')
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            print("✅ Вопрос №1 найден!")
            print(f"   Данные: {data}")
            print(f"   Типы: {data.get('types', [])}")
            print(f"   Есть поле 'id'?: {'id' in data}")
        else:
            print("❌ Вопрос №1 не найден!")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    check_collections()
    check_single_question()