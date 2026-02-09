import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';

// Найдите корневой элемент
const container = document.getElementById('root');

// Проверьте, что элемент существует
if (!container) {
    console.error('❌ Не найден элемент с id="root"');
    document.body.innerHTML = '<h1 style="color: red; text-align: center; padding: 50px;">Ошибка: не найден корневой элемент</h1>';
} else {
    // Создайте корень React 18
    const root = createRoot(container);
    
    // Рендерите приложение
    root.render(
        <React.StrictMode>
            <App />
        </React.StrictMode>
    );
}