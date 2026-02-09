// import React, { useState, useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';
// import { ResultTable } from './../components/admin/ResultsTable'; 

// export const AdminPage = ({ onLogout }) => {
//   const navigate = useNavigate();
//   const [users, setUsers] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [generating, setGenerating] = useState(false);
//   const [count, setCount] = useState(10);
//   const [message, setMessage] = useState('');
//   const [selectedUser, setSelectedUser] = useState(null);
//   const [showResultsModal, setShowResultsModal] = useState(false);
//   const [userResults, setUserResults] = useState(null);
//   const [showConfirmModal, setShowConfirmModal] = useState(false);
//   const [userIdToReset, setUserIdToReset] = useState(null);

//   useEffect(() => {
//     loadUsers();
//   }, []);

//   const loadUsers = async () => {
//     setLoading(true);
//     setMessage('');
//     try {
//       const token = localStorage.getItem('psychology_test_token');
//       const response = await fetch('http://localhost:8000/api/admin/users', {
//         headers: {
//           'Authorization': `Bearer ${token}`
//         }
//       });
      
//       const data = await response.json();
//       if (data.success) {
//         setUsers(data.users || []);
//       } else {
//         setMessage('Ошибка загрузки пользователей: ' + (data.detail || 'Неизвестная ошибка'));
//       }
//     } catch (error) {
//       console.error('Error loading users:', error);
//       setMessage('Ошибка соединения с сервером');
//     } finally {
//       setLoading(false);
//     }
//   };

//   const generateUsers = async () => {
//     setGenerating(true);
//     setMessage('');
    
//     try {
//       const token = localStorage.getItem('psychology_test_token');
      
//       const response = await fetch(
//         `http://localhost:8000/api/admin/generate-and-download-users?count=${count}`,
//         {
//           method: 'POST',
//           headers: {
//             'Authorization': `Bearer ${token}`
//           }
//         }
//       );
      
//       if (response.ok) {
//         // Скачиваем файл
//         const blob = await response.blob();
//         const url = window.URL.createObjectURL(blob);
//         const link = document.createElement('a');
//         link.href = url;
//         link.download = response.headers.get('content-disposition')?.split('filename=')[1] || 'users.csv';
//         document.body.appendChild(link);
//         link.click();
//         document.body.removeChild(link);
        
//         setMessage(`✅ Создано ${count} пользователей. CSV файл скачан.`);
        
//         // Обновляем список
//         setTimeout(() => loadUsers(), 1000);
//       } else {
//         const errorData = await response.json();
//         setMessage(`❌ Ошибка: ${errorData.detail || 'Неизвестная ошибка'}`);
//       }
      
//     } catch (error) {
//       console.error('Error generating users:', error);
//       setMessage('❌ Ошибка соединения с сервером');
//     } finally {
//       setGenerating(false);
//     }
//   };

//   // Функция просмотра результатов пользователя
//   const viewUserResults = async (user) => {
//     try {
//       const token = localStorage.getItem('psychology_test_token');
//       const response = await fetch(`http://localhost:8000/api/admin/user/${user.id}/answers`, {
//         headers: {
//           'Authorization': `Bearer ${token}`
//         }
//       });
      
//       const data = await response.json();
//       if (data.success) {
//         setSelectedUser(user);
//         setUserResults(data);
//         setShowResultsModal(true);
//       } else {
//         setMessage('❌ Ошибка загрузки результатов');
//       }
//     } catch (error) {
//       console.error('Error viewing user results:', error);
//       setMessage('❌ Ошибка загрузки результатов');
//     }
//   };

//   // Функция генерации PDF отчета пользователя
//   const generateUserPDF = async (user) => {
//     try {
//       const token = localStorage.getItem('psychology_test_token');
//       const response = await fetch(`http://localhost:8000/api/export/pdf/user/${user.id}`, {
//         headers: {
//           'Authorization': `Bearer ${token}`
//         }
//       });
      
//       if (response.ok) {
//         const blob = await response.blob();
//         const url = window.URL.createObjectURL(blob);
//         const link = document.createElement('a');
//         link.href = url;
//         link.download = `report_${user.login}_${new Date().toISOString().slice(0, 10)}.pdf`;
//         document.body.appendChild(link);
//         link.click();
//         document.body.removeChild(link);
        
//         setMessage(`✅ PDF отчет для ${user.login} скачан`);
//       } else {
//         const errorData = await response.json();
//         setMessage(`❌ Ошибка: ${errorData.detail || 'Неизвестная ошибка'}`);
//       }
//     } catch (error) {
//       console.error('Error generating PDF:', error);
//       setMessage('❌ Ошибка генерации PDF');
//     }
//   };

//   // Функция генерации общего PDF отчета
//   const generateSummaryPDF = async () => {
//     try {
//       const token = localStorage.getItem('psychology_test_token');
//       const response = await fetch('http://localhost:8000/api/export/pdf/summary', {
//         headers: {
//           'Authorization': `Bearer ${token}`
//         }
//       });
      
//       if (response.ok) {
//         const blob = await response.blob();
//         const url = window.URL.createObjectURL(blob);
//         const link = document.createElement('a');
//         link.href = url;
//         link.download = `summary_report_${new Date().toISOString().slice(0, 10)}.pdf`;
//         document.body.appendChild(link);
//         link.click();
//         document.body.removeChild(link);
        
//         setMessage('✅ Общий PDF отчет скачан');
//       } else {
//         const errorData = await response.json();
//         setMessage(`❌ Ошибка: ${errorData.detail || 'Неизвестная ошибка'}`);
//       }
//     } catch (error) {
//       console.error('Error generating summary PDF:', error);
//       setMessage('❌ Ошибка генерации общего отчета');
//     }
//   };

//   // Функция экспорта CSV результатов
//   const exportResultsCSV = async () => {
//     try {
//       const token = localStorage.getItem('psychology_test_token');
//       const response = await fetch('http://localhost:8000/api/export/csv/summary', {
//         headers: {
//           'Authorization': `Bearer ${token}`
//         }
//       });
      
//       if (response.ok) {
//         const blob = await response.blob();
//         const url = window.URL.createObjectURL(blob);
//         const link = document.createElement('a');
//         link.href = url;
//         link.download = `results_${new Date().toISOString().slice(0, 10)}.csv`;
//         document.body.appendChild(link);
//         link.click();
//         document.body.removeChild(link);
        
//         setMessage('✅ CSV отчет скачан');
//       } else {
//         const errorData = await response.json();
//         setMessage(`❌ Ошибка: ${errorData.detail || 'Неизвестная ошибка'}`);
//       }
//     } catch (error) {
//       console.error('Error exporting CSV:', error);
//       setMessage('❌ Ошибка экспорта CSV');
//     }
//   };

//   // Функция сброса теста пользователя (теперь открывает модальное окно)
//   const resetUserTest = (userId) => {
//     setUserIdToReset(userId);
//     setShowConfirmModal(true);
//   };

//   const confirmReset = async () => {
//     try {
//       const token = localStorage.getItem('psychology_test_token');
//       const response = await fetch(`http://localhost:8000/api/admin/user/${userIdToReset}/reset`, {
//         method: 'POST',
//         headers: {
//           'Authorization': `Bearer ${token}`
//         }
//       });
      
//       const data = await response.json();
//       if (data.success) {
//         setMessage(`✅ Тест пользователя сброшен. Удалено: ${data.deleted.answers} ответов, ${data.deleted.results} результатов`);
//         loadUsers();
//       } else {
//         setMessage('❌ Ошибка сброса теста');
//       }
//     } catch (error) {
//       console.error('Error resetting user test:', error);
//       setMessage('❌ Ошибка сброса теста');
//     } finally {
//       setShowConfirmModal(false);
//       setUserIdToReset(null);
//     }
//   };

//   // Функция просмотра ответов пользователя
//   const viewUserAnswers = async (user) => {
//     try {
//       const token = localStorage.getItem('psychology_test_token');
//       const response = await fetch(`http://localhost:8000/api/admin/user/${user.id}/answers`, {
//         headers: {
//           'Authorization': `Bearer ${token}`
//         }
//       });
      
//       const data = await response.json();
//       if (data.success) {
//         const answersText = data.answers.map(a => 
//           `Вопрос ${a.question_id}: ${a.answer ? '✅ Да' : '❌ Нет'} (${a.points} баллов)`
//         ).join('\n');
        
//         alert(`
// 👤 ${user.login}
// 📊 Статус: ${data.user.isCompleted ? 'Завершен' : 'Не завершен'}
// 📅 Дата завершения: ${data.user.completedAt || 'Нет'}
// 📝 Ответов: ${data.count}

// 📋 Ответы на вопросы:
// ${answersText}

// ${data.results ? `
// 📈 РЕЗУЛЬТАТЫ:
// ${Object.entries(data.results.scores || {}).map(([scale, score]) => 
//   `${scale}: ${score} баллов (${data.results.interpretations?.[scale] || 'Нет интерпретации'})`
// ).join('\n')}

// 🏆 РЕКОМЕНДАЦИЯ: ${data.results.recommendation?.toUpperCase() || 'Нет'}
// ` : '📊 Результаты еще не обработаны'}
//         `);
//       }
//     } catch (error) {
//       console.error('Error viewing answers:', error);
//       setMessage('❌ Ошибка загрузки ответов');
//     }
//   };

//   return (
//     <div className="container">
//       <h2 style={{ marginBottom: '30px' }}>Панель администратора</h2>
      
//       {/* Панель генерации пользователей */}
//       <div className="card" style={{ marginBottom: '30px' }}>
//         <h3>Генерация тестируемых</h3>
        
//         <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginBottom: '20px' }}>
//           <label>Количество пользователей:</label>
//           <input
//             type="number"
//             value={count}
//             onChange={(e) => setCount(parseInt(e.target.value) || 10)}
//             min="1"
//             max="100"
//             style={{ width: '100px', padding: '8px' }}
//           />
          
//           <button 
//             onClick={generateUsers}
//             disabled={generating}
//             className="btn btn-success"
//           >
//             {generating ? '🔄 Генерация...' : '🚀 Сгенерировать'}
//           </button>
//         </div>
        
//         {message && (
//           <div className={`alert ${message.includes('✅') ? 'alert-success' : 'alert-error'}`}>
//             {message}
//           </div>
//         )}
        
//         <p style={{ fontSize: '14px', color: '#666' }}>
//           После генерации автоматически скачается CSV файл с логинами и паролями.
//         </p>
//       </div>
      
//       {/* Панель результатов */}
//       <div className="card">
//         <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
//           <h3 style={{ margin: 0 }}>Результаты тестирования</h3>
//           <div style={{ display: 'flex', gap: '10px' }}>
//             <button onClick={loadUsers} disabled={loading} className="btn btn-primary">
//               {loading ? '🔄 Обновление...' : '📊 Обновить'}
//             </button>
//             <button onClick={generateSummaryPDF} className="btn btn-success">
//               📄 Общий PDF
//             </button>
//             <button onClick={exportResultsCSV} className="btn btn-info">
//               📊 CSV Экспорт
//             </button>
//           </div>
//         </div>
        
//         {loading ? (
//           <div style={{ textAlign: 'center', padding: '20px' }}>
//             <div className="loading-spinner"></div>
//             <p>Загрузка пользователей...</p>
//           </div>
//         ) : users.length === 0 ? (
//           <p style={{ textAlign: 'center', padding: '20px', color: '#666' }}>
//             Пользователи не найдены. Сгенерируйте тестируемых.
//           </p>
//         ) : (
//           <ResultTable 
//             users={users}
//             onViewResults={viewUserResults}
//             onGeneratePDF={generateUserPDF}
//             onResetTest={resetUserTest}
//             onViewAnswers={viewUserAnswers}
//           />
//         )}
//       </div>

//       {/* Модальное окно с результатами */}
//       {showResultsModal && selectedUser && userResults && (
//         <div className="modal-overlay" onClick={() => setShowResultsModal(false)}>
//           <div className="modal" onClick={e => e.stopPropagation()}>
//             <div className="modal-header">
//               <h3>📊 Результаты: {selectedUser.login}</h3>
//               <button onClick={() => setShowResultsModal(false)} className="btn-close">×</button>
//             </div>
            
//             <div className="modal-body">
//               <div style={{ marginBottom: '20px' }}>
//                 <h4>📋 Информация о тестировании:</h4>
//                 <p><strong>Логин:</strong> {selectedUser.login}</p>
//                 <p><strong>Статус:</strong> {userResults.user.isCompleted ? '✅ Завершен' : '⏳ В процессе'}</p>
//                 <p><strong>Дата завершения:</strong> {userResults.user.completedAt || 'Нет'}</p>
//                 <p><strong>Количество ответов:</strong> {userResults.count}</p>
//               </div>
              
//               {userResults.results && (
//                 <>
//                   <div style={{ marginBottom: '20px' }}>
//                     <h4>📈 Баллы по шкалам:</h4>
//                     <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px' }}>
//                       {Object.entries(userResults.results.scores || {}).map(([scale, score]) => (
//                         <div key={scale} style={{ 
//                           backgroundColor: '#f8f9fa', 
//                           padding: '10px', 
//                           borderRadius: '5px',
//                           border: '1px solid #dee2e6'
//                         }}>
//                           <strong>{scale}:</strong> {score} баллов
//                           <div style={{ fontSize: '12px', color: '#666' }}>
//                             {userResults.results.interpretations?.[scale]}
//                           </div>
//                         </div>
//                       ))}
//                     </div>
//                   </div>
                  
//                   <div style={{ marginBottom: '20px' }}>
//                     <h4>🏆 Рекомендация:</h4>
//                     <div style={{
//                       display: 'inline-block',
//                       padding: '10px 20px',
//                       borderRadius: '20px',
//                       color: 'white',
//                       fontWeight: 'bold',
//                       backgroundColor: 
//                         userResults.results.recommendation === 'рекомендован' ? '#28a745' :
//                         userResults.results.recommendation === 'условно рекомендован' ? '#ffc107' :
//                         userResults.results.recommendation === 'ретест' ? '#17a2b8' : '#dc3545'
//                     }}>
//                       {userResults.results.recommendation?.toUpperCase() || 'НЕТ ДАННЫХ'}
//                     </div>
//                   </div>
//                 </>
//               )}
              
//               <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', marginTop: '20px' }}>
//                 <button 
//                   onClick={() => generateUserPDF(selectedUser)}
//                   className="btn btn-success"
//                 >
//                   📄 Скачать PDF
//                 </button>
//                 <button 
//                   onClick={() => setShowResultsModal(false)}
//                   className="btn btn-secondary"
//                 >
//                   Закрыть
//                 </button>
//               </div>
//             </div>
//           </div>
//         </div>
//       )}

//       {/* Модальное окно подтверждения сброса */}
//       {showConfirmModal && (
//         <div className="modal-overlay" onClick={() => setShowConfirmModal(false)}>
//           <div className="modal" onClick={e => e.stopPropagation()} style={{ maxWidth: '500px' }}>
//             <div className="modal-header">
//               <h3>⚠️ Подтверждение</h3>
//               <button onClick={() => setShowConfirmModal(false)} className="btn-close">×</button>
//             </div>
//             <div className="modal-body">
//               <p>Вы уверены, что хотите сбросить результаты теста? Все данные будут удалены.</p>
//               <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', marginTop: '20px' }}>
//                 <button 
//                   onClick={() => setShowConfirmModal(false)}
//                   className="btn btn-secondary"
//                 >
//                   Отмена
//                 </button>
//                 <button 
//                   onClick={confirmReset}
//                   className="btn btn-danger"
//                 >
//                   Сбросить
//                 </button>
//               </div>
//             </div>
//           </div>
//         </div>
//       )}

//       {/* Стили для модального окна */}
//       <style jsx>{`
//         .modal-overlay {
//           position: fixed;
//           top: 0;
//           left: 0;
//           right: 0;
//           bottom: 0;
//           background: rgba(0, 0, 0, 0.5);
//           display: flex;
//           justify-content: center;
//           align-items: center;
//           z-index: 1000;
//         }
        
//         .modal {
//           background: white;
//           border-radius: 8px;
//           padding: 20px;
//           max-width: 800px;
//           width: 90%;
//           max-height: 80vh;
//           overflow-y: auto;
//           box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
//         }
        
//         .modal-header {
//           display: flex;
//           justify-content: space-between;
//           align-items: center;
//           margin-bottom: 20px;
//           border-bottom: 1px solid #eee;
//           padding-bottom: 10px;
//         }
        
//         .modal-header h3 {
//           margin: 0;
//         }
        
//         .btn-close {
//           background: none;
//           border: none;
//           font-size: 24px;
//           cursor: pointer;
//           color: #666;
//         }
        
//         .btn-close:hover {
//           color: #333;
//         }
        
//         .modal-body {
//           padding: 10px 0;
//         }
        
//         .loading-spinner {
//           border: 4px solid #f3f3f3;
//           border-top: 4px solid #3498db;
//           border-radius: 50%;
//           width: 40px;
//           height: 40px;
//           animation: spin 1s linear infinite;
//           margin: 0 auto 10px;
//         }
        
//         @keyframes spin {
//           0% { transform: rotate(0deg); }
//           100% { transform: rotate(360deg); }
//         }
        
//         .alert-success {
//           background-color: #d4edda;
//           color: #155724;
//           padding: 10px;
//           border-radius: 4px;
//           border: 1px solid #c3e6cb;
//         }
        
//         .alert-error {
//           background-color: #f8d7da;
//           color: #721c24;
//           padding: 10px;
//           border-radius: 4px;
//           border: 1px solid #f5c6cb;
//         }
        
//         .btn {
//           padding: 8px 16px;
//           border: none;
//           border-radius: 4px;
//           cursor: pointer;
//           font-size: 14px;
//           transition: background-color 0.2s;
//         }
        
//         .btn-primary {
//           background-color: #007bff;
//           color: white;
//         }
        
//         .btn-primary:hover:not(:disabled) {
//           background-color: #0056b3;
//         }
        
//         .btn-success {
//           background-color: #28a745;
//           color: white;
//         }
        
//         .btn-success:hover:not(:disabled) {
//           background-color: #1e7e34;
//         }
        
//         .btn-info {
//           background-color: #17a2b8;
//           color: white;
//         }
        
//         .btn-info:hover:not(:disabled) {
//           background-color: #117a8b;
//         }
        
//         .btn-secondary {
//           background-color: #6c757d;
//           color: white;
//         }
        
//         .btn-secondary:hover:not(:disabled) {
//           background-color: #545b62;
//         }
        
//         .btn-danger {
//           background-color: #dc3545;
//           color: white;
//         }
        
//         .btn-danger:hover:not(:disabled) {
//           background-color: #bd2130;
//         }
        
//         .btn:disabled {
//           opacity: 0.6;
//           cursor: not-allowed;
//         }
//       `}</style>
//     </div>
//   );
// };
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ResultTable } from './../components/admin/ResultsTable'; 
import { api } from '../services/api';

export const AdminPage = ({ onLogout }) => {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [count, setCount] = useState(10);
  const [message, setMessage] = useState('');
  const [selectedUser, setSelectedUser] = useState(null);
  const [showResultsModal, setShowResultsModal] = useState(false);
  const [userResults, setUserResults] = useState(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [userIdToReset, setUserIdToReset] = useState(null);

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    setLoading(true);
    setMessage('');
    try {
      const data = await api.getUsers();
      setUsers(data.users || []);
    } catch (error) {
      console.error('Error loading users:', error);
      setMessage('Ошибка загрузки пользователей: ' + (error.message || 'Неизвестная ошибка'));
    } finally {
      setLoading(false);
    }
  };

  const generateUsers = async () => {
    setGenerating(true);
    setMessage('');
    
    try {
      // Используем централизованный API
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/api/admin/generate-and-download-users?count=${count}`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('psychology_test_token')}`
          }
        }
      );
      
      if (response.ok) {
        // Скачиваем файл
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = response.headers.get('content-disposition')?.split('filename=')[1] || 'users.csv';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        setMessage(`✅ Создано ${count} пользователей. CSV файл скачан.`);
        
        // Обновляем список
        setTimeout(() => loadUsers(), 1000);
      } else {
        const errorData = await response.json();
        setMessage(`❌ Ошибка: ${errorData.detail || 'Неизвестная ошибка'}`);
      }
      
    } catch (error) {
      console.error('Error generating users:', error);
      setMessage('❌ Ошибка соединения с сервером');
    } finally {
      setGenerating(false);
    }
  };

  // Функция просмотра результатов пользователя
  const viewUserResults = async (user) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/admin/user/${user.id}/answers`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('psychology_test_token')}`
        }
      });
      
      const data = await response.json();
      if (data.success) {
        setSelectedUser(user);
        setUserResults(data);
        setShowResultsModal(true);
      } else {
        setMessage('❌ Ошибка загрузки результатов');
      }
    } catch (error) {
      console.error('Error viewing user results:', error);
      setMessage('❌ Ошибка загрузки результатов');
    }
  };

  // Функция генерации PDF отчета пользователя
  const generateUserPDF = async (user) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/export/pdf/user/${user.id}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('psychology_test_token')}`
        }
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `report_${user.login}_${new Date().toISOString().slice(0, 10)}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        setMessage(`✅ PDF отчет для ${user.login} скачан`);
      } else {
        const errorData = await response.json();
        setMessage(`❌ Ошибка: ${errorData.detail || 'Неизвестная ошибка'}`);
      }
    } catch (error) {
      console.error('Error generating PDF:', error);
      setMessage('❌ Ошибка генерации PDF');
    }
  };

  // Функция генерации общего PDF отчета
  const generateSummaryPDF = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/export/pdf/summary`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('psychology_test_token')}`
        }
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `summary_report_${new Date().toISOString().slice(0, 10)}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        setMessage('✅ Общий PDF отчет скачан');
      } else {
        const errorData = await response.json();
        setMessage(`❌ Ошибка: ${errorData.detail || 'Неизвестная ошибка'}`);
      }
    } catch (error) {
      console.error('Error generating summary PDF:', error);
      setMessage('❌ Ошибка генерации общего отчета');
    }
  };

  // Функция экспорта CSV результатов
  const exportResultsCSV = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/export/csv/summary`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('psychology_test_token')}`
        }
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `results_${new Date().toISOString().slice(0, 10)}.csv`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        setMessage('✅ CSV отчет скачан');
      } else {
        const errorData = await response.json();
        setMessage(`❌ Ошибка: ${errorData.detail || 'Неизвестная ошибка'}`);
      }
    } catch (error) {
      console.error('Error exporting CSV:', error);
      setMessage('❌ Ошибка экспорта CSV');
    }
  };

  // Функция сброса теста пользователя
  const resetUserTest = (userId) => {
    setUserIdToReset(userId);
    setShowConfirmModal(true);
  };

  const confirmReset = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/admin/user/${userIdToReset}/reset`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('psychology_test_token')}`
        }
      });
      
      const data = await response.json();
      if (data.success) {
        setMessage(`✅ Тест пользователя сброшен. Удалено: ${data.deleted.answers} ответов, ${data.deleted.results} результатов`);
        loadUsers();
      } else {
        setMessage('❌ Ошибка сброса теста');
      }
    } catch (error) {
      console.error('Error resetting user test:', error);
      setMessage('❌ Ошибка сброса теста');
    } finally {
      setShowConfirmModal(false);
      setUserIdToReset(null);
    }
  };

  // Функция просмотра ответов пользователя
  const viewUserAnswers = async (user) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/admin/user/${user.id}/answers`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('psychology_test_token')}`
        }
      });
      
      const data = await response.json();
      if (data.success) {
        const answersText = data.answers.map(a => 
          `Вопрос ${a.question_id}: ${a.answer ? '✅ Да' : '❌ Нет'} (${a.points} баллов)`
        ).join('\n');
        
        alert(`
👤 ${user.login}
📊 Статус: ${data.user.isCompleted ? 'Завершен' : 'Не завершен'}
📅 Дата завершения: ${data.user.completedAt || 'Нет'}
📝 Ответов: ${data.count}

📋 Ответы на вопросы:
${answersText}

${data.results ? `
📈 РЕЗУЛЬТАТЫ:
${Object.entries(data.results.scores || {}).map(([scale, score]) => 
  `${scale}: ${score} баллов (${data.results.interpretations?.[scale] || 'Нет интерпретации'})`
).join('\n')}

🏆 РЕКОМЕНДАЦИЯ: ${data.results.recommendation?.toUpperCase() || 'Нет'}
` : '📊 Результаты еще не обработаны'}
        `);
      }
    } catch (error) {
      console.error('Error viewing answers:', error);
      setMessage('❌ Ошибка загрузки ответов');
    }
  };

  return (
    <div className="container">
      <h2 style={{ marginBottom: '30px' }}>Панель администратора</h2>
      
      {/* Панель генерации пользователей */}
      <div className="card" style={{ marginBottom: '30px' }}>
        <h3>Генерация тестируемых</h3>
        
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginBottom: '20px' }}>
          <label>Количество пользователей:</label>
          <input
            type="number"
            value={count}
            onChange={(e) => setCount(parseInt(e.target.value) || 10)}
            min="1"
            max="100"
            style={{ width: '100px', padding: '8px' }}
          />
          
          <button 
            onClick={generateUsers}
            disabled={generating}
            className="btn btn-success"
          >
            {generating ? '🔄 Генерация...' : '🚀 Сгенерировать'}
          </button>
        </div>
        
        {message && (
          <div className={`alert ${message.includes('✅') ? 'alert-success' : 'alert-error'}`}>
            {message}
          </div>
        )}
        
        <p style={{ fontSize: '14px', color: '#666' }}>
          После генерации автоматически скачается CSV файл с логинами и паролями.
        </p>
      </div>
      
      {/* Панель результатов */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h3 style={{ margin: 0 }}>Результаты тестирования</h3>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button onClick={loadUsers} disabled={loading} className="btn btn-primary">
              {loading ? '🔄 Обновление...' : '📊 Обновить'}
            </button>
            <button onClick={generateSummaryPDF} className="btn btn-success">
              📄 Общий PDF
            </button>
            <button onClick={exportResultsCSV} className="btn btn-info">
              📊 CSV Экспорт
            </button>
          </div>
        </div>
        
        {loading ? (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <div className="loading-spinner"></div>
            <p>Загрузка пользователей...</p>
          </div>
        ) : users.length === 0 ? (
          <p style={{ textAlign: 'center', padding: '20px', color: '#666' }}>
            Пользователи не найдены. Сгенерируйте тестируемых.
          </p>
        ) : (
          <ResultTable 
            users={users}
            onViewResults={viewUserResults}
            onGeneratePDF={generateUserPDF}
            onResetTest={resetUserTest}
            onViewAnswers={viewUserAnswers}
          />
        )}
      </div>

      {/* Модальное окно с результатами */}
      {showResultsModal && selectedUser && userResults && (
        <div className="modal-overlay" onClick={() => setShowResultsModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>📊 Результаты: {selectedUser.login}</h3>
              <button onClick={() => setShowResultsModal(false)} className="btn-close">×</button>
            </div>
            
            <div className="modal-body">
              <div style={{ marginBottom: '20px' }}>
                <h4>📋 Информация о тестировании:</h4>
                <p><strong>Логин:</strong> {selectedUser.login}</p>
                <p><strong>Статус:</strong> {userResults.user.isCompleted ? '✅ Завершен' : '⏳ В процессе'}</p>
                <p><strong>Дата завершения:</strong> {userResults.user.completedAt || 'Нет'}</p>
                <p><strong>Количество ответов:</strong> {userResults.count}</p>
              </div>
              
              {userResults.results && (
                <>
                  <div style={{ marginBottom: '20px' }}>
                    <h4>📈 Баллы по шкалам:</h4>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px' }}>
                      {Object.entries(userResults.results.scores || {}).map(([scale, score]) => (
                        <div key={scale} style={{ 
                          backgroundColor: '#f8f9fa', 
                          padding: '10px', 
                          borderRadius: '5px',
                          border: '1px solid #dee2e6'
                        }}>
                          <strong>{scale}:</strong> {score} баллов
                          <div style={{ fontSize: '12px', color: '#666' }}>
                            {userResults.results.interpretations?.[scale]}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div style={{ marginBottom: '20px' }}>
                    <h4>🏆 Рекомендация:</h4>
                    <div style={{
                      display: 'inline-block',
                      padding: '10px 20px',
                      borderRadius: '20px',
                      color: 'white',
                      fontWeight: 'bold',
                      backgroundColor: 
                        userResults.results.recommendation === 'рекомендован' ? '#28a745' :
                        userResults.results.recommendation === 'условно рекомендован' ? '#ffc107' :
                        userResults.results.recommendation === 'ретест' ? '#17a2b8' : '#dc3545'
                    }}>
                      {userResults.results.recommendation?.toUpperCase() || 'НЕТ ДАННЫХ'}
                    </div>
                  </div>
                </>
              )}
              
              <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', marginTop: '20px' }}>
                <button 
                  onClick={() => generateUserPDF(selectedUser)}
                  className="btn btn-success"
                >
                  📄 Скачать PDF
                </button>
                <button 
                  onClick={() => setShowResultsModal(false)}
                  className="btn btn-secondary"
                >
                  Закрыть
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Модальное окно подтверждения сброса */}
      {showConfirmModal && (
        <div className="modal-overlay" onClick={() => setShowConfirmModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()} style={{ maxWidth: '500px' }}>
            <div className="modal-header">
              <h3>⚠️ Подтверждение</h3>
              <button onClick={() => setShowConfirmModal(false)} className="btn-close">×</button>
            </div>
            <div className="modal-body">
              <p>Вы уверены, что хотите сбросить результаты теста? Все данные будут удалены.</p>
              <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', marginTop: '20px' }}>
                <button 
                  onClick={() => setShowConfirmModal(false)}
                  className="btn btn-secondary"
                >
                  Отмена
                </button>
                <button 
                  onClick={confirmReset}
                  className="btn btn-danger"
                >
                  Сбросить
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Стили для модального окна */}
      <style jsx>{`
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.5);
          display: flex;
          justify-content: center;
          align-items: center;
          z-index: 1000;
        }
        
        .modal {
          background: white;
          border-radius: 8px;
          padding: 20px;
          max-width: 800px;
          width: 90%;
          max-height: 80vh;
          overflow-y: auto;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        
        .modal-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
          border-bottom: 1px solid #eee;
          padding-bottom: 10px;
        }
        
        .modal-header h3 {
          margin: 0;
        }
        
        .btn-close {
          background: none;
          border: none;
          font-size: 24px;
          cursor: pointer;
          color: #666;
        }
        
        .btn-close:hover {
          color: #333;
        }
        
        .modal-body {
          padding: 10px 0;
        }
        
        .loading-spinner {
          border: 4px solid #f3f3f3;
          border-top: 4px solid #3498db;
          border-radius: 50%;
          width: 40px;
          height: 40px;
          animation: spin 1s linear infinite;
          margin: 0 auto 10px;
        }
        
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        
        .alert-success {
          background-color: #d4edda;
          color: #155724;
          padding: 10px;
          border-radius: 4px;
          border: 1px solid #c3e6cb;
        }
        
        .alert-error {
          background-color: #f8d7da;
          color: #721c24;
          padding: 10px;
          border-radius: 4px;
          border: 1px solid #f5c6cb;
        }
        
        .btn {
          padding: 8px 16px;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px;
          transition: background-color 0.2s;
        }
        
        .btn-primary {
          background-color: #007bff;
          color: white;
        }
        
        .btn-primary:hover:not(:disabled) {
          background-color: #0056b3;
        }
        
        .btn-success {
          background-color: #28a745;
          color: white;
        }
        
        .btn-success:hover:not(:disabled) {
          background-color: #1e7e34;
        }
        
        .btn-info {
          background-color: #17a2b8;
          color: white;
        }
        
        .btn-info:hover:not(:disabled) {
          background-color: #117a8b;
        }
        
        .btn-secondary {
          background-color: #6c757d;
          color: white;
        }
        
        .btn-secondary:hover:not(:disabled) {
          background-color: #545b62;
        }
        
        .btn-danger {
          background-color: #dc3545;
          color: white;
        }
        
        .btn-danger:hover:not(:disabled) {
          background-color: #bd2130;
        }
        
        .btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }
      `}</style>
    </div>
  );
};
