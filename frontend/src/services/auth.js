// // // Сервис аутентификации
// // export const authService = {
// //     isAuthenticated() {
// //         const token = localStorage.getItem('auth_token');
// //         const user = localStorage.getItem('user');
// //         return !!(token && user);
// //     },
    
// //     getCurrentUser() {
// //         const userStr = localStorage.getItem('user');
// //         return userStr ? JSON.parse(userStr) : null;
// //     },
    
// //     async login(login, password) {
// //     try {
// //         // 🔥 ИСПРАВЬТЕ ПУТЬ - должно быть /api/auth/login
// //         const response = await fetch('http://localhost:8000/api/auth/login', {
// //             method: 'POST',
// //             headers: {
// //                 'Content-Type': 'application/json'
// //             },
// //             body: JSON.stringify({ login, password })
// //         });
        
// //         if (!response.ok) {
// //             throw new Error('Ошибка авторизации');
// //         }
        
// //         const data = await response.json();
        
// //         // 🔥 СОХРАНЯЕМ ВО ВСЕХ МЕСТАХ
// //         localStorage.setItem('auth_token', data.access_token);
// //         localStorage.setItem('psychology_test_token', data.access_token);
// //         localStorage.setItem('access_token', data.access_token);
// //         localStorage.setItem('user', JSON.stringify(data.user));
        
// //         console.log('✅ authService: токен сохранен');
        
// //         return data.user;
// //     } catch (error) {
// //         console.error('Login error:', error);
// //         throw error;
// //     }
// // },
    
// //     logout() {
// //         localStorage.removeItem('auth_token');
// //         localStorage.removeItem('user');
// //         window.location.hash = '#/login';
// //     },
    
// //     requireAuth() {
// //         if (!this.isAuthenticated()) {
// //             window.location.hash = '#/login';
// //             return false;
// //         }
// //         return true;
// //     },
    
// //     requireAdmin() {
// //         if (!this.isAuthenticated()) {
// //             window.location.hash = '#/login';
// //             return false;
// //         }
        
// //         const user = this.getCurrentUser();
// //         if (user.login !== 'admin') {
// //             window.location.hash = '#/test';
// //             return false;
// //         }
        
// //         return true;
// //     }
// // };

// import { api } from './api'; // Импортируем централизованный API

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
//         try {
//             // Используем централизованный API
//             const data = await api.login(login, password);

//             // Сохраняем токен и пользователя
//             localStorage.setItem('auth_token', data.access_token);
//             localStorage.setItem('psychology_test_token', data.access_token);
//             localStorage.setItem('access_token', data.access_token);
//             localStorage.setItem('user', JSON.stringify(data.user));

//             console.log('✅ authService: токен сохранен');

//             return data.user;
//         } catch (error) {
//             console.error('Login error:', error);
//             throw error;
//         }
//     },

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


// authService.js
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

            // Сохраняем токен и пользователя во всех возможных местах
            if (data.access_token) {
                localStorage.setItem('auth_token', data.access_token);
                localStorage.setItem('psychology_test_token', data.access_token);
                localStorage.setItem('access_token', data.access_token);
            }
            
            if (data.user) {
                localStorage.setItem('user', JSON.stringify(data.user));
                localStorage.setItem('psychology_test_user', JSON.stringify(data.user));
            }

            console.log('✅ authService: токен сохранен');
            console.log('👤 Пользователь:', data.user?.login);
            console.log('🔑 Токен (первые 20 символов):', data.access_token?.substring(0, 20) + '...');

            return data.user;
        } catch (error) {
            console.error('Login error:', error);
            // Добавляем более информативное сообщение об ошибке
            if (error.message.includes('Failed to fetch')) {
                throw new Error('Не удалось подключиться к серверу. Проверьте подключение к интернету.');
            } else if (error.message.includes('401')) {
                throw new Error('Неверный логин или пароль');
            } else {
                throw new Error(error.message || 'Ошибка авторизации');
            }
        }
    },

    logout() {
        // Очищаем все токены и данные пользователя
        localStorage.removeItem('auth_token');
        localStorage.removeItem('psychology_test_token');
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        localStorage.removeItem('psychology_test_user');
        window.location.hash = '#/login';
    },

    requireAuth() {
        if (!this.isAuthenticated()) {
            console.log('⚠️ Требуется авторизация - перенаправление на /login');
            window.location.hash = '#/login';
            return false;
        }
        return true;
    },

    requireAdmin() {
        if (!this.isAuthenticated()) {
            console.log('⚠️ Требуется авторизация - перенаправление на /login');
            window.location.hash = '#/login';
            return false;
        }

        const user = this.getCurrentUser();
        if (!user || user.login !== 'admin') {
            console.log('⚠️ Требуются права администратора - перенаправление на /test');
            window.location.hash = '#/test';
            return false;
        }

        return true;
    },
    
    // Дополнительные методы для удобства
    getToken() {
        return localStorage.getItem('auth_token') || 
               localStorage.getItem('psychology_test_token') || 
               localStorage.getItem('access_token');
    },
    
    checkTokenValidity() {
        const token = this.getToken();
        if (!token) return false;
        
        // Можно добавить проверку срока действия токена, если есть JWT
        try {
            // Пример проверки JWT (если токен в формате JWT)
            const payload = JSON.parse(atob(token.split('.')[1]));
            if (payload.exp && payload.exp * 1000 < Date.now()) {
                console.log('❌ Токен истек');
                this.logout();
                return false;
            }
            return true;
        } catch {
            // Если токен не JWT или произошла ошибка при парсинге
            return !!token;
        }
    },
    
    // Инициализация при загрузке приложения
    initialize() {
        console.log('🔐 Инициализация authService');
        console.log('📊 Статус аутентификации:', this.isAuthenticated() ? '✅ Авторизован' : '❌ Не авторизован');
        console.log('👤 Текущий пользователь:', this.getCurrentUser()?.login || 'Нет');
        
        // Проверяем токен при загрузке
        if (this.isAuthenticated() && !this.checkTokenValidity()) {
            console.log('⚠️ Токен недействителен, выполняем выход');
            this.logout();
        }
    }
};