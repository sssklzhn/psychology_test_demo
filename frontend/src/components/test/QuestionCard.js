import { createElement } from '../../utils/helpers.js';

export class QuestionCard {
    constructor(question, currentIndex, totalQuestions, onAnswer) {
        this.question = question;
        this.currentIndex = currentIndex;
        this.totalQuestions = totalQuestions;
        this.onAnswer = onAnswer;
        this.container = null;
        this.selectedAnswer = null;
    }
    
    render() {
        this.container = createElement('div', 'question-container');
        
        // Прогресс бар
        const progressContainer = createElement('div');
        progressContainer.style.marginBottom = '30px';
        
        const progressText = createElement('div', '', `Вопрос ${this.currentIndex + 1} из ${this.totalQuestions}`);
        progressText.style.textAlign = 'center';
        progressText.style.color = '#6c757d';
        progressText.style.marginBottom = '10px';
        
        const progressBar = createElement('div', 'progress-bar');
        const progressFill = createElement('div', 'progress-fill');
        const progressPercent = ((this.currentIndex + 1) / this.totalQuestions) * 100;
        progressFill.style.width = `${progressPercent}%`;
        progressBar.appendChild(progressFill);
        
        progressContainer.appendChild(progressText);
        progressContainer.appendChild(progressBar);
        
        // Текст вопроса
        const questionCard = createElement('div', 'card');
        questionCard.style.minHeight = '300px';
        questionCard.style.display = 'flex';
        questionCard.style.flexDirection = 'column';
        questionCard.style.justifyContent = 'space-between';
        
        const questionText = createElement('div', 'question-text', this.question.text);
        
        // Кнопки ответов
        const answersContainer = createElement('div', 'answer-buttons');
        
        const yesButton = createElement('button', 'btn answer-btn yes', 'Да');
        yesButton.addEventListener('click', () => this.handleAnswer(true));
        
        const noButton = createElement('button', 'btn answer-btn no', 'Нет');
        noButton.addEventListener('click', () => this.handleAnswer(false));
        
        answersContainer.appendChild(yesButton);
        answersContainer.appendChild(noButton);
        
        questionCard.appendChild(questionText);
        questionCard.appendChild(answersContainer);
        
        this.container.appendChild(progressContainer);
        this.container.appendChild(questionCard);
        
        return this.container;
    }
    
    handleAnswer(answer) {
        this.selectedAnswer = answer;
        
        // Визуальная обратная связь
        const buttons = this.container.querySelectorAll('.answer-btn');
        buttons.forEach(btn => {
            btn.classList.remove('selected');
        });
        
        if (answer) {
            this.container.querySelector('.answer-btn.yes').classList.add('selected');
        } else {
            this.container.querySelector('.answer-btn.no').classList.add('selected');
        }
        
        // Вызываем callback
        if (this.onAnswer) {
            setTimeout(() => {
                this.onAnswer({
                    question_id: this.question.id || this.question.question_id,
                    answer: answer
                });
            }, 300); // Небольшая задержка для анимации
        }
    }
    
    getAnswer() {
        return this.selectedAnswer;
    }
    
    setAnswer(answer) {
        this.selectedAnswer = answer;
        if (this.container) {
            const buttons = this.container.querySelectorAll('.answer-btn');
            buttons.forEach(btn => btn.classList.remove('selected'));
            
            if (answer === true) {
                const yesBtn = this.container.querySelector('.answer-btn.yes');
                if (yesBtn) yesBtn.classList.add('selected');
            } else if (answer === false) {
                const noBtn = this.container.querySelector('.answer-btn.no');
                if (noBtn) noBtn.classList.add('selected');
            }
        }
    }
    
    destroy() {
        if (this.container && this.container.parentNode) {
            this.container.parentNode.removeChild(this.container);
        }
    }
}