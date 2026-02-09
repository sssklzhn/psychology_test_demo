# # app/services/pdf_generator.py
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib import colors
# from reportlab.lib.units import cm
# from datetime import datetime
# import io
# import unicodedata

# def safe_string(text):
#     """Безопасное преобразование строки для PDF"""
#     if text is None:
#         return ""
    
#     # Преобразуем в строку
#     text = str(text)
    
#     # Убираем непечатаемые символы и нормализуем
#     text = unicodedata.normalize('NFKD', text)
#     text = ''.join(c for c in text if not unicodedata.combining(c))
    
#     # Заменяем проблемные символы
#     text = text.encode('ascii', 'ignore').decode('ascii')
    
#     return text

# def generate_user_pdf(user_data, results):
#     """
#     Генерация индивидуального отчета в PDF
#     """
#     buffer = io.BytesIO()
    
#     try:
#         # Создаем документ
#         doc = SimpleDocTemplate(
#             buffer,
#             pagesize=A4,
#             rightMargin=72,
#             leftMargin=72,
#             topMargin=72,
#             bottomMargin=72
#         )
        
#         elements = []
#         styles = getSampleStyleSheet()
        
#         # Используем только ASCII заголовки
#         elements.append(Paragraph("PSYCHOLOGY TEST REPORT", styles['Heading1']))
#         elements.append(Spacer(1, 20))
        
#         # Информация о пользователе (безопасные строки)
#         login = safe_string(user_data.get('login', 'Unknown'))
#         date_str = safe_string(user_data.get('completedAt', datetime.now().strftime('%Y-%m-%d')))
        
#         elements.append(Paragraph(f"User: {login}", styles['Normal']))
#         elements.append(Paragraph(f"Date: {date_str}", styles['Normal']))
#         elements.append(Paragraph(f"Status: {'Completed' if user_data.get('isCompleted') else 'Not completed'}", styles['Normal']))
#         elements.append(Spacer(1, 20))
        
#         # Результаты
#         elements.append(Paragraph("TEST RESULTS", styles['Heading2']))
        
#         scores = results.get('scores', {})
#         if scores:
#             data = [['Scale', 'Points']]
            
#             # Английские названия шкал
#             scale_names = {
#                 'Isk': 'Reliability',
#                 'Con': 'Autoaggression',
#                 'Ast': 'Vulnerability',
#                 'Ist': 'Hysteroid',
#                 'Psi': 'Psychopathic',
#                 'NPN': 'Neuro-Psychic'
#             }
            
#             for scale_code, scale_name in scale_names.items():
#                 score = scores.get(scale_code, 0)
#                 data.append([scale_name, str(score)])
            
#             table = Table(data, colWidths=[4*cm, 2*cm])
#             table.setStyle(TableStyle([
#                 ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                 ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
#                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                 ('FONTSIZE', (0, 0), (-1, 0), 12),
#                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                 ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
#                 ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#                 ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#                 ('FONTSIZE', (0, 1), (-1, -1), 10),
#                 ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ]))
            
#             elements.append(table)
#             elements.append(Spacer(1, 20))
        
#         # Рекомендация
#         recommendation = results.get('recommendation', 'no data')
#         elements.append(Paragraph("RECOMMENDATION", styles['Heading2']))
        
#         # Преобразуем рекомендацию на английский
#         rec_map = {
#             'рекомендован': 'RECOMMENDED',
#             'условно рекомендован': 'CONDITIONALLY RECOMMENDED', 
#             'не рекомендован': 'NOT RECOMMENDED',
#             'ретест': 'RETEST REQUIRED'
#         }
        
#         clean_rec = rec_map.get(recommendation, recommendation.upper())
#         elements.append(Paragraph(clean_rec, styles['Normal']))
        
#         elements.append(Spacer(1, 20))
#         elements.append(Paragraph("Note: Report generated automatically", ParagraphStyle(
#             'Note',
#             parent=styles['Italic'],
#             fontSize=8,
#             textColor=colors.grey
#         )))
        
#         # Генерируем PDF
#         doc.build(elements)
        
#     except Exception as e:
#         print(f"PDF generation error: {e}")
#         # Создаем простейший PDF в случае ошибки
#         buffer = io.BytesIO()
#         from reportlab.pdfgen import canvas
#         c = canvas.Canvas(buffer, pagesize=A4)
#         c.setFont("Helvetica", 12)
#         c.drawString(100, 750, "Psychology Test Report")
#         c.drawString(100, 730, f"User: {safe_string(user_data.get('login', 'Unknown'))}")
#         c.drawString(100, 710, "Error in report generation")
#         c.save()
    
#     # Получаем байты
#     pdf_bytes = buffer.getvalue()
#     buffer.close()
    
#     return pdf_bytes

# def generate_summary_pdf(all_results):
#     """
#     Генерация сводного отчета по всем пользователям
#     """
#     buffer = io.BytesIO()
    
#     try:
#         doc = SimpleDocTemplate(
#             buffer,
#             pagesize=A4,
#             rightMargin=72,
#             leftMargin=72,
#             topMargin=72,
#             bottomMargin=72
#         )
        
#         elements = []
#         styles = getSampleStyleSheet()
        
#         elements.append(Paragraph("SUMMARY TEST REPORT", styles['Heading1']))
#         elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
#         elements.append(Spacer(1, 20))
        
#         elements.append(Paragraph(f"Total tested: {len(all_results)}", styles['Heading2']))
#         elements.append(Spacer(1, 10))
        
#         if all_results:
#             # Статистика рекомендаций
#             stats = {
#                 'RECOMMENDED': 0,
#                 'CONDITIONALLY': 0,
#                 'NOT RECOMMENDED': 0,
#                 'RETEST': 0
#             }
            
#             for result in all_results:
#                 rec = result.get('recommendation', '')
#                 if 'рекомендован' in rec and 'условно' not in rec:
#                     stats['RECOMMENDED'] += 1
#                 elif 'условно' in rec:
#                     stats['CONDITIONALLY'] += 1
#                 elif 'не рекомендован' in rec:
#                     stats['NOT RECOMMENDED'] += 1
#                 elif 'ретест' in rec:
#                     stats['RETEST'] += 1
            
#             # Таблица статистики
#             stats_data = [['Recommendation', 'Count']]
#             for rec_type, count in stats.items():
#                 stats_data.append([rec_type, str(count)])
            
#             stats_table = Table(stats_data, colWidths=[5*cm, 3*cm])
#             stats_table.setStyle(TableStyle([
#                 ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
#                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#                 ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
#                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                 ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
#                 ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ]))
            
#             elements.append(stats_table)
#             elements.append(Spacer(1, 20))
            
#             # Список пользователей
#             elements.append(Paragraph("Users list:", styles['Heading3']))
#             for i, result in enumerate(all_results[:20], 1):  # Ограничим 20 пользователей
#                 user = result.get('user', {})
#                 login = safe_string(user.get('login', f'User{i}'))
#                 rec = result.get('recommendation', '')
                
#                 # Упрощаем рекомендацию
#                 if 'рекомендован' in rec and 'условно' not in rec:
#                     rec_short = 'OK'
#                 elif 'условно' in rec:
#                     rec_short = 'COND'
#                 elif 'не рекомендован' in rec:
#                     rec_short = 'NO'
#                 elif 'ретест' in rec:
#                     rec_short = 'RETEST'
#                 else:
#                     rec_short = '?'
                
#                 elements.append(Paragraph(f"{i}. {login} - {rec_short}", styles['Normal']))
            
#             if len(all_results) > 20:
#                 elements.append(Paragraph(f"... and {len(all_results) - 20} more users", styles['Normal']))
        
#         else:
#             elements.append(Paragraph("No test results available", styles['Normal']))
        
#         doc.build(elements)
        
#     except Exception as e:
#         print(f"Summary PDF error: {e}")
#         # Простой PDF в случае ошибки
#         buffer = io.BytesIO()
#         from reportlab.pdfgen import canvas
#         c = canvas.Canvas(buffer, pagesize=A4)
#         c.setFont("Helvetica", 12)
#         c.drawString(100, 750, "Summary Test Report")
#         c.drawString(100, 730, f"Total users: {len(all_results)}")
#         c.drawString(100, 710, "Simplified report due to error")
#         c.save()
    
#     pdf_bytes = buffer.getvalue()
#     buffer.close()
    
#     return pdf_bytes
# app/services/pdf_generator.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from datetime import datetime
import io

def transliterate(text):
    """Преобразует кириллицу в латиницу"""
    if not text:
        return ""
    
    # Словарь транслитерации
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D',
        'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
        'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
        'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch',
        'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
        'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
        ' ': ' ', '-': '-', '_': '_', '.': '.', ',': ',',
        ':': ':', ';': ';', '!': '!', '?': '?', '(': '(',
        ')': ')', '[': '[', ']': ']', '{': '{', '}': '}'
    }
    
    result = []
    for char in str(text):
        if char in translit_dict:
            result.append(translit_dict[char])
        elif 'a' <= char <= 'z' or 'A' <= char <= 'Z' or '0' <= char <= '9':
            result.append(char)
        else:
            result.append('?')
    
    return ''.join(result)

def generate_user_pdf(user_data, results):
    """Генерация PDF - ТОЛЬКО ASCII текст"""
    buffer = io.BytesIO()
    
    try:
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        margin = 20 * mm
        y = height - margin
        
        # ТОЛЬКО ASCII заголовок
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin, y, "PSYCHOLOGY TEST REPORT")
        y -= 25
        
        # Информация о пользователе
        c.setFont("Helvetica", 12)
        login = transliterate(user_data.get('login', 'Unknown'))
        c.drawString(margin, y, f"User: {login}")
        y -= 20
        
        date_str = user_data.get('completedAt', datetime.now().strftime('%Y-%m-%d'))
        c.drawString(margin, y, f"Date: {date_str}")
        y -= 20
        
        status = "Completed" if user_data.get('isCompleted') else "Not completed"
        c.drawString(margin, y, f"Status: {status}")
        y -= 30
        
        # Результаты
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y, "TEST RESULTS BY SCALES:")
        y -= 25
        
        scores = results.get('scores', {})
        
        # Английские названия шкал
        scale_names = {
            'Isk': 'Reliability',
            'Con': 'Autoaggression',
            'Ast': 'Vulnerability',
            'Ist': 'Hysteroid',
            'Psi': 'Psychopathic',
            'NPN': 'Neuro-psychic instability'
        }
        
        c.setFont("Helvetica", 10)
        
        # Заголовок таблицы
        c.drawString(margin, y, "Scale")
        c.drawString(margin + 80, y, "Points")
        y -= 20
        
        # Линия
        c.line(margin, y, width - margin, y)
        y -= 15
        
        # Данные
        for scale_code, scale_name in scale_names.items():
            if y < margin + 50:
                c.showPage()
                y = height - margin
                c.setFont("Helvetica", 10)
            
            score = scores.get(scale_code, 0)
            c.drawString(margin, y, scale_name)
            c.drawString(margin + 80, y, str(score))
            y -= 20
        
        y -= 20
        
        # Рекомендация
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y, "RECOMMENDATION:")
        y -= 25
        
        c.setFont("Helvetica", 12)
        recommendation = results.get('recommendation', 'no data')
        
        # Только английские рекомендации
        if recommendation == "рекомендован":
            rec_text = "RECOMMENDED - All indicators normal."
        elif recommendation == "условно рекомендован":
            rec_text = "CONDITIONALLY RECOMMENDED - Some indicators need attention."
        elif recommendation == "не рекомендован":
            rec_text = "NOT RECOMMENDED - Critical indicators exceeded."
        elif recommendation == "ретест":
            rec_text = "RETEST REQUIRED - Results may be unreliable."
        else:
            rec_text = transliterate(recommendation)
        
        # Разбиваем длинный текст
        words = rec_text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= 70:
                current_line += " " + word if current_line else word
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        for line in lines:
            if y < margin + 50:
                c.showPage()
                y = height - margin
                c.setFont("Helvetica", 12)
            c.drawString(margin, y, line)
            y -= 20
        
        # Подпись
        y -= 30
        c.setFont("Helvetica", 10)
        c.drawString(margin, y, "Report generated automatically")
        c.drawString(width - margin - 100, y, datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        c.save()
        
    except Exception as e:
        print(f"PDF generation error: {e}")
        # Абсолютно простой PDF
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, "Test Report")
        c.drawString(100, 730, "Simplified version")
        c.drawString(100, 710, f"User: {user_data.get('login', 'User')[:20]}")
        c.save()
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

def generate_summary_pdf(all_results):
    """Сводный отчет - ТОЛЬКО ASCII"""
    buffer = io.BytesIO()
    
    try:
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        margin = 20 * mm
        y = height - margin
        
        # Заголовок
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin, y, "SUMMARY TEST REPORT")
        y -= 25
        
        c.setFont("Helvetica", 12)
        c.drawString(margin, y, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        y -= 20
        
        c.drawString(margin, y, f"Total tested: {len(all_results)}")
        y -= 30
        
        if all_results:
            # Статистика
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin, y, "STATISTICS:")
            y -= 25
            
            stats = {'RECOMMENDED': 0, 'CONDITIONAL': 0, 'NOT RECOMMENDED': 0, 'RETEST': 0}
            
            for result in all_results:
                rec = result.get('recommendation', '')
                if 'рекомендован' in rec and 'условно' not in rec:
                    stats['RECOMMENDED'] += 1
                elif 'условно' in rec:
                    stats['CONDITIONAL'] += 1
                elif 'не рекомендован' in rec:
                    stats['NOT RECOMMENDED'] += 1
                elif 'ретест' in rec:
                    stats['RETEST'] += 1
            
            c.setFont("Helvetica", 12)
            for rec_type, count in stats.items():
                c.drawString(margin, y, f"{rec_type}: {count}")
                y -= 20
            
            y -= 20
            
            # Список пользователей
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin, y, "USERS LIST:")
            y -= 25
            
            c.setFont("Helvetica", 10)
            for i, result in enumerate(all_results[:50], 1):
                if y < margin + 50:
                    c.showPage()
                    y = height - margin
                    c.setFont("Helvetica", 10)
                
                user = result.get('user', {})
                login = transliterate(user.get('login', f'User{i}'))
                rec = result.get('recommendation', '')
                
                # Сокращаем рекомендацию
                if 'рекомендован' in rec and 'условно' not in rec:
                    rec_short = 'OK'
                elif 'условно' in rec:
                    rec_short = 'COND'
                elif 'не рекомендован' in rec:
                    rec_short = 'NO'
                elif 'ретест' in rec:
                    rec_short = 'RETEST'
                else:
                    rec_short = '?'
                
                # Обрезаем логин
                login_display = login if len(login) <= 25 else login[:22] + "..."
                
                c.drawString(margin, y, f"{i:3d}. {login_display:<30} - {rec_short}")
                y -= 15
            
            if len(all_results) > 50:
                c.showPage()
                y = height - margin
                c.setFont("Helvetica", 10)
                c.drawString(margin, y, f"... and {len(all_results) - 50} more users")
        
        c.save()
        
    except Exception as e:
        print(f"Summary PDF error: {e}")
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, "Summary Report")
        c.drawString(100, 730, f"Total: {len(all_results)} users")
        c.save()
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes