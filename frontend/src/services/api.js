// Базовый URL API
const API_URL = process.env.REACT_APP_API_URL;


// Получение токена из localStorage
const getToken = () => {// Получение токена из localStorage
  // Ищем токен во всех возможных местах
  return localStorage.getItem('psychology_test_token') || 
         localStorage.getItem('auth_token') || 
         localStorage.getItem('access_token') ||
         localStorage.getItem('token'); // на всякий случай
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
    const response = await fetch(url, config);
    
    if (!response.ok) {
      if (response.status === 401) {
        // Неавторизован - очищаем токен
        localStorage.removeItem('psychology_test_token');
        localStorage.removeItem('psychology_test_user');
        window.location.href = '/login';
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

// Экспортируем методы API
export const api = {
  // Аутентификация
  login: async (login, password) => {
    return apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ login, password })
    });
  },
  
  // Административные функции
  generateUsers: async (count) => {
    return apiRequest(`/admin/generate-users?count=${count}`, {
      method: 'POST'
    });
  },
  
  getUsers: async () => {
    return apiRequest('/admin/users');
  },
  
  // Тестирование
  getQuestions: async () => {
    return apiRequest('/questions');
  },
  
  submitTest: async (answers) => {
    return apiRequest('/test/submit', {
      method: 'POST',
      body: JSON.stringify({ answers })
    });
  },
  
  getResults: async (userId) => {
    return apiRequest(`/results/${userId}`);
  }
};