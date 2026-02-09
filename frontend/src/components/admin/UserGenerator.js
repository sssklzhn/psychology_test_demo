import { createElement, clearElement, downloadCSV } from '../../utils/helpers.js';
import { api } from '../../services/api.js';
import { showNotification } from '../../utils/helpers.js';

export class UserGenerator {
    constructor() {
        this.container = null;
        this.users = [];
    }
    
    render() {
        this.container = createElement('div', 'user-generator');
        
        const card = createElement('div', 'card');
        
        const title = createElement('h3', '', 'Генерация тестируемых');
        title.style.marginBottom = '20px';
        
        // Элементы управления
        const controls = createElement('div', 'controls');
        controls.style.display = 'flex';
        controls.style.gap = '10px';
        controls.style.alignItems = 'center';
        controls.style.marginBottom = '20px';
        controls.style.flexWrap = 'wrap';
        
        // Поле для количества
        const countLabel = createElement('label', '', 'Количество пользователей:');
        const countInput = createElement('input', 'form-control');
        countInput.type = 'number';
        countInput.min = '1';
        countInput.max = '100';
        countInput.value = '10';
        countInput.style.width = '100px';
        
        // Кнопка генерации
        const generateButton = createElement('button', 'btn btn-success', 'Сгенерировать');
        generateButton.addEventListener('click', () => this.generateUsers());
        
        controls.appendChild(countLabel);
        controls.appendChild(countInput);
        controls.appendChild(generateButton);
        
        // Таблица пользователей
        this.usersTable = createElement('div', 'users-table');
        this.usersTable.style.marginTop = '20px';
        
        card.appendChild(title);
        card.appendChild(controls);
        card.appendChild(this.usersTable);
        
        this.container.appendChild(card);
        
        return this.container;
    }
    
    async generateUsers() {
        const countInput = this.container.querySelector('input[type="number"]');
        const count = parseInt(countInput.value);
        const button = this.container.querySelector('.btn-success');
        
        const originalText = button.textContent;
        button.textContent = 'Генерация...';
        button.disabled = true;
        
        try {
            const response = await api.generateUsers(count);
            this.users = response.users;
            
            this.renderUsersTable();
            showNotification(`Создано ${this.users.length} пользователей`, 'success');
            
            // Автоматическое скачивание CSV
            const csvData = this.users.map(user => ({
                Логин: user.login,
                Пароль: user.password
            }));
            downloadCSV(csvData, 'users.csv');
            
        } catch (error) {
            showNotification('Ошибка при создании пользователей', 'error');
            console.error('Generate users error:', error);
        } finally {
            button.textContent = originalText;
            button.disabled = false;
        }
    }
    
    renderUsersTable() {
        clearElement(this.usersTable);
        
        if (this.users.length === 0) {
            return;
        }
        
        const tableTitle = createElement('h4', '', 'Созданные пользователи:');
        tableTitle.style.marginBottom = '15px';
        
        const table = createElement('table', 'table');
        
        // Заголовки таблицы
        const thead = createElement('thead');
        const headerRow = createElement('tr');
        ['№', 'Логин', 'Пароль', 'Действия'].forEach(text => {
            const th = createElement('th', '', text);
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        
        // Тело таблицы
        const tbody = createElement('tbody');
        this.users.forEach((user, index) => {
            const row = createElement('tr');
            
            // №
            const td1 = createElement('td', '', (index + 1).toString());
            
            // Логин
            const td2 = createElement('td', '', user.login);
            
            // Пароль
            const td3 = createElement('td', '', user.password);
            
            // Действия
            const td4 = createElement('td');
            const copyButton = createElement('button', 'btn btn-sm btn-primary', 'Копировать');
            copyButton.style.marginRight = '5px';
            copyButton.addEventListener('click', () => {
                navigator.clipboard.writeText(`${user.login}:${user.password}`);
                showNotification('Логин и пароль скопированы!', 'success');
            });
            td4.appendChild(copyButton);
            
            row.appendChild(td1);
            row.appendChild(td2);
            row.appendChild(td3);
            row.appendChild(td4);
            tbody.appendChild(row);
        });
        
        table.appendChild(thead);
        table.appendChild(tbody);
        
        this.usersTable.appendChild(tableTitle);
        this.usersTable.appendChild(table);
    }
    
    destroy() {
        if (this.container && this.container.parentNode) {
            this.container.parentNode.removeChild(this.container);
        }
    }
}