// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';

// export const LoginPage = ({ onLogin }) => {
//   const navigate = useNavigate();
//   const [login, setLogin] = useState('');
//   const [password, setPassword] = useState('');
//   const [error, setError] = useState('');
//   const [loading, setLoading] = useState(false);

//   const handleSubmit = async (e) => {
//   e.preventDefault();
//   setError('');
//   setLoading(true);

//   try {
//     const response = await fetch('http://localhost:8000/api/auth/login', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ login, password }),
//     });

//     const data = await response.json();

//     if (!response.ok) {
//       throw new Error(data.detail || 'Ошибка авторизации');
//     }

//     // 🔥 СОХРАНЯЕМ ТОКЕН ВО ВСЕХ МЕСТАХ
//     localStorage.setItem('psychology_test_token', data.access_token);
//     localStorage.setItem('auth_token', data.access_token);           // Для authService.js
//     localStorage.setItem('access_token', data.access_token);         // Для AdminPage.js напрямую
    
//     // Сохраняем пользователя
//     localStorage.setItem('user', JSON.stringify(data.user));
    
//     console.log('✅ Токен сохранен:', {
//       psychology_test_token: localStorage.getItem('psychology_test_token'),
//       auth_token: localStorage.getItem('auth_token'),
//       access_token: localStorage.getItem('access_token'),
//       user: localStorage.getItem('user')
//     });

//     // Вызываем callback из App.js
//     onLogin(data.user, data.access_token);

//     // Перенаправляем в зависимости от роли
//     if (data.user.login === 'admin') {
//       navigate('/admin');
//     } else {
//       navigate('/test');
//     }

//   } catch (err) {
//     setError(err.message || 'Ошибка авторизации');
//   } finally {
//     setLoading(false);
//   }
// };

//   return (
//     <div className="container">
//       <div className="card" style={{ maxWidth: '400px', margin: '50px auto' }}>
//         <h2 style={{ textAlign: 'center', marginBottom: '30px' }}>Вход в систему</h2>
        
//         <form onSubmit={handleSubmit}>
//           <div className="form-group">
//             <label className="form-label">Логин:</label>
//             <input
//               type="text"
//               className="form-control"
//               value={login}
//               onChange={(e) => setLogin(e.target.value)}
//               placeholder="Введите логин"
//               required
//             />
//           </div>
          
//           <div className="form-group">
//             <label className="form-label">Пароль:</label>
//             <input
//               type="password"
//               className="form-control"
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//               placeholder="Введите пароль"
//               required
//             />
//           </div>
          
//           {error && (
//             <div className="alert alert-error">
//               {error}
//             </div>
//           )}
          
//           <button 
//             type="submit" 
//             className="btn btn-primary"
//             style={{ width: '100%', padding: '12px' }}
//             disabled={loading}
//           >
//             {loading ? 'Вход...' : 'Войти'}
//           </button>
//         </form>
        
//         <div className="alert alert-info" style={{ marginTop: '20px' }}>
//           <strong>Демо доступ:</strong><br/>
//           • Администратор: login: <code>admin</code>, password: <code>admin123</code><br/>
//           • Тестируемый: login: <code>Тестируемый1</code>, password: <code>сгенерированный пароль</code>
//         </div>
//       </div>
//     </div>
//   );
// };
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from './../services/authService'; // Импортируем сервис аутентификации

export const LoginPage = ({ onLogin }) => {
  const navigate = useNavigate();
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Используем сервис аутентификации
      const user = await authService.login(login, password);
      
      console.log('✅ Токен сохранен:', {
        psychology_test_token: localStorage.getItem('psychology_test_token'),
        auth_token: localStorage.getItem('auth_token'),
        access_token: localStorage.getItem('access_token'),
        user: localStorage.getItem('user')
      });

      // Вызываем callback из App.js
      onLogin(user, localStorage.getItem('access_token'));

      // Перенаправляем в зависимости от роли
      if (user.login === 'admin') {
        navigate('/admin');
      } else {
        navigate('/test');
      }

    } catch (err) {
      setError(err.message || 'Ошибка авторизации');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: '400px', margin: '50px auto' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '30px' }}>Вход в систему</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Логин:</label>
            <input
              type="text"
              className="form-control"
              value={login}
              onChange={(e) => setLogin(e.target.value)}
              placeholder="Введите логин"
              required
            />
          </div>
          
          <div className="form-group">
            <label className="form-label">Пароль:</label>
            <input
              type="password"
              className="form-control"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Введите пароль"
              required
            />
          </div>
          
          {error && (
            <div className="alert alert-error">
              {error}
            </div>
          )}
          
          <button 
            type="submit" 
            className="btn btn-primary"
            style={{ width: '100%', padding: '12px' }}
            disabled={loading}
          >
            {loading ? 'Вход...' : 'Войти'}
          </button>
        </form>
        
        <div className="alert alert-info" style={{ marginTop: '20px' }}>
          <strong>Демо доступ:</strong><br/>
          • Администратор: login: <code>admin</code>, password: <code>admin123</code><br/>
          • Тестируемый: login: <code>Тестируемый1</code>, password: <code>сгенерированный пароль</code>
        </div>
      </div>
    </div>
  );
};