# backend/test_questions_direct.py
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def check_questions_direct():
    """Прямая проверка вопросов в Firebase"""
    
    print("=== ПРЯМАЯ ПРОВЕРКА ВОПРОСОВ ===\n")
    
    try:
        questions_ref = db.collection("Questions")
        docs = list(questions_ref.limit(5).stream())
        
        print(f"Всего вопросов в Firebase: {len(list(questions_ref.stream()))}")
        
        if not docs:
            print("❌ Вопросы не найдены в коллекции 'Questions'")
            # Проверим какие коллекции есть
            collections = db.collections()
            print("\nДоступные коллекции:")
            for col in collections:
                count = len(list(col.stream()))
                print(f"  - {col.id}: {count} документов")
            return
        
        print("\nПервые 5 вопросов:")
        for i, doc in enumerate(docs, 1):
            data = doc.to_dict()
            print(f"\n{i}. ID: {doc.id}")
            print(f"   Текст: {data.get('text', 'Нет текста')[:60]}...")
            print(f"   Поля: {list(data.keys())}")
            print(f"   Типы: {data.get('types', data.get('scales', 'Нет'))}")
            print(f"   Баллы: Да={data.get('pointsIfYes', 0)}, Нет={data.get('pointsIfNo', 0)}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    check_questions_direct()