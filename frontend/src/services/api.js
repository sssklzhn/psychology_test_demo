// // Базовый URL API
// const API_URL = process.env.REACT_APP_API_URL;


// // Получение токена из localStorage
// const getToken = () => {// Получение токена из localStorage
//   // Ищем токен во всех возможных местах
//   return localStorage.getItem('psychology_test_token') || 
//          localStorage.getItem('auth_token') || 
//          localStorage.getItem('access_token') ||
//          localStorage.getItem('token'); // на всякий случай
// };

// // Базовый запрос
// const apiRequest = async (endpoint, options = {}) => {
//   const url = `${API_URL}${endpoint}`;
//   const token = getToken();
  
//   const headers = {
//     'Content-Type': 'application/json',
//     ...(token && { 'Authorization': `Bearer ${token}` }),
//     ...options.headers
//   };
  
//   const config = {
//     ...options,
//     headers
//   };
  
//   try {
//     const response = await fetch(url, config);
    
//     if (!response.ok) {
//       if (response.status === 401) {
//         // Неавторизован - очищаем токен
//         localStorage.removeItem('psychology_test_token');
//         localStorage.removeItem('psychology_test_user');
//         window.location.href = '/login';
//       }
//       throw new Error(`HTTP error! status: ${response.status}`);
//     }
    
//     return await response.json();
//   } catch (error) {
//     console.error('API Error:', error);
//     throw error;
//   }
// };

// // Экспортируем методы API
// export const api = {
//   // Аутентификация
//   login: async (login, password) => {
//     return apiRequest('/auth/login', {
//       method: 'POST',
//       body: JSON.stringify({ login, password })
//     });
//   },
  
//   // Административные функции
//   generateUsers: async (count) => {
//     return apiRequest(`/admin/generate-users?count=${count}`, {
//       method: 'POST'
//     });
//   },
  
//   getUsers: async () => {
//     return apiRequest('/admin/users');
//   },
  
//   // Тестирование
//   getQuestions: async () => {
//     return apiRequest('/questions');
//   },
  
//   submitTest: async (answers) => {
//     return apiRequest('/test/submit', {
//       method: 'POST',
//       body: JSON.stringify({ answers })
//     });
//   },
  
//   getResults: async (userId) => {
//     return apiRequest(`/results/${userId}`);
//   }
// };

// api.js
// Базовый URL API - используем переменную окружения
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Проверка наличия URL
if (!API_URL) {
  console.warn('REACT_APP_API_URL is not defined in environment variables');
}

// Получение токена из localStorage
const getToken = () => {
  return localStorage.getItem('psychology_test_token') || 
         localStorage.getItem('auth_token') || 
         localStorage.getItem('access_token') ||
         localStorage.getItem('token');
};

// Базовый запрос
const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_URL}${endpoint}`;
  const token = getToken();
  
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers
  };
  
  const config = {
    ...options,
    headers
  };
  
  try {
    console.log(`API Request: ${url}`); // Для отладки
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`API Error ${response.status}:`, errorText);
      
      if (response.status === 401) {
        // Неавторизован - очищаем токен и перенаправляем на логин
        localStorage.removeItem('psychology_test_token');
        localStorage.removeItem('auth_token');
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = '/#/login';
        throw new Error('Сессия истекла. Пожалуйста, войдите снова.');
      }
      
      // Пытаемся распарсить ошибку как JSON
      let errorMessage = `HTTP error! status: ${response.status}`;
      try {
        const errorData = JSON.parse(errorText);
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch {
        // Если не JSON, оставляем текст ошибки
        if (errorText) errorMessage = errorText;
      }
      
      throw new Error(errorMessage);
    }
    
    const data = await response.json();
    console.log(`API Response from ${url}:`, data); // Для отладки
    return data;
    
  } catch (error) {
    console.error('API Request Error:', error);
    throw error;
  }
};

// Экспортируем методы API
export const api = {
  // Аутентификация
  login: async (login, password) => {
    return apiRequest('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ login, password })
    });
  },
  
  // Административные функции
  generateUsers: async (count) => {
    return apiRequest(`/api/admin/generate-users?count=${count}`, {
      method: 'POST'
    });
  },
  
  getUsers: async () => {
    return apiRequest('/api/admin/users');
  },
  
  // Функция генерации и скачивания пользователей (как в AdminPage.js)
  generateAndDownloadUsers: async (count) => {
    const token = getToken();
    const response = await fetch(
      `${API_URL}/api/admin/generate-and-download-users?count=${count}`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response;
  },
  
  // Тестирование
  getQuestions: async () => {
    return apiRequest('/api/questions');
  },
  
  submitTest: async (answers) => {
    return apiRequest('/api/test/submit', {
      method: 'POST',
      body: JSON.stringify({ answers })
    });
  },
  
  // Результаты
  getResults: async (userId) => {
    return apiRequest(`/api/results/${userId}`);
  },
  
  // Просмотр ответов пользователя
  getUserAnswers: async (userId) => {
    return apiRequest(`/api/admin/user/${userId}/answers`);
  },
  
  // Генерация PDF отчета пользователя
  generateUserPDF: async (userId) => {
    const token = getToken();
    const response = await fetch(`${API_URL}/api/export/pdf/user/${userId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response;
  },
  
  // Генерация общего PDF отчета
  generateSummaryPDF: async () => {
    const token = getToken();
    const response = await fetch(`${API_URL}/api/export/pdf/summary`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response;
  },
  
  // Экспорт CSV результатов
  exportResultsCSV: async () => {
    const token = getToken();
    const response = await fetch(`${API_URL}/api/export/csv/summary`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response;
  },
  
  // Сброс теста пользователя
  resetUserTest: async (userId) => {
    return apiRequest(`/api/admin/user/${userId}/reset`, {
      method: 'POST'
    });
  },
  
  // Проверка соединения с сервером
  checkConnection: async () => {
    try {
      const response = await fetch(`${API_URL}/api/health`);
      return response.ok;
    } catch (error) {
      console.error('Server connection check failed:', error);
      return false;
    }
  }
};