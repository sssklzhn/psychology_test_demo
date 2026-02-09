# app/services/csv_generator.py
import csv
import io
from datetime import datetime

def generate_summary_csv(all_results):
    """Генерация CSV отчета"""
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Заголовки
    headers = [
        'Логин', 'Дата тестирования', 'Статус',
        'Достоверность', 'Аутоагрессия', 'Ранимость',
        'Истероидность', 'Психопатическая', 'НПН',
        'Рекомендация', 'Интерпретация'
    ]
    writer.writerow(headers)
    
    for result in all_results:
        user = result.get('user', {})
        scores = result.get('scores', {})
        
        row = [
            user.get('login', ''),
            user.get('completedAt', ''),
            'Завершено' if user.get('isCompleted') else 'В процессе',
            scores.get('Isk', 0),
            scores.get('Con', 0),
            scores.get('Ast', 0),
            scores.get('Ist', 0),
            scores.get('Psi', 0),
            scores.get('NPN', 0),
            result.get('recommendation', ''),
            '; '.join(result.get('interpretations', {}).values())
        ]
        writer.writerow(row)
    
    return output.getvalue().encode('utf-8-sig')