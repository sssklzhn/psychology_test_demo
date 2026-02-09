"""
Логика подсчета баллов по шкалам
"""

# Нормы по шкалам (из Excel файла)
SCALES_NORMS = {
    "Isk": {
        "name": "Достоверность",
        "norm_min": 0,
        "norm_max": 9,
        "max_points": 15,
        "critical": True  # Если превышено - тест недостоверен
    },
    "Con": {
        "name": "Аутоагрессия", 
        "norm_min": 0,
        "norm_max": 6,
        "max_points": 14,
        "critical": True  # Если превышено - не рекомендован
    },
    "Ast": {
        "name": "Ранимость, чувствительность",
        "norm_min": 0,
        "norm_max": 15,
        "max_points": 19
    },
    "Ist": {
        "name": "Истероидные проявления",
        "norm_min": 0,
        "norm_max": 27,
        "max_points": 30
    },
    "Psi": {
        "name": "Психопатическая реакция",
        "norm_min": 0,
        "norm_max": 13,
        "max_points": 30,
        "critical": True  # Если превышено - не рекомендован
    },
    "NPN": {
        "name": "Нервно-психическая неустойчивость",
        "norm_min": 0,
        "norm_max": 23,
        "max_points": 67,
        "critical": True  # Если превышено - не рекомендован
    }
}

# Маппинг русских названий шкал на коды
RUSSIAN_TO_CODE = {
    "Достоверность": "Isk",
    "Аутоагрессия": "Con",
    "Ранимость": "Ast",
    "Истероидность": "Ist",
    "Психопатическая": "Psi",
    "НПН": "NPN",
    "Нейтральные": "General",
    "Эмоциональные": "Emotional"
}

# app/services/scoring.py

def calculate_scores(answers, questions_map):
    """
    Подсчет баллов по шкалам на основе ответов
    """
    print("🧮 Начинаем подсчет баллов...")
    print(f"📊 Ответов: {len(answers)}")
    print(f"📋 Вопросов в мапе: {len(questions_map)}")
    
    # Инициализируем счетчики
    scores = {scale: 0 for scale in SCALES_NORMS.keys()}
    
    for i, answer in enumerate(answers):
        # 🔥 ПРЕОБРАЗУЕМ объект Answer в словарь если нужно
        if hasattr(answer, 'question_id'):
            # Это объект Pydantic модели
            question_id = str(answer.question_id)
            answer_value = bool(answer.answer)
        else:
            # Это уже словарь
            question_id = str(answer.get("question_id", ""))
            answer_value = bool(answer.get("answer", False))
        
        question = questions_map.get(question_id)
        
        if not question:
            print(f"⚠️ Вопрос {question_id} не найден в мапе")
            continue
        
        # Получаем русские названия шкал из вопроса
        russian_scales = question.get("types", [])
        
        # Преобразуем в коды
        scale_codes = []
        for russian_scale in russian_scales:
            code = RUSSIAN_TO_CODE.get(russian_scale)
            if code:
                scale_codes.append(code)
            else:
                print(f"⚠️ Неизвестная шкала: {russian_scale}")
        
        # Определяем баллы за ответ
        if answer_value:  # Ответ "Да"
            points = question.get("pointsIfYes", 0)
        else:  # Ответ "Нет"
            points = question.get("pointsIfNo", 0)
        
        # Распределяем баллы по шкалам
        if points > 0 and scale_codes:
            for scale_code in scale_codes:
                if scale_code in scores:
                    scores[scale_code] += points
                    print(f"   Вопрос {i+1}: +{points} к {scale_code} ({question_id})")
    
    print(f"📈 Итоговые баллы: {scores}")
    return scores

def interpret_scores(scores):
    """
    Интерпретация результатов по нормам
    
    Args:
        scores: dict - баллы по шкалам
    
    Returns:
        tuple: (interpretations, recommendation)
    """
    print("📊 Интерпретация результатов...")
    
    interpretations = {}
    recommendation = "рекомендован"
    
    for scale, score in scores.items():
        norm = SCALES_NORMS.get(scale)
        if not norm:
            interpretations[scale] = f"{score} баллов"
            continue
        
        norm_max = norm.get("norm_max", 0)
        
        # Шкала достоверности - особый случай
        if scale == "Isk":
            if score > norm_max:
                interpretations[scale] = f"Недостоверен ({score} > {norm_max})"
                if recommendation != "не рекомендован":
                    recommendation = "ретест"
            else:
                interpretations[scale] = f"Достоверен ({score}/{norm_max})"
        
        # Остальные шкалы
        elif score > norm_max:
            interpretations[scale] = f"Превышение ({score} > {norm_max})"
            
            # Если шкала критическая
            if norm.get("critical", False):
                recommendation = "не рекомендован"
            elif recommendation == "рекомендован":
                recommendation = "условно рекомендован"
        else:
            interpretations[scale] = f"Норма ({score}/{norm_max})"
    
    print(f"📋 Интерпретации: {interpretations}")
    print(f"✅ Рекомендация: {recommendation}")
    
    return interpretations, recommendation

def generate_personal_report(user_data, scores, interpretations, recommendation):
    """
    Генерация текстового отчета для пользователя
    
    Args:
        user_data: dict - данные пользователя
        scores: dict - баллы по шкалам
        interpretations: dict - интерпретации
        recommendation: str - рекомендация
    
    Returns:
        str: текстовый отчет
    """
    report = []
    report.append("=" * 50)
    report.append("ПСИХОЛОГИЧЕСКОЕ ТЕСТИРОВАНИЕ")
    report.append("=" * 50)
    report.append(f"Тестируемый: {user_data.get('login', 'Неизвестно')}")
    report.append(f"Дата: {user_data.get('completedAt', 'Не указана')}")
    report.append("")
    
    report.append("РЕЗУЛЬТАТЫ ПО ШКАЛАМ:")
    report.append("-" * 30)
    
    for scale in SCALES_NORMS.keys():
        norm = SCALES_NORMS[scale]
        score = scores.get(scale, 0)
        interpretation = interpretations.get(scale, "Нет данных")
        
        report.append(f"{norm['name']}: {score} баллов")
        report.append(f"  {interpretation}")
        report.append(f"  (Норма: 0-{norm['norm_max']} баллов)")
        report.append("")
    
    report.append("ИТОГОВАЯ РЕКОМЕНДАЦИЯ:")
    report.append("-" * 30)
    
    if recommendation == "рекомендован":
        report.append("✅ РЕКОМЕНДОВАН")
        report.append("Все показатели в пределах нормы.")
    elif recommendation == "условно рекомендован":
        report.append("⚠️ УСЛОВНО РЕКОМЕНДОВАН")
        report.append("Некоторые показатели требуют внимания.")
    elif recommendation == "не рекомендован":
        report.append("❌ НЕ РЕКОМЕНДОВАН")
        report.append("Превышены критические показатели.")
    elif recommendation == "ретест":
        report.append("🔄 ТРЕБУЕТСЯ ПОВТОРНОЕ ТЕСТИРОВАНИЕ")
        report.append("Результаты могут быть недостоверны.")
    
    report.append("")
    report.append("Примечание: Данные результаты носят рекомендательный характер.")
    report.append("=" * 50)
    
    return "\n".join(report)

# Тестовая функция
def test_scoring():
    """Тестирование подсчета баллов"""
    
    print("🧪 Тестирование функции подсчета баллов...")
    
    # Создаем тестовые данные
    test_questions_map = {
        "1": {
            "id": "1",
            "types": ["Достоверность"],
            "pointsIfYes": 1,
            "pointsIfNo": 0
        },
        "2": {
            "id": "2",
            "types": ["Аутоагрессия"],
            "pointsIfYes": 1,
            "pointsIfNo": 0
        },
        "3": {
            "id": "3", 
            "types": ["Ранимость"],
            "pointsIfYes": 0,
            "pointsIfNo": 1
        }
    }
    
    test_answers = [
        {"question_id": "1", "answer": True},
        {"question_id": "2", "answer": True},
        {"question_id": "3", "answer": False}
    ]
    
    scores = calculate_scores(test_answers, test_questions_map)
    interpretations, recommendation = interpret_scores(scores)
    
    print("\n🎯 Результаты теста:")
    print(f"Баллы: {scores}")
    print(f"Интерпретации: {interpretations}")
    print(f"Рекомендация: {recommendation}")
    
    return scores, interpretations, recommendation

if __name__ == "__main__":
    test_scoring()