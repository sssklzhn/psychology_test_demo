// import React, { useState, useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';

// export const TestPage = ({ user, onLogout }) => {
//   const navigate = useNavigate();
//   const [questions, setQuestions] = useState([]);
//   const [currentQuestion, setCurrentQuestion] = useState(0);
//   const [answers, setAnswers] = useState({});
//   const [loading, setLoading] = useState(true);
//   const [submitting, setSubmitting] = useState(false);
//   const [completed, setCompleted] = useState(false);
//   const [results, setResults] = useState(null);
//   const [error, setError] = useState('');

//   useEffect(() => {
//     // Проверяем, не завершен ли уже тест
//     if (user && user.isCompleted) {
//       setCompleted(true);
//     }
    
//     loadQuestions();
//   }, [user]);

//   const loadQuestions = async () => {
//   try {
//     console.log("🔍 Загрузка вопросов...");
    
//     const token = localStorage.getItem('psychology_test_token');
//     console.log("📝 Токен:", token ? token.substring(0, 20) + "..." : "Нет токена");
    
//     // Проверим весь localStorage
//     console.log("🔍 Все ключи в localStorage:", Object.keys(localStorage));
    
//     // Проверим сохранен ли пользователь
//     const userData = localStorage.getItem('user');
//     console.log("👤 Пользователь из 'user':", userData);
    
//     // 🔥 ВОЗВРАЩАЕМ заголовок Authorization
//     if (!token) {
//       console.error("❌ НЕТ ТОКЕНА в localStorage!");
//       setError("Требуется авторизация. Пожалуйста, войдите заново.");
//       return;
//     }
    
//     const response = await fetch('http://localhost:8000/api/questions', {
//       headers: {
//         'Authorization': `Bearer ${token}`  // 🔥 ВКЛЮЧАЕМ ЗАГОЛОВОК
//       }
//     });
    
//     console.log("📊 Статус ответа:", response.status);
//     console.log("📊 OK:", response.ok);
    
//     if (!response.ok) {
//       const errorText = await response.text();
//       console.error("❌ Ошибка сервера:", errorText);
      
//       if (response.status === 401) {
//         // Неавторизован - очищаем localStorage и переходим на логин
//         localStorage.removeItem('psychology_test_token');
//         localStorage.removeItem('user');
//         localStorage.removeItem('psychology_test_user');
//         localStorage.removeItem('access_token');
//         localStorage.removeItem('auth_token');
//         window.location.href = '/login';
//         return;
//       }
      
//       throw new Error(`HTTP error! status: ${response.status}`);
//     }
    
//     const data = await response.json();
//     console.log("✅ Успешный ответ от сервера");
//     console.log("📦 Данные:", data);
    
//     if (data.success) {
//       console.log(`✅ Загружено ${data.questions?.length || 0} вопросов`);
//       setQuestions(data.questions || []);
//     } else {
//       console.log("❌ Ошибка в данных:", data.message);
//       setError(data.message || 'Ошибка загрузки вопросов');
//     }
//   } catch (error) {
//     console.error('❌ Ошибка загрузки вопросов:', error);
//     setError('Ошибка соединения с сервером: ' + error.message);
//   } finally {
//     setLoading(false);
//   }
// };

//   const handleAnswer = (answer) => {
//     const questionId = questions[currentQuestion]?.id;
//     if (questionId) {
//       setAnswers({
//         ...answers,
//         [questionId]: answer
//       });
//     }
    
//     // Автоматически переходим к следующему вопросу
//     if (currentQuestion < questions.length - 1) {
//       setCurrentQuestion(currentQuestion + 1);
//     }
//   };

//   const handlePrevQuestion = () => {
//     if (currentQuestion > 0) {
//       setCurrentQuestion(currentQuestion - 1);
//     }
//   };

//   const handleNextQuestion = () => {
//     if (currentQuestion < questions.length - 1) {
//       setCurrentQuestion(currentQuestion + 1);
//     }
//   };

//   const handleSubmitTest = async () => {
//     // Проверяем, что на все вопросы ответили
//     const answeredCount = Object.keys(answers).length;
//     if (answeredCount < questions.length) {
//       alert(`Вы ответили только на ${answeredCount} из ${questions.length} вопросов. Ответьте на все вопросы перед завершением.`);
//       return;
//     }
    
//     // Подтверждение
//     if (!window.confirm('Вы уверены, что хотите завершить тест? После завершения изменить ответы будет нельзя.')) {
//       return;
//     }
    
//     setSubmitting(true);
    
//     try {
//       const token = localStorage.getItem('psychology_test_token');
      
//       // Конвертируем answers в массив
//       const answersArray = Object.keys(answers).map(questionId => ({
//         question_id: questionId,
//         answer: answers[questionId]
//       }));
      
//       const response = await fetch('http://localhost:8000/api/test/submit', {
//         method: 'POST',
//         headers: {
//           'Authorization': `Bearer ${token}`,
//           'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ answers: answersArray })
//       });
      
//       const data = await response.json();
//       if (data.success) {
//         setResults(data.results);
//         setCompleted(true);
        
//         // Обновляем статус пользователя
//         const storedUser = JSON.parse(localStorage.getItem('psychology_test_user') || '{}');
//         storedUser.isCompleted = true;
//         localStorage.setItem('psychology_test_user', JSON.stringify(storedUser));
//       } else {
//         setError('Ошибка отправки теста');
//       }
//     } catch (error) {
//       console.error('Error submitting test:', error);
//       setError('Ошибка соединения с сервером');
//     } finally {
//       setSubmitting(false);
//     }
//   };

//   if (loading) {
//     return (
//       <div style={{ textAlign: 'center', padding: '50px' }}>
//         <div className="loading-spinner"></div>
//         <p>Загрузка вопросов...</p>
//       </div>
//     );
//   }

//   if (completed) {
//     return (
//       <div className="container">
//         <div className="card" style={{ maxWidth: '800px', margin: '50px auto', textAlign: 'center' }}>
//           <h2>✅ Тест успешно завершен!</h2>
//           <p>Благодарим за прохождение тестирования.</p>
          
//           {results && (
//             <div style={{ marginTop: '30px' }}>
//               <h3>Ваши результаты:</h3>
              
//               <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px', margin: '20px 0' }}>
//                 {results.scores && Object.entries(results.scores).map(([scale, score]) => (
//                   <div key={scale} style={{ 
//                     backgroundColor: '#f8f9fa', 
//                     padding: '15px', 
//                     borderRadius: '5px',
//                     border: '1px solid #dee2e6'
//                   }}>
//                     <strong>{scale}:</strong> {score} баллов
//                   </div>
//                 ))}
//               </div>
              
//               <div style={{ margin: '30px 0' }}>
//                 <h4>Рекомендация:</h4>
//                 <div style={{
//                   display: 'inline-block',
//                   padding: '10px 20px',
//                   borderRadius: '20px',
//                   color: 'white',
//                   fontWeight: 'bold',
//                   backgroundColor: 
//                     results.recommendation === 'рекомендован' ? '#28a745' :
//                     results.recommendation === 'условно рекомендован' ? '#ffc107' :
//                     results.recommendation === 'ретест' ? '#17a2b8' : '#dc3545'
//                 }}>
//                   {results.recommendation.toUpperCase()}
//                 </div>
//               </div>
//             </div>
//           )}
          
//           <div className="alert alert-info" style={{ marginTop: '30px' }}>
//             <p>Результаты были отправлены администратору. Вы можете закрыть эту страницу.</p>
//           </div>
          
//           <button 
//             onClick={onLogout}
//             className="btn btn-primary"
//             style={{ marginTop: '20px' }}
//           >
//             Выйти из системы
//           </button>
//         </div>
//       </div>
//     );
//   }

//   if (error) {
//     return (
//       <div className="container">
//         <div className="alert alert-error">{error}</div>
//         <button onClick={() => window.location.reload()} className="btn btn-primary">
//           Попробовать снова
//         </button>
//       </div>
//     );
//   }

//   const currentQuestionData = questions[currentQuestion];
//   const progress = ((currentQuestion + 1) / questions.length) * 100;
//   const answeredCount = Object.keys(answers).length;

//   return (
//     <div className="container">
//       <div className="card">
//         <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
//           <h3 style={{ margin: 0 }}>Психологическое тестирование</h3>
//           <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
//             <span style={{ fontSize: '14px', color: '#666' }}>
//               Ответов: {answeredCount}/{questions.length}
//             </span>
//             <span style={{ fontSize: '14px', color: '#666' }}>
//               Тестируемый: {user?.login || 'Неизвестно'}
//             </span>
//           </div>
//         </div>
        
//         {/* Прогресс бар */}
//         <div style={{ marginBottom: '30px' }}>
//           <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
//             <span style={{ fontSize: '14px' }}>Вопрос {currentQuestion + 1} из {questions.length}</span>
//             <span style={{ fontSize: '14px' }}>{Math.round(progress)}%</span>
//           </div>
//           <div style={{
//             height: '8px',
//             backgroundColor: '#e9ecef',
//             borderRadius: '4px',
//             overflow: 'hidden'
//           }}>
//             <div style={{
//               width: `${progress}%`,
//               height: '100%',
//               backgroundColor: '#3498db',
//               transition: 'width 0.3s'
//             }}></div>
//           </div>
//         </div>
        
//         {/* Вопрос */}
//         {currentQuestionData && (
//           <div>
//             <h4 style={{ marginBottom: '30px', lineHeight: '1.6' }}>
//               {currentQuestionData.text}
//             </h4>
            
//             <div style={{ display: 'flex', justifyContent: 'center', gap: '30px', marginBottom: '40px' }}>
//               <button
//                 onClick={() => handleAnswer(true)}
//                 style={{
//                   padding: '15px 40px',
//                   fontSize: '18px',
//                   backgroundColor: answers[currentQuestionData.id] === true ? '#28a745' : '#f8f9fa',
//                   color: answers[currentQuestionData.id] === true ? 'white' : '#333',
//                   border: '2px solid #28a745',
//                   borderRadius: '8px',
//                   cursor: 'pointer',
//                   transition: 'all 0.3s'
//                 }}
//               >
//                 Да
//               </button>
              
//               <button
//                 onClick={() => handleAnswer(false)}
//                 style={{
//                   padding: '15px 40px',
//                   fontSize: '18px',
//                   backgroundColor: answers[currentQuestionData.id] === false ? '#dc3545' : '#f8f9fa',
//                   color: answers[currentQuestionData.id] === false ? 'white' : '#333',
//                   border: '2px solid #dc3545',
//                   borderRadius: '8px',
//                   cursor: 'pointer',
//                   transition: 'all 0.3s'
//                 }}
//               >
//                 Нет
//               </button>
//             </div>
//           </div>
//         )}
        
//         {/* Навигация */}
//         <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '30px' }}>
//           <button
//             onClick={handlePrevQuestion}
//             disabled={currentQuestion === 0}
//             className="btn btn-secondary"
//           >
//             ← Назад
//           </button>
          
//           {currentQuestion === questions.length - 1 ? (
//             <button
//               onClick={handleSubmitTest}
//               disabled={submitting || answeredCount < questions.length}
//               className="btn btn-success"
//             >
//               {submitting ? 'Отправка...' : 'Завершить тест'}
//             </button>
//           ) : (
//             <button
//               onClick={handleNextQuestion}
//               disabled={currentQuestion === questions.length - 1}
//               className="btn btn-primary"
//             >
//               Далее →
//             </button>
//           )}
//         </div>
        
//         <div style={{ marginTop: '20px', fontSize: '14px', color: '#666', textAlign: 'center' }}>
//           <p>Ваши ответы автоматически сохраняются. Вы можете вернуться к предыдущим вопросам.</p>
//         </div>
//       </div>
//     </div>
//   );
// };
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from './../api'; // Импортируем централизованный API

export const TestPage = ({ user, onLogout }) => {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    // Проверяем, не завершен ли уже тест
    if (user && user.isCompleted) {
      setCompleted(true);
    }
    
    loadQuestions();
  }, [user]);

  const loadQuestions = async () => {
    try {
      console.log("🔍 Загрузка вопросов...");
      
      const token = localStorage.getItem('psychology_test_token');
      
      if (!token) {
        console.error("❌ НЕТ ТОКЕНА в localStorage!");
        setError("Требуется авторизация. Пожалуйста, войдите заново.");
        return;
      }
      
      // Используем централизованный API
      const data = await api.getQuestions();
      
      console.log("✅ Успешный ответ от сервера");
      console.log(`✅ Загружено ${data.questions?.length || 0} вопросов`);
      setQuestions(data.questions || []);
      
    } catch (error) {
      console.error('❌ Ошибка загрузки вопросов:', error);
      
      if (error.message.includes('401') || error.message.includes('Unauthorized')) {
        // Неавторизован - очищаем localStorage и переходим на логин
        localStorage.removeItem('psychology_test_token');
        localStorage.removeItem('user');
        localStorage.removeItem('psychology_test_user');
        localStorage.removeItem('access_token');
        localStorage.removeItem('auth_token');
        window.location.href = '/login';
        return;
      }
      
      setError('Ошибка соединения с сервером: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (answer) => {
    const questionId = questions[currentQuestion]?.id;
    if (questionId) {
      setAnswers({
        ...answers,
        [questionId]: answer
      });
    }
    
    // Автоматически переходим к следующему вопросу
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleNextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handleSubmitTest = async () => {
    // Проверяем, что на все вопросы ответили
    const answeredCount = Object.keys(answers).length;
    if (answeredCount < questions.length) {
      alert(`Вы ответили только на ${answeredCount} из ${questions.length} вопросов. Ответьте на все вопросы перед завершением.`);
      return;
    }
    
    // Подтверждение
    if (!window.confirm('Вы уверены, что хотите завершить тест? После завершения изменить ответы будет нельзя.')) {
      return;
    }
    
    setSubmitting(true);
    
    try {
      // Конвертируем answers в массив
      const answersArray = Object.keys(answers).map(questionId => ({
        question_id: questionId,
        answer: answers[questionId]
      }));
      
      // Используем централизованный API
      const data = await api.submitTest(answersArray);
      
      if (data.success) {
        setResults(data.results);
        setCompleted(true);
        
        // Обновляем статус пользователя
        const storedUser = JSON.parse(localStorage.getItem('user') || '{}');
        storedUser.isCompleted = true;
        localStorage.setItem('user', JSON.stringify(storedUser));
      } else {
        setError('Ошибка отправки теста');
      }
    } catch (error) {
      console.error('Error submitting test:', error);
      setError('Ошибка соединения с сервером');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <div className="loading-spinner"></div>
        <p>Загрузка вопросов...</p>
      </div>
    );
  }

  if (completed) {
    return (
      <div className="container">
        <div className="card" style={{ maxWidth: '800px', margin: '50px auto', textAlign: 'center' }}>
          <h2>✅ Тест успешно завершен!</h2>
          <p>Благодарим за прохождение тестирования.</p>
          
          {results && (
            <div style={{ marginTop: '30px' }}>
              <h3>Ваши результаты:</h3>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px', margin: '20px 0' }}>
                {results.scores && Object.entries(results.scores).map(([scale, score]) => (
                  <div key={scale} style={{ 
                    backgroundColor: '#f8f9fa', 
                    padding: '15px', 
                    borderRadius: '5px',
                    border: '1px solid #dee2e6'
                  }}>
                    <strong>{scale}:</strong> {score} баллов
                  </div>
                ))}
              </div>
              
              <div style={{ margin: '30px 0' }}>
                <h4>Рекомендация:</h4>
                <div style={{
                  display: 'inline-block',
                  padding: '10px 20px',
                  borderRadius: '20px',
                  color: 'white',
                  fontWeight: 'bold',
                  backgroundColor: 
                    results.recommendation === 'рекомендован' ? '#28a745' :
                    results.recommendation === 'условно рекомендован' ? '#ffc107' :
                    results.recommendation === 'ретест' ? '#17a2b8' : '#dc3545'
                }}>
                  {results.recommendation.toUpperCase()}
                </div>
              </div>
            </div>
          )}
          
          <div className="alert alert-info" style={{ marginTop: '30px' }}>
            <p>Результаты были отправлены администратору. Вы можете закрыть эту страницу.</p>
          </div>
          
          <button 
            onClick={onLogout}
            className="btn btn-primary"
            style={{ marginTop: '20px' }}
          >
            Выйти из системы
          </button>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div className="alert alert-error">{error}</div>
        <button onClick={() => window.location.reload()} className="btn btn-primary">
          Попробовать снова
        </button>
      </div>
    );
  }

  const currentQuestionData = questions[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;
  const answeredCount = Object.keys(answers).length;

  return (
    <div className="container">
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h3 style={{ margin: 0 }}>Психологическое тестирование</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <span style={{ fontSize: '14px', color: '#666' }}>
              Ответов: {answeredCount}/{questions.length}
            </span>
            <span style={{ fontSize: '14px', color: '#666' }}>
              Тестируемый: {user?.login || 'Неизвестно'}
            </span>
          </div>
        </div>
        
        {/* Прогресс бар */}
        <div style={{ marginBottom: '30px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
            <span style={{ fontSize: '14px' }}>Вопрос {currentQuestion + 1} из {questions.length}</span>
            <span style={{ fontSize: '14px' }}>{Math.round(progress)}%</span>
          </div>
          <div style={{
            height: '8px',
            backgroundColor: '#e9ecef',
            borderRadius: '4px',
            overflow: 'hidden'
          }}>
            <div style={{
              width: `${progress}%`,
              height: '100%',
              backgroundColor: '#3498db',
              transition: 'width 0.3s'
            }}></div>
          </div>
        </div>
        
        {/* Вопрос */}
        {currentQuestionData && (
          <div>
            <h4 style={{ marginBottom: '30px', lineHeight: '1.6' }}>
              {currentQuestionData.text}
            </h4>
            
            <div style={{ display: 'flex', justifyContent: 'center', gap: '30px', marginBottom: '40px' }}>
              <button
                onClick={() => handleAnswer(true)}
                style={{
                  padding: '15px 40px',
                  fontSize: '18px',
                  backgroundColor: answers[currentQuestionData.id] === true ? '#28a745' : '#f8f9fa',
                  color: answers[currentQuestionData.id] === true ? 'white' : '#333',
                  border: '2px solid #28a745',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  transition: 'all 0.3s'
                }}
              >
                Да
              </button>
              
              <button
                onClick={() => handleAnswer(false)}
                style={{
                  padding: '15px 40px',
                  fontSize: '18px',
                  backgroundColor: answers[currentQuestionData.id] === false ? '#dc3545' : '#f8f9fa',
                  color: answers[currentQuestionData.id] === false ? 'white' : '#333',
                  border: '2px solid #dc3545',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  transition: 'all 0.3s'
                }}
              >
                Нет
              </button>
            </div>
          </div>
        )}
        
        {/* Навигация */}
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '30px' }}>
          <button
            onClick={handlePrevQuestion}
            disabled={currentQuestion === 0}
            className="btn btn-secondary"
          >
            ← Назад
          </button>
          
          {currentQuestion === questions.length - 1 ? (
            <button
              onClick={handleSubmitTest}
              disabled={submitting || answeredCount < questions.length}
              className="btn btn-success"
            >
              {submitting ? 'Отправка...' : 'Завершить тест'}
            </button>
          ) : (
            <button
              onClick={handleNextQuestion}
              disabled={currentQuestion === questions.length - 1}
              className="btn btn-primary"
            >
              Далее →
            </button>
          )}
        </div>
        
        <div style={{ marginTop: '20px', fontSize: '14px', color: '#666', textAlign: 'center' }}>
          <p>Ваши ответы автоматически сохраняются. Вы можете вернуться к предыдущим вопросам.</p>
        </div>
      </div>
    </div>
  );
};