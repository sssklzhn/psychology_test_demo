// Утилиты для работы с DOM и данными
export const createElement = (tag, className = '', textContent = '') => {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (textContent) element.textContent = textContent;
    return element;
};

export const clearElement = (element) => {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
};

export const formatDate = (dateString) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
};

export const generatePassword = (length = 8) => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let password = '';
    for (let i = 0; i < length; i++) {
        password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return password;
};

export const downloadCSV = (data, filename = 'data.csv') => {
    let csvContent = "data:text/csv;charset=utf-8,";
    
    // Заголовки
    const headers = Object.keys(data[0]);
    csvContent += headers.join(",") + "\n";
    
    // Данные
    data.forEach(item => {
        const row = headers.map(header => {
            let cell = item[header] || '';
            // Экранируем кавычки
            if (typeof cell === 'string') {
                cell = cell.replace(/"/g, '""');
                if (cell.includes(',') || cell.includes('"') || cell.includes('\n')) {
                    cell = `"${cell}"`;
                }
            }
            return cell;
        });
        csvContent += row.join(",") + "\n";
    });
    
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};

export const showNotification = (message, type = 'success', duration = 3000) => {
    const notification = createElement('div', `alert alert-${type}`);
    notification.textContent = message;
    
    const container = document.getElementById('notifications') || createNotificationsContainer();
    container.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, duration);
};

const createNotificationsContainer = () => {
    const container = createElement('div', 'notifications');
    container.id = 'notifications';
    container.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        max-width: 400px;
    `;
    document.body.appendChild(container);
    return container;
};