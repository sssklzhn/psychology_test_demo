import { createElement, clearElement } from '../../utils/helpers.js';
import { authService } from '../../services/auth.js';
import { showNotification } from '../../utils/helpers.js';

export class LoginForm {
    constructor(onLoginSuccess) {
        this.onLoginSuccess = onLoginSuccess;
        this.container = null;
    }
    
    render() {
        this.container = createElement('div', 'login-container');
        
        const card = createElement('div', 'card');
        card.style.maxWidth = '400px';
        card.style.margin = '50px auto';
        
        const title = createElement('h2', '', 'Вход в систему');
        title.style.textAlign = 'center';
        title.style.marginBottom = '30px';
        title.style.color = '#2c3e50';
        
        const form = createElement('form');
        form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Логин
        const loginGroup = createElement('div', 'form-group');
        const loginLabel = createElement('label', 'form-label', 'Логин');
        loginLabel.setAttribute('for', 'login');
        const loginInput = createElement('input', 'form-control');
        loginInput.id = 'login';
        loginInput.type = 'text';
        loginInput.placeholder = 'Тестируемый1 или admin';
        loginInput.required = true;
        loginGroup.appendChild(loginLabel);
        loginGroup.appendChild(loginInput);
        
        // Пароль
        const passwordGroup = createElement('div', 'form-group');
        const passwordLabel = createElement('label', 'form-label', 'Пароль');
        passwordLabel.setAttribute('for', 'password');
        const passwordInput = createElement('input', 'form-control');
        passwordInput.id = 'password';
        passwordInput.type = 'password';
        passwordInput.placeholder = 'Введите пароль';
        passwordInput.required = true;
        passwordGroup.appendChild(passwordLabel);
        passwordGroup.appendChild(passwordInput);
        
        // Кнопка входа
        const submitButton = createElement('button', 'btn btn-primary', 'Войти');
        submitButton.type = 'submit';
        submitButton.style.width = '100%';
        submitButton.style.padding = '12px';
        
        // Демо информация
        const demoInfo = createElement('div', 'alert alert-warning');
        demoInfo.style.marginTop = '20px';
        demoInfo.innerHTML = `
            <strong>Демо доступ:</strong><br>
            • Администратор: login: <code>admin</code>, password: <code>admin123</code><br>
            • Тестируемый: login: <code>Тестируемый1</code>, password: <code>смотрите в CSV</code>
        `;
        
        form.appendChild(loginGroup);
        form.appendChild(passwordGroup);
        form.appendChild(submitButton);
        
        card.appendChild(title);
        card.appendChild(form);
        card.appendChild(demoInfo);
        
        this.container.appendChild(card);
        
        return this.container;
    }
    
    async handleSubmit(event) {
        event.preventDefault();
        
        const login = document.getElementById('login').value;
        const password = document.getElementById('password').value;
        
        const submitButton = event.target.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Вход...';
        submitButton.disabled = true;
        
        try {
            const user = await authService.login(login, password);
            showNotification('Вход выполнен успешно!', 'success');
            
            if (this.onLoginSuccess) {
                this.onLoginSuccess(user);
            }
        } catch (error) {
            showNotification('Ошибка входа. Проверьте логин и пароль.', 'error');
            console.error('Login error:', error);
        } finally {
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        }
    }
    
    destroy() {
        if (this.container && this.container.parentNode) {
            this.container.parentNode.removeChild(this.container);
        }
    }
}