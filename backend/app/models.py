from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

# Модели для запросов/ответов
class UserCreate(BaseModel):
    login: str
    password: str

class UserResponse(BaseModel):
    user_id: str
    login: str
    is_completed: bool
    completed_at: Optional[datetime]

class Question(BaseModel):
    question_id: str
    text: str
    scales: List[str]  
    yes_points: Dict[str, int]  # Баллы за "Да"
    no_points: Dict[str, int]   # Баллы за "Нет"

class Answer(BaseModel):
    question_id: str
    answer: bool  # True = "Да", False = "Нет"

class TestSubmission(BaseModel):
    answers: List[Answer]

class ScoreResult(BaseModel):
    scores: Dict[str, int]
    interpretations: Dict[str, str]
    recommendation: str  

# Нормы по шкалам из Excelки
SCALES_NORMS = {
    "Isk": {"name": "Достоверность", "norm_min": 0, "norm_max": 9, "max_points": 15},
    "Con": {"name": "Аутоагрессия", "norm_min": 0, "norm_max": 6, "max_points": 14},
    "Ast": {"name": "Ранимость", "norm_min": 0, "norm_max": 15, "max_points": 19},
    "Ist": {"name": "Истероидность", "norm_min": 0, "norm_max": 27, "max_points": 30},
    "Psi": {"name": "Психопатия", "norm_min": 0, "norm_max": 13, "max_points": 30},
    "NPN": {"name": "Нервно-психическая неустойчивость", "norm_min": 0, "norm_max": 23, "max_points": 67}
}