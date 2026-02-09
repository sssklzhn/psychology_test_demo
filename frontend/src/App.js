// import React, { useState, useEffect } from 'react';
// import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
// import { LoginPage } from './pages/LoginPage';
// import { AdminPage } from './pages/AdminPage';
// import { TestPage } from './pages/TestPage';
// import './App.css';

// function App() {
//   const [isLoading, setIsLoading] = useState(true);
//   const [user, setUser] = useState(null);

//   useEffect(() => {
//     // Проверяем авторизацию при загрузке
//     const storedUser = localStorage.getItem('psychology_test_user');
//     const storedToken = localStorage.getItem('psychology_test_token');
    
//     if (storedUser && storedToken) {
//       setUser(JSON.parse(storedUser));
//     }
    
//     setIsLoading(false);
//   }, []);

//   const handleLogin = (userData, token) => {
//     setUser(userData);
//     localStorage.setItem('psychology_test_user', JSON.stringify(userData));
//     localStorage.setItem('psychology_test_token', token);
//   };

//   const handleLogout = () => {
//     setUser(null);
//     localStorage.removeItem('psychology_test_user');
//     localStorage.removeItem('psychology_test_token');
//     window.location.href = '/login';
//   };

//   if (isLoading) {
//     return (
//       <div style={styles.loadingContainer}>
//         <div style={styles.loadingSpinner}></div>
//         <p style={styles.loadingText}>Загрузка приложения...</p>
//       </div>
//     );
//   }

//   return (
//     <Router>
//       <div style={styles.app}>
//         <header style={styles.header}>
//           <h1 style={styles.title}>Психологическое тестирование</h1>
//           <p style={styles.subtitle}>Тест для оценки психологических качеств охранников</p>
          
//           {user && (
//             <div style={styles.userInfo}>
//               <span style={styles.userName}>
//                 {user.login === 'admin' ? '👑 Администратор' : `👤 ${user.login}`}
//               </span>
//               <button 
//                 onClick={handleLogout}
//                 style={styles.logoutButton}
//               >
//                 Выйти
//               </button>
//             </div>
//           )}
//         </header>

//         <main style={styles.main}>
//           <Routes>
//             <Route 
//               path="/" 
//               element={
//                 user ? (
//                   user.login === 'admin' ? (
//                     <Navigate to="/admin" />
//                   ) : (
//                     <Navigate to="/test" />
//                   )
//                 ) : (
//                   <Navigate to="/login" />
//                 )
//               } 
//             />
            
//             <Route 
//               path="/login" 
//               element={
//                 user ? (
//                   user.login === 'admin' ? (
//                     <Navigate to="/admin" />
//                   ) : (
//                     <Navigate to="/test" />
//                   )
//                 ) : (
//                   <LoginPage onLogin={handleLogin} />
//                 )
//               } 
//             />
            
//             <Route 
//               path="/admin" 
//               element={
//                 user && user.login === 'admin' ? (
//                   <AdminPage onLogout={handleLogout} />
//                 ) : (
//                   <Navigate to="/login" />
//                 )
//               } 
//             />
            
//             <Route 
//               path="/test" 
//               element={
//                 user && user.login !== 'admin' ? (
//                   <TestPage user={user} onLogout={handleLogout} />
//                 ) : (
//                   <Navigate to="/login" />
//                 )
//               } 
//             />
//           </Routes>
//         </main>

//         <footer style={styles.footer}>
//           <p>© {new Date().getFullYear()} Психологическое тестирование. Все права защищены.</p>
//           <p style={styles.footerNote}>Тест состоит из 160 вопросов и оценивает 6 психологических шкал</p>
//         </footer>
//       </div>
//     </Router>
//   );
// }

// const styles = {
//   app: {
//     minHeight: '100vh',
//     display: 'flex',
//     flexDirection: 'column',
//     backgroundColor: '#f8f9fa',
//     fontFamily: 'Arial, sans-serif'
//   },
//   loadingContainer: {
//     display: 'flex',
//     flexDirection: 'column',
//     justifyContent: 'center',
//     alignItems: 'center',
//     height: '100vh',
//     backgroundColor: '#f8f9fa'
//   },
//   loadingSpinner: {
//     width: '50px',
//     height: '50px',
//     border: '5px solid #f3f3f3',
//     borderTop: '5px solid #3498db',
//     borderRadius: '50%',
//     animation: 'spin 1s linear infinite',
//     marginBottom: '20px'
//   },
//   loadingText: {
//     color: '#666',
//     fontSize: '18px'
//   },
//   header: {
//     backgroundColor: '#2c3e50',
//     color: 'white',
//     padding: '20px 40px',
//     textAlign: 'center',
//     position: 'relative'
//   },
//   title: {
//     margin: '0 0 10px 0',
//     fontSize: '28px',
//     fontWeight: '600'
//   },
//   subtitle: {
//     margin: '0',
//     fontSize: '16px',
//     opacity: '0.9'
//   },
//   userInfo: {
//     position: 'absolute',
//     right: '40px',
//     top: '50%',
//     transform: 'translateY(-50%)',
//     display: 'flex',
//     alignItems: 'center',
//     gap: '20px'
//   },
//   userName: {
//     fontSize: '14px',
//     fontWeight: '500',
//     backgroundColor: 'rgba(255, 255, 255, 0.1)',
//     padding: '5px 15px',
//     borderRadius: '20px'
//   },
//   logoutButton: {
//     backgroundColor: '#e74c3c',
//     color: 'white',
//     border: 'none',
//     padding: '8px 16px',
//     borderRadius: '4px',
//     cursor: 'pointer',
//     fontSize: '14px',
//     fontWeight: '500',
//     transition: 'background-color 0.3s'
//   },
//   main: {
//     flex: '1',
//     padding: '40px 20px',
//     maxWidth: '1200px',
//     width: '100%',
//     margin: '0 auto'
//   },
//   footer: {
//     backgroundColor: '#2c3e50',
//     color: 'white',
//     padding: '20px',
//     textAlign: 'center',
//     fontSize: '14px'
//   },
//   footerNote: {
//     margin: '10px 0 0 0',
//     fontSize: '12px',
//     opacity: '0.8'
//   }
// };

// // Добавляем стили для анимации
// const styleSheet = document.createElement('style');
// styleSheet.textContent = `
//   @keyframes spin {
//     0% { transform: rotate(0deg); }
//     100% { transform: rotate(360deg); }
//   }
// `;
// document.head.appendChild(styleSheet);

// export default App;

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from './pages/LoginPage';
import { AdminPage } from './pages/AdminPage';
import { TestPage } from './pages/TestPage';
import { authService } from './services/authService';
import './App.css';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Инициализируем сервис аутентификации
    authService.initialize();
    
    // Проверяем авторизацию при загрузке
    const currentUser = authService.getCurrentUser();
    const token = authService.getToken();
    
    console.log('🔍 Проверка авторизации при загрузке:');
    console.log('👤 Пользователь из localStorage:', currentUser);
    console.log('🔑 Токен:', token ? 'Присутствует' : 'Отсутствует');
    
    if (currentUser && token) {
      setUser(currentUser);
      console.log('✅ Авторизованный пользователь:', currentUser.login);
    } else {
      console.log('⚠️ Пользователь не авторизован');
    }
    
    setIsLoading(false);
  }, []);

  const handleLogin = (userData, token) => {
    console.log('✅ Пользователь вошел:', userData.login);
    setUser(userData);
  };

  const handleLogout = () => {
    console.log('👋 Пользователь вышел');
    setUser(null);
    authService.logout(); // Используем сервис для выхода
  };

  if (isLoading) {
    return (
      <div style={styles.loadingContainer}>
        <div style={styles.loadingSpinner}></div>
        <p style={styles.loadingText}>Загрузка приложения...</p>
      </div>
    );
  }

  return (
    <Router>
      <div style={styles.app}>
        <header style={styles.header}>
          <h1 style={styles.title}>Психологическое тестирование</h1>
          <p style={styles.subtitle}>Тест для оценки психологических качеств охранников</p>
          
          {user && (
            <div style={styles.userInfo}>
              <span style={styles.userName}>
                {user.login === 'admin' ? '👑 Администратор' : `👤 ${user.login}`}
              </span>
              <button 
                onClick={handleLogout}
                style={styles.logoutButton}
                onMouseEnter={(e) => e.target.style.backgroundColor = '#c0392b'}
                onMouseLeave={(e) => e.target.style.backgroundColor = '#e74c3c'}
              >
                Выйти
              </button>
            </div>
          )}
        </header>

        <main style={styles.main}>
          <Routes>
            <Route 
              path="/" 
              element={
                user ? (
                  user.login === 'admin' ? (
                    <Navigate to="/admin" replace />
                  ) : (
                    <Navigate to="/test" replace />
                  )
                ) : (
                  <Navigate to="/login" replace />
                )
              } 
            />
            
            <Route 
              path="/login" 
              element={
                user ? (
                  user.login === 'admin' ? (
                    <Navigate to="/admin" replace />
                  ) : (
                    <Navigate to="/test" replace />
                  )
                ) : (
                  <LoginPage onLogin={handleLogin} />
                )
              } 
            />
            
            <Route 
              path="/admin" 
              element={
                user && user.login === 'admin' ? (
                  <AdminPage onLogout={handleLogout} />
                ) : (
                  <Navigate to="/login" replace />
                )
              } 
            />
            
            <Route 
              path="/test" 
              element={
                user && user.login !== 'admin' ? (
                  <TestPage user={user} onLogout={handleLogout} />
                ) : (
                  <Navigate to="/login" replace />
                )
              } 
            />
            
            {/* Резервный маршрут для несуществующих путей */}
            <Route 
              path="*" 
              element={<Navigate to="/" replace />} 
            />
          </Routes>
        </main>

        <footer style={styles.footer}>
          <p>© {new Date().getFullYear()} Психологическое тестирование. Все права защищены.</p>
          <p style={styles.footerNote}>
            Тест состоит из 160 вопросов и оценивает 6 психологических шкал |
            API: {process.env.REACT_APP_API_URL || 'http://localhost:5000'}
          </p>
        </footer>
      </div>
    </Router>
  );
}

const styles = {
  app: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: '#f8f9fa',
    fontFamily: 'Arial, sans-serif'
  },
  loadingContainer: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    backgroundColor: '#f8f9fa'
  },
  loadingSpinner: {
    width: '50px',
    height: '50px',
    border: '5px solid #f3f3f3',
    borderTop: '5px solid #3498db',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
    marginBottom: '20px'
  },
  loadingText: {
    color: '#666',
    fontSize: '18px'
  },
  header: {
    backgroundColor: '#2c3e50',
    color: 'white',
    padding: '20px 40px',
    textAlign: 'center',
    position: 'relative'
  },
  title: {
    margin: '0 0 10px 0',
    fontSize: '28px',
    fontWeight: '600'
  },
  subtitle: {
    margin: '0',
    fontSize: '16px',
    opacity: '0.9'
  },
  userInfo: {
    position: 'absolute',
    right: '40px',
    top: '50%',
    transform: 'translateY(-50%)',
    display: 'flex',
    alignItems: 'center',
    gap: '20px'
  },
  userName: {
    fontSize: '14px',
    fontWeight: '500',
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    padding: '5px 15px',
    borderRadius: '20px',
    backdropFilter: 'blur(10px)'
  },
  logoutButton: {
    backgroundColor: '#e74c3c',
    color: 'white',
    border: 'none',
    padding: '8px 16px',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '500',
    transition: 'background-color 0.3s ease'
  },
  main: {
    flex: '1',
    padding: '40px 20px',
    maxWidth: '1200px',
    width: '100%',
    margin: '0 auto'
  },
  footer: {
    backgroundColor: '#2c3e50',
    color: 'white',
    padding: '20px',
    textAlign: 'center',
    fontSize: '14px'
  },
  footerNote: {
    margin: '10px 0 0 0',
    fontSize: '12px',
    opacity: '0.8'
  }
};

// Создаем и добавляем стили для анимаций
useEffect(() => {
  const styleSheet = document.createElement('style');
  styleSheet.textContent = `
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    .card {
      animation: fadeIn 0.3s ease-out;
    }
  `;
  document.head.appendChild(styleSheet);
  
  return () => {
    document.head.removeChild(styleSheet);
  };
}, []);

export default App;