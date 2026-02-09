#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database import db
from app.crud import create_test_users, get_all_users

def test_firebase():
    print("🔧 Тестирование подключения Firebase...")
    
    if not db:
        print("❌ Firebase не подключен!")
        return False
    
    print("✅ Firebase подключен успешно!")
    
    # Тест 1: Создание тестовых пользователей
    print("\n🧪 Тест 1: Создание тестовых пользователей...")
    import asyncio
    
    async def test():
        users = await create_test_users(3)
        print(f"Создано пользователей: {len(users)}")
        for user in users:
            print(f"  - {user['login']}: {user['password']}")
        
        # Тест 2: Получение пользователей
        print("\n🧪 Тест 2: Получение всех пользователей...")
        all_users = await get_all_users()
        print(f"Всего пользователей в БД: {len(all_users)}")
        
        return True
    
    success = asyncio.run(test())
    
    if success:
        print("\n🎉 Все тесты пройдены успешно!")
        return True
    else:
        print("\n❌ Тесты не пройдены")
        return False

if __name__ == "__main__":
    test_firebase()