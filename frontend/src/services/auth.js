// // Сервис аутентификации
// export const authService = {
//     isAuthenticated() {
//         const token = localStorage.getItem('auth_token');
//         const user = localStorage.getItem('user');
//         return !!(token && user);
//     },
    
//     getCurrentUser() {
//         const userStr = localStorage.getItem('user');
//         return userStr ? JSON.parse(userStr) : null;
//     },
    
//     async login(login, password) {
//     try {
//         // 🔥 ИСПРАВЬТЕ ПУТЬ - должно быть /api/auth/login
//         const response = await fetch('http://localhost:8000/api/auth/login', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({ login, password })
//         });
        
//         if (!response.ok) {
//             throw new Error('Ошибка авторизации');
//         }
        
//         const data = await response.json();
        
//         // 🔥 СОХРАНЯЕМ ВО ВСЕХ МЕСТАХ
//         localStorage.setItem('auth_token', data.access_token);
//         localStorage.setItem('psychology_test_token', data.access_token);
//         localStorage.setItem('access_token', data.access_token);
//         localStorage.setItem('user', JSON.stringify(data.user));
        
//         console.log('✅ authService: токен сохранен');
        
//         return data.user;
//     } catch (error) {
//         console.error('Login error:', error);
//         throw error;
//     }
// },
    
//     logout() {
//         localStorage.removeItem('auth_token');
//         localStorage.removeItem('user');
//         window.location.hash = '#/login';
//     },
    
//     requireAuth() {
//         if (!this.isAuthenticated()) {
//             window.location.hash = '#/login';
//             return false;
//         }
//         return true;
//     },
    
//     requireAdmin() {
//         if (!this.isAuthenticated()) {
//             window.location.hash = '#/login';
//             return false;
//         }
        
//         const user = this.getCurrentUser();
//         if (user.login !== 'admin') {
//             window.location.hash = '#/test';
//             return false;
//         }
        
//         return true;
//     }
// };

import { api } from './api'; // Импортируем централизованный API

export const authService = {
    isAuthenticated() {
        const token = localStorage.getItem('auth_token');
        const user = localStorage.getItem('user');
        return !!(token && user);
    },

    getCurrentUser() {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    },

    async login(login, password) {
        try {
            // Используем централизованный API
            const data = await api.login(login, password);

            // Сохраняем токен и пользователя
            localStorage.setItem('auth_token', data.access_token);
            localStorage.setItem('psychology_test_token', data.access_token);
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));

            console.log('✅ authService: токен сохранен');

            return data.user;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    },

    logout() {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
        window.location.hash = '#/login';
    },

    requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.hash = '#/login';
            return false;
        }
        return true;
    },

    requireAdmin() {
        if (!this.isAuthenticated()) {
            window.location.hash = '#/login';
            return false;
        }

        const user = this.getCurrentUser();
        if (user.login !== 'admin') {
            window.location.hash = '#/test';
            return false;
        }

        return true;
    }
};
